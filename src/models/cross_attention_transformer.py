import os
import math
import io
import wave
import json
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Dict, Any, Tuple, List, Optional
from pathlib import Path


class AudioFeatureExtractor:
    """
    Extracts time-frequency acoustic representations from raw audio bytes or files.
    Outputs normalized filterbank / spectral features (Frames x Features) suitable
    for the Cross-Attention Transformer key/value inputs.
    """
    def __init__(self, sample_rate: int = 16000, n_fft: int = 512, hop_length: int = 256, n_mels: int = 40):
        self.sample_rate = sample_rate
        self.n_fft = n_fft
        self.hop_length = hop_length
        self.n_mels = n_mels

    def extract_from_bytes(self, audio_bytes: bytes, max_frames: int = 128) -> np.ndarray:
        """
        Parses audio bytes (WAV, MP3, or raw PCM) into an acoustic spectrogram tensor (max_frames, n_mels).
        """
        pcm_data = self._read_pcm(audio_bytes)
        if len(pcm_data) < self.n_fft:
            # Pad with subtle dither noise if too short
            pcm_data = np.pad(pcm_data, (0, self.n_fft * 4), mode='constant')

        # Compute STFT spectrogram via numpy
        features = self._compute_spectrogram(pcm_data, max_frames=max_frames)
        return features

    def _read_pcm(self, audio_bytes: bytes) -> np.ndarray:
        """Attempts to read WAV PCM format or falls back to raw buffer parsing."""
        try:
            with wave.open(io.BytesIO(audio_bytes), "rb") as wf:
                n_channels = wf.getnchannels()
                sampwidth = wf.getsampwidth()
                frames = wf.readframes(min(wf.getnframes(), self.sample_rate * 30))  # Up to 30 sec
                
                if sampwidth == 2:
                    audio = np.frombuffer(frames, dtype=np.int16).astype(np.float32) / 32768.0
                elif sampwidth == 1:
                    audio = (np.frombuffer(frames, dtype=np.uint8).astype(np.float32) - 128.0) / 128.0
                else:
                    audio = np.frombuffer(frames, dtype=np.int16).astype(np.float32) / 32768.0

                if n_channels > 1:
                    audio = audio[::n_channels]
                return audio
        except Exception:
            # Raw byte heuristic fallback for MP3 / OGG or unknown headers
            raw = np.frombuffer(audio_bytes, dtype=np.uint8).astype(np.float32)
            normalized = (raw - 128.0) / 128.0
            return normalized

    def _compute_spectrogram(self, signal: np.ndarray, max_frames: int = 128) -> np.ndarray:
        """Computes multi-band acoustic energy and spectral centroid features."""
        n_samples = len(signal)
        n_frames = min(max_frames, max(1, (n_samples - self.n_fft) // self.hop_length))
        
        # Window function (Hanning)
        window = 0.5 - 0.5 * np.cos(2 * np.pi * np.arange(self.n_fft) / (self.n_fft - 1))
        
        frames_spec = []
        for i in range(n_frames):
            start = i * self.hop_length
            segment = signal[start : start + self.n_fft]
            if len(segment) < self.n_fft:
                segment = np.pad(segment, (0, self.n_fft - len(segment)), mode='constant')
            
            # FFT
            fft_mag = np.abs(np.fft.rfft(segment * window))
            
            # Bin into n_mels energy bands
            band_size = max(1, len(fft_mag) // self.n_mels)
            mels = [float(np.mean(fft_mag[b * band_size : (b + 1) * band_size])) for b in range(self.n_mels)]
            frames_spec.append(mels)

        spec = np.array(frames_spec, dtype=np.float32)
        
        # Pad or trim to fixed max_frames
        if len(spec) < max_frames:
            pad_width = ((0, max_frames - len(spec)), (0, 0))
            spec = np.pad(spec, pad_width, mode='constant')
        else:
            spec = spec[:max_frames]

        # Log-scale normalization
        spec = np.log1p(np.maximum(spec, 0.0))
        mean = np.mean(spec)
        std = np.std(spec) + 1e-6
        return (spec - mean) / std


class SimpleVocabulary:
    """Lightweight subword/word tokenizer and vocabulary mapping."""
    def __init__(self, vocab_path: Optional[str] = None):
        self.word2id = {"<pad>": 0, "<unk>": 1, "<cls>": 2, "<sep>": 3}
        self.id2word = {0: "<pad>", 1: "<unk>", 2: "<cls>", 3: "<sep>"}
        if vocab_path and os.path.exists(vocab_path):
            self.load(vocab_path)

    def fit_on_texts(self, texts: List[str], max_vocab: int = 5000):
        for text in texts:
            words = text.lower().replace(".", " ").replace(",", " ").replace("!", " ").replace("?", " ").split()
            for w in words:
                if w not in self.word2id and len(self.word2id) < max_vocab:
                    idx = len(self.word2id)
                    self.word2id[w] = idx
                    self.id2word[idx] = w

    def encode(self, text: str, max_len: int = 64) -> List[int]:
        words = text.lower().replace(".", " ").replace(",", " ").replace("!", " ").replace("?", " ").split()
        tokens = [2]  # <cls>
        for w in words:
            tokens.append(self.word2id.get(w, 1))
            if len(tokens) >= max_len - 1:
                break
        tokens.append(3)  # <sep>
        if len(tokens) < max_len:
            tokens += [0] * (max_len - len(tokens))
        return tokens[:max_len]

    def save(self, path: str):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.word2id, f, ensure_ascii=False, indent=2)

    def load(self, path: str):
        with open(path, "r", encoding="utf-8") as f:
            self.word2id = json.load(f)
            self.id2word = {v: k for k, v in self.word2id.items()}


class PositionalEncoding(nn.Module):
    """Sinusoidal Positional Encoding for Sequence Transformers."""
    def __init__(self, d_model: int, max_len: int = 512):
        super().__init__()
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        self.register_buffer("pe", pe.unsqueeze(0))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: (batch_size, seq_len, d_model)
        return x + self.pe[:, : x.size(1), :]


class CrossAttentionBlock(nn.Module):
    """
    Multimodal Cross-Attention Layer:
    Queries: Derived from Transcribed Text sequence
    Keys & Values: Derived from Acoustic Audio Spectrogram frames
    Allows the model to attend to speech pitch, stress, and acoustic cues for each phrase.
    """
    def __init__(self, d_model: int, n_heads: int = 4, dropout: float = 0.1):
        super().__init__()
        self.cross_mha = nn.MultiheadAttention(embed_dim=d_model, num_heads=n_heads, dropout=dropout, batch_first=True)
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        
        # Position-wise Feed-Forward Network
        self.ffn = nn.Sequential(
            nn.Linear(d_model, d_model * 2),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(d_model * 2, d_model),
            nn.Dropout(dropout),
        )

    def forward(self, text_emb: torch.Tensor, audio_emb: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        # text_emb: Q, audio_emb: K, V
        attn_out, attn_weights = self.cross_mha(query=text_emb, key=audio_emb, value=audio_emb)
        x = self.norm1(text_emb + attn_out)
        out = self.norm2(x + self.ffn(x))
        return out, attn_weights


class CrossAttentionTransformerModel(nn.Module):
    """
    Multimodal Cross-Attention Transformer for Threat & Fraud Voice Classification.
    Fuses transcribed text tokens with acoustic spectrogram features.
    
    Includes:
    - Text Token Embedding & Positional Encoding
    - Audio Feature 1D-Conv/Linear Projection & Positional Encoding
    - Cross-Attention Fusion Block
    - Self-Attention Context Refinement Block
    - Binary Threat Head (Threat vs Legitimate)
    - Multi-class Threat Type Head (Extortion, Impersonation, KYC Phishing, Customs/Police, Clean)
    """
    def __init__(
        self,
        vocab_size: int = 2500,
        audio_feat_dim: int = 40,
        d_model: int = 128,
        n_heads: int = 4,
        num_classes: int = 5,
        dropout: float = 0.1,
    ):
        super().__init__()
        self.d_model = d_model
        
        # Text Encoder
        self.text_embedding = nn.Embedding(vocab_size, d_model, padding_idx=0)
        self.text_pos = PositionalEncoding(d_model, max_len=128)
        
        # Audio Encoder
        self.audio_proj = nn.Sequential(
            nn.Linear(audio_feat_dim, d_model),
            nn.LayerNorm(d_model),
            nn.GELU(),
            nn.Dropout(dropout),
        )
        self.audio_pos = PositionalEncoding(d_model, max_len=256)
        
        # Multimodal Cross-Attention Block (Text attends to Audio)
        self.cross_attn = CrossAttentionBlock(d_model=d_model, n_heads=n_heads, dropout=dropout)
        
        # Multimodal Self-Attention Block (Self-refinement)
        self.self_attn = nn.MultiheadAttention(embed_dim=d_model, num_heads=n_heads, dropout=dropout, batch_first=True)
        self.self_norm = nn.LayerNorm(d_model)
        
        # Pooling & Classification Heads
        # Binary Threat Classification Head: [0 = Clean/Non-Threat, 1 = Threat Message]
        self.threat_binary_head = nn.Sequential(
            nn.Linear(d_model, 64),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(64, 2)
        )
        
        # Multi-class Threat Category Head:
        # [0: Clean, 1: Financial Extortion, 2: Emergency Impersonation, 3: Bank KYC Phishing, 4: Law Enforcement Intimidation]
        self.threat_category_head = nn.Sequential(
            nn.Linear(d_model, 64),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(64, num_classes)
        )
        
        # Urgency & Acoustic Tension Estimator
        self.urgency_head = nn.Sequential(
            nn.Linear(d_model, 32),
            nn.GELU(),
            nn.Linear(32, 1),
            nn.Sigmoid()
        )

    def forward(
        self,
        text_tokens: torch.Tensor,
        audio_features: torch.Tensor
    ) -> Dict[str, torch.Tensor]:
        """
        text_tokens: (batch_size, seq_len)
        audio_features: (batch_size, audio_frames, audio_feat_dim)
        """
        # 1. Text embedding + positional encoding
        t_emb = self.text_embedding(text_tokens) * math.sqrt(self.d_model)
        t_emb = self.text_pos(t_emb)
        
        # 2. Audio projection + positional encoding
        a_emb = self.audio_proj(audio_features)
        a_emb = self.audio_pos(a_emb)
        
        # 3. Cross-Attention: Text queries attend to Audio keys & values
        cross_out, attn_weights = self.cross_attn(t_emb, a_emb)
        
        # 4. Self-Attention refinement + Text Residual Skip Connection
        self_out, _ = self.self_attn(cross_out, cross_out, cross_out)
        fused = self.self_norm(cross_out + self_out + t_emb)

        
        # 5. Global representation (mean pooling over non-padded tokens)
        mask = (text_tokens != 0).unsqueeze(-1).float()
        pooled = (fused * mask).sum(dim=1) / (mask.sum(dim=1) + 1e-6)
        
        # 6. Prediction Heads
        binary_logits = self.threat_binary_head(pooled)
        category_logits = self.threat_category_head(pooled)
        urgency_score = self.urgency_head(pooled)
        
        return {
            "binary_logits": binary_logits,
            "category_logits": category_logits,
            "urgency_score": urgency_score,
            "attention_weights": attn_weights,
            "pooled_features": pooled
        }
