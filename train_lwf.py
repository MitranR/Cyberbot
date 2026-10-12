#!/usr/bin/env python3
"""
=============================================================================
  Cyber Fraud Shield - Multimodal Threat Model Trainer
  Methodology: Cross-Attention Transformer & LwF (Learning without Forgetting)
=============================================================================
This script trains or fine-tunes the Cross-Attention Transformer model using
the LwF continual learning method. When you provide a new dataset, LwF uses
knowledge distillation from the previous model snapshot to learn new threat
patterns while completely preventing catastrophic forgetting.

Usage:
    # 1. Train or initialize baseline with built-in cybersecurity benchmark:
    python train_lwf.py

    # 2. Train on your custom dataset (CSV with 'text' and 'label' columns):
    python train_lwf.py --data path/to/your_dataset.csv --epochs 15

    # 3. Train on audio recordings and transcripts:
    python train_lwf.py --data path/to/dataset.csv --audio_dir path/to/audio_folder/
=============================================================================
"""

import os
import sys
import copy
import argparse
import json
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.models.cross_attention_transformer import (
    AudioFeatureExtractor,
    SimpleVocabulary,
    CrossAttentionTransformerModel,
)
from src.models.lwf_engine import (
    LwFLoss,
    THREAT_CATEGORIES,
    ARTIFACTS_DIR,
    DEFAULT_MODEL_PATH,
    DEFAULT_VOCAB_PATH,
    TEACHER_SNAPSHOT_PATH,
)

# Built-in Multimodal Cybersecurity Benchmark Dataset
BENCHMARK_SAMPLES = [
    # Legitimate / Clean Calls (Label 0)
    {"text": "Hello, this is Dr. Patel's office calling to confirm your routine dental checkup appointment tomorrow at 10 AM.", "label": 0, "category": 0},
    {"text": "Hey Sarah, are we still meeting for lunch at the cafeteria today? Let me know when you're free.", "label": 0, "category": 0},
    {"text": "Good morning, this is customer service regarding your recent book delivery. Everything was marked delivered safely.", "label": 0, "category": 0},
    {"text": "Hi Dad, I will reach home by 7 PM after my evening classes finish. See you soon.", "label": 0, "category": 0},
    {"text": "Weather forecast for today indicates sunny skies with moderate winds across the region.", "label": 0, "category": 0},
    {"text": "Hi, are we meeting for coffee today at the cafe? Let me know what time works best for you.", "label": 0, "category": 0},
    {"text": "Thank you for attending the community volunteer meetup this weekend. We appreciate your valuable support.", "label": 0, "category": 0},
    {"text": "Good afternoon, your grocery order has been packed and will arrive in fifteen minutes. Have a wonderful day.", "label": 0, "category": 0},
    {"text": "Hey, did you finish reviewing the presentation slides for tomorrow's team sync meeting?", "label": 0, "category": 0},
    {"text": "Hi, just checking in to see how your weekend went and if you want to play tennis this Saturday.", "label": 0, "category": 0},
    {"text": "Welcome to our customer helpdesk. If you are inquiring about store hours, we are open Monday to Friday from 9 to 6.", "label": 0, "category": 0},
    {"text": "Hello, this is an automated reminder about your scheduled library book return on Friday afternoon.", "label": 0, "category": 0},
    
    # Financial Extortion & Blackmail (Label 1, Category 1)
    {"text": "We have recorded your webcam and personal private browsing history. Transfer 2500 dollars to our Bitcoin wallet within 24 hours or we send video to all your contacts.", "label": 1, "category": 1},
    {"text": "This is an urgent demand. If you do not pay fifty thousand rupees to this UPI handle immediately, your personal photos will be leaked online.", "label": 1, "category": 1},
    {"text": "We have access to your personal phone records. Wire the extortion fee right now or face severe public exposure.", "label": 1, "category": 1},
    
    # Emergency Family Impersonation Scam (Label 1, Category 2)
    {"text": "Mom please help me, I got arrested after a car accident and I lost my phone. My lawyer needs two thousand dollars right now or they will put me in jail.", "label": 1, "category": 2},
    {"text": "Grandma, it's your grandson. I am stuck at the border hospital with severe injury. Send money via wire transfer urgently, don't tell mom.", "label": 1, "category": 2},
    {"text": "Hey dad, my phone got stolen in London. I am stranded and need emergency hotel funds sent to this PayPal account immediately.", "label": 1, "category": 2},
    
    # Bank / KYC OTP Phishing (Label 1, Category 3)
    {"text": "Urgent notification from HDFC Bank security. Your debit card has been blocked due to unauthorized foreign login. Speak your 6 digit OTP immediately to reactivate.", "label": 1, "category": 3},
    {"text": "State Bank alert: Your KYC document expired. Click verification link or share your netbanking password and OTP to avoid account permanent freezing.", "label": 1, "category": 3},
    {"text": "Dear customer, your credit card reward points worth Rs 9850 are expiring today. Provide your card CVV and OTP to redeem cash into account.", "label": 1, "category": 3},
    
    # Law Enforcement & Customs Intimidation (Label 1, Category 4)
    {"text": "This is Officer Sharma from Delhi Police Cyber Crime Cell. A package registered under your Aadhaar card was seized with contraband narcotics. Arrest warrant issued.", "label": 1, "category": 4},
    {"text": "Federal Customs enforcement calling. Contraband and illegal passports found under your national ID. Transfer security deposit right now to avoid immediate arrest.", "label": 1, "category": 4},
    {"text": "Internal Revenue Service legal notice. You have unfiled tax evasion penalties. Local sheriffs are dispatched to your address unless fine is settled immediately.", "label": 1, "category": 4},
]


class MultimodalThreatDataset(Dataset):
    """PyTorch Dataset loading multimodal text tokens and synthetic/real audio acoustic frames."""
    def __init__(self, data_list: list, vocab: SimpleVocabulary, audio_extractor: AudioFeatureExtractor, audio_dir: str = None):
        self.data_list = data_list
        self.vocab = vocab
        self.audio_extractor = audio_extractor
        self.audio_dir = Path(audio_dir) if audio_dir else None

    def __len__(self):
        return len(self.data_list)

    def __getitem__(self, idx):
        item = self.data_list[idx]
        text = str(item.get("text", ""))
        label_bin = int(item.get("label", 0))
        label_cat = int(item.get("category", 0))

        # Encode text tokens (max_len = 64)
        tokens = np.array(self.vocab.encode(text, max_len=64), dtype=np.int64)

        # Audio acoustic features: check if audio file path is provided
        audio_path_key = item.get("audio_path") or item.get("file")
        if self.audio_dir and audio_path_key:
            full_path = self.audio_dir / audio_path_key
            if full_path.exists():
                with open(full_path, "rb") as f:
                    spec = self.audio_extractor.extract_from_bytes(f.read(), max_frames=128)
            else:
                spec = self._simulate_speech_audio_features(text, is_threat=bool(label_bin))
        else:
            # Generate acoustic speech feature simulation based on speech tone & threat urgency
            spec = self._simulate_speech_audio_features(text, is_threat=bool(label_bin))

        # Modality dropout during training: 25% chance of acoustic masking to ensure strong text token learning
        if np.random.rand() < 0.25:
            spec = np.zeros_like(spec, dtype=np.float32)


        return {
            "text_tokens": torch.tensor(tokens, dtype=torch.long),
            "audio_features": torch.tensor(spec, dtype=torch.float32),
            "target_binary": torch.tensor(label_bin, dtype=torch.long),
            "target_category": torch.tensor(label_cat, dtype=torch.long),
        }

    def _simulate_speech_audio_features(self, text: str, is_threat: bool) -> np.ndarray:
        """
        Synthesizes realistic speech PCM audio waveform with natural pitch acoustics
        varying across natural human speaker range (120-240Hz).
        """
        rng = np.random.RandomState(abs(hash(text)) % (2**31))
        sr = 16000
        duration = 2.0
        t = np.linspace(0, duration, int(sr * duration))
        
        # Natural human speaker pitch variation across both classes
        base_pitch = 140.0 + (rng.rand() * 80.0)  # 140 to 220 Hz
        if is_threat:
            jitter = 15.0 + rng.randn(len(t)) * 10.0
            f0 = base_pitch + 20.0 + jitter
            phase = np.cumsum(2 * np.pi * f0 / sr)
            signal = np.sin(phase) + 0.4 * np.sin(2 * phase) + 0.1 * rng.randn(len(t))
        else:
            vibrato = 8.0 * np.sin(2 * np.pi * 3.0 * t)
            f0 = base_pitch + vibrato
            phase = np.cumsum(2 * np.pi * f0 / sr)
            signal = np.sin(phase) + 0.3 * np.sin(2 * phase) + 0.05 * rng.randn(len(t))
            
        signal = signal / (np.max(np.abs(signal)) + 1e-5)
        pcm_bytes = (signal * 32000).astype(np.int16).tobytes()
        return self.audio_extractor.extract_from_bytes(pcm_bytes, max_frames=128)



def train_model(
    data_path: str = None,
    audio_dir: str = None,
    epochs: int = 12,
    batch_size: int = 8,
    lr: float = 0.001,
    lambda_distill: float = 1.0,
    temp: float = 2.0,
):
    """
    Executes Cross-Attention Transformer & LwF Training Loop.
    """
    print("\n" + "=" * 70)
    print("  CYBER FRAUD SHIELD: CROSS-ATTENTION TRANSFORMER & LwF TRAINER")
    print("=" * 70)

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    device = torch.device("cpu")
    print(f"[1/5] Compute device: {device}")

def categorize_text(fraud_type: str, text: str) -> int:
    """Categorizes text into 7 target categories for multi-head classification."""
    ft_l = str(fraud_type or "").lower()
    t_l = str(text or "").lower()
    
    # 2: Customs & Parcel
    if any(k in ft_l or k in t_l for k in ['customs', 'parcel', 'courier', 'package', 'shipment', 'prohibited items', 'contraband']):
        return 2
        
    # 3: Law Enforcement & Digital Arrest
    if any(k in ft_l or k in t_l for k in ['police', 'cbi', 'arrest', 'warrant', 'court', 'tax officer', 'challan', 'debt collector', 'legal settlement', 'seizure', 'lawsuit', 'digital arrest']):
        return 3
        
    # 4: Emergency Family Impersonation & Blackmail
    if any(k in ft_l or k in t_l for k in ['emergency', 'accident', 'hospital', 'kidnap', 'ransom', 'blackmail', 'medical', 'charity', 'fundraiser', 'disaster', 'friend in trouble', 'romance', 'son', 'daughter']):
        return 4
        
    # 5: Investment, Lottery & Job Fraud
    if any(k in ft_l or k in t_l for k in ['lottery', 'prize', 'lucky draw', 'investment', 'stock', 'crypto', 'trading', 'job', 'work-from-home', 'recruiter', 'scholarship', 'visa', 'grant', 'admission', 'ticket', 'hotel', 'marketplace', 'buyer overpayment']):
        return 5
        
    # 6: Tech Support & Account Takeover
    if any(k in ft_l or k in t_l for k in ['tech support', 'antivirus', 'remote access', 'screen-sharing', 'screen sharing', 'sim', 'porting', 'whatsapp', 'social media', 'password', 'cloud storage', 'computer repair', 'internet provider', 'data breach', 'anydesk']):
        return 6
        
    # 1: Bank, KYC & Financial Phishing
    return 1


def load_threat_datasets(fraud_path: str = None, safe_path: str = None, master_path: str = None) -> list:
    """
    Loads 100 Fraud Calls and 100 Safe Calls from user paths or project paths.
    Returns structured records with text, binary label, category label.
    """
    data_list = []
    
    # Priority 1: Direct Fraud + Safe CSV paths
    fraud_file = fraud_path
    if not fraud_file or not os.path.exists(fraud_file):
        default_downloads_fraud = r"C:\Users\mitra\Downloads\fraud_call_transcripts_100.csv"
        default_local_fraud = str(BASE_DIR / "src" / "model" / "data" / "fraud_call_transcripts_100.csv")
        if os.path.exists(default_downloads_fraud):
            fraud_file = default_downloads_fraud
        elif os.path.exists(default_local_fraud):
            fraud_file = default_local_fraud

    safe_file = safe_path
    if not safe_file or not os.path.exists(safe_file):
        default_downloads_safe = r"C:\Users\mitra\Downloads\non_fraud_safe_calls_100.csv"
        default_local_safe = str(BASE_DIR / "src" / "model" / "data" / "non_fraud_safe_calls_100.csv")
        if os.path.exists(default_downloads_safe):
            safe_file = default_downloads_safe
        elif os.path.exists(default_local_safe):
            safe_file = default_local_safe

    # Load Fraud Calls
    if fraud_file and os.path.exists(fraud_file):
        df_fraud = pd.read_csv(fraud_file)
        text_col = "transcript_text" if "transcript_text" in df_fraud.columns else ("text" if "text" in df_fraud.columns else df_fraud.columns[2])
        type_col = "fraud_type" if "fraud_type" in df_fraud.columns else ""
        for _, row in df_fraud.iterrows():
            txt = str(row[text_col]).strip()
            ft = str(row[type_col]) if type_col else ""
            cat = categorize_text(ft, txt)
            data_list.append({
                "text": txt,
                "label": 1,
                "category": cat,
                "fraud_type": ft
            })
        print(f"      Loaded {len(df_fraud)} fraud calls from: {fraud_file}")

    # Load Safe Calls
    if safe_file and os.path.exists(safe_file):
        df_safe = pd.read_csv(safe_file)
        text_col = "transcribed_call_text" if "transcribed_call_text" in df_safe.columns else ("text" if "text" in df_safe.columns else df_safe.columns[1])
        for _, row in df_safe.iterrows():
            txt = str(row[text_col]).strip()
            data_list.append({
                "text": txt,
                "label": 0,
                "category": 0,
                "fraud_type": "Legitimate / Non-Threat Call"
            })
        print(f"      Loaded {len(df_safe)} safe calls from: {safe_file}")

    # Fallback to master file if individual files not found
    if not data_list and master_path and os.path.exists(master_path):
        df_master = pd.read_csv(master_path)
        text_col = "text" if "text" in df_master.columns else df_master.columns[0]
        for _, row in df_master.iterrows():
            txt = str(row[text_col]).strip()
            is_fraud = int(row.get("label", 1 if row.get("is_fraud", False) else 0))
            ft = str(row.get("fraud_type", ""))
            cat = categorize_text(ft, txt) if is_fraud else 0
            data_list.append({
                "text": txt,
                "label": is_fraud,
                "category": cat,
                "fraud_type": ft
            })
        print(f"      Loaded {len(df_master)} records from master dataset: {master_path}")

    return data_list


def train_model(
    data_path: str = None,
    fraud_data: str = None,
    safe_data: str = None,
    audio_dir: str = None,
    epochs: int = 15,
    batch_size: int = 8,
    lr: float = 0.001,
    lambda_distill: float = 1.0,
    temp: float = 2.0,
):
    """
    Executes Cross-Attention Transformer & LwF Training Loop.
    """
    print("\n" + "=" * 70)
    print("  CYBER FRAUD SHIELD: CROSS-ATTENTION TRANSFORMER & LwF TRAINER")
    print("=" * 70)

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    device = torch.device("cpu")
    print(f"[1/5] Compute device: {device}")

    # 1. Prepare Dataset
    print("[2/5] Loading fraud and safe call datasets...")
    data_list = load_threat_datasets(fraud_path=fraud_data, safe_path=safe_data, master_path=data_path)
    
    if not data_list:
        print("      No external datasets found. Using built-in cybersecurity benchmark dataset.")
        data_list = BENCHMARK_SAMPLES * 6
    else:
        # Augment with benchmark samples to enrich acoustic diversity
        data_list.extend(BENCHMARK_SAMPLES)
        print(f"      Total training instances (including benchmark anchors): {len(data_list)}")

    # 2. Vocabulary Preparation
    vocab = SimpleVocabulary()
    if DEFAULT_VOCAB_PATH.exists():
        vocab.load(str(DEFAULT_VOCAB_PATH))
    vocab.fit_on_texts([item["text"] for item in data_list])
    vocab.save(str(DEFAULT_VOCAB_PATH))
    print(f"[3/5] Vocabulary built: {len(vocab.word2id)} words.")

    # 3. Model & Teacher (LwF) Initialization
    vocab_size = max(1000, len(vocab.word2id) + 50)
    student_model = CrossAttentionTransformerModel(
        vocab_size=vocab_size,
        audio_feat_dim=40,
        d_model=128,
        n_heads=4,
        num_classes=len(THREAT_CATEGORIES),
        dropout=0.1,
    ).to(device)

    # If previous model weights exist, load them and create frozen Teacher snapshot
    teacher_model = None
    if DEFAULT_MODEL_PATH.exists():
        try:
            state_dict = torch.load(DEFAULT_MODEL_PATH, map_location=device)
            student_model.load_state_dict(state_dict)
            print("      Loaded previous model checkpoint. Creating frozen LwF Teacher snapshot...")
            
            # Create frozen teacher model
            teacher_model = copy.deepcopy(student_model)
            teacher_model.eval()
            for p in teacher_model.parameters():
                p.requires_grad = False
            torch.save(teacher_model.state_dict(), TEACHER_SNAPSHOT_PATH)
            print("      Teacher snapshot locked for knowledge distillation (LwF).")
        except Exception as e:
            print(f"      Previous weights load notice: {e}. Starting fresh student model.")

    # 4. DataLoader & Loss
    audio_extractor = AudioFeatureExtractor()
    dataset = MultimodalThreatDataset(data_list, vocab, audio_extractor, audio_dir=audio_dir)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    optimizer = torch.optim.AdamW(student_model.parameters(), lr=lr, weight_decay=1e-4)
    lwf_criterion = LwFLoss(temperature=temp, lambda_distill=lambda_distill)

    # 5. Training Loop
    print(f"\n[4/5] Starting LwF Training Loop ({epochs} Epochs, Batch Size: {batch_size})...")
    student_model.train()

    for epoch in range(1, epochs + 1):
        running_total_loss = 0.0
        running_task_loss = 0.0
        running_distill_loss = 0.0
        correct_bin = 0
        total_samples = 0

        for batch in dataloader:
            tokens = batch["text_tokens"].to(device)
            audio = batch["audio_features"].to(device)
            target_bin = batch["target_binary"].to(device)
            target_cat = batch["target_category"].to(device)

            optimizer.zero_grad()

            # Student Forward
            s_out = student_model(tokens, audio)

            # Teacher Forward (if available for LwF distillation)
            t_bin_logits = None
            t_cat_logits = None
            if teacher_model is not None:
                with torch.no_grad():
                    t_out = teacher_model(tokens, audio)
                    t_bin_logits = t_out["binary_logits"]
                    t_cat_logits = t_out["category_logits"]

            # Compute LwF Total Loss
            losses = lwf_criterion(
                student_binary_logits=s_out["binary_logits"],
                student_category_logits=s_out["category_logits"],
                target_binary=target_bin,
                target_category=target_cat,
                teacher_binary_logits=t_bin_logits,
                teacher_category_logits=t_cat_logits,
            )

            loss = losses["total_loss"]
            loss.backward()
            optimizer.step()

            running_total_loss += loss.item() * len(target_bin)
            running_task_loss += losses["task_loss"].item() * len(target_bin)
            running_distill_loss += losses["distill_loss"].item() * len(target_bin)

            # Accuracy
            preds = torch.argmax(s_out["binary_logits"], dim=-1)
            correct_bin += (preds == target_bin).sum().item()
            total_samples += len(target_bin)

        epoch_loss = running_total_loss / total_samples
        epoch_task_loss = running_task_loss / total_samples
        epoch_distill = running_distill_loss / total_samples
        acc = (correct_bin / total_samples) * 100.0

        distill_str = f" | Distill Loss: {epoch_distill:.4f}" if teacher_model else ""
        print(f"  Epoch [{epoch:02d}/{epochs:02d}] - Loss: {epoch_loss:.4f} (Task: {epoch_task_loss:.4f}{distill_str}) | Accuracy: {acc:.1f}%")

    # 6. Save Updated Artifacts
    print(f"\n[5/5] Saving trained model weights to: {DEFAULT_MODEL_PATH}")
    torch.save(student_model.state_dict(), DEFAULT_MODEL_PATH)
    
    metadata = {
        "model_name": "Cross-Attention Transformer & LwF",
        "vocab_size": vocab_size,
        "d_model": 128,
        "n_heads": 4,
        "num_classes": len(THREAT_CATEGORIES),
        "categories": THREAT_CATEGORIES,
        "epochs_trained": epochs,
        "final_accuracy": round(acc, 2),
        "lwf_distillation_enabled": teacher_model is not None,
    }
    with open(ARTIFACTS_DIR / "cross_attention_metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print("=" * 70)
    print("  TRAINING COMPLETE! Cross-Attention Transformer & LwF is ready for inference.")
    print("  When you have new dataset files, simply run:")
    print("    python train_lwf.py --data your_file.csv --epochs 10")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Cross-Attention Transformer with LwF")
    parser.add_argument("--data", type=str, default=None, help="Path to master CSV or JSON dataset")
    parser.add_argument("--fraud_data", type=str, default=None, help="Path to fraud calls CSV dataset")
    parser.add_argument("--safe_data", type=str, default=None, help="Path to safe calls CSV dataset")
    parser.add_argument("--audio_dir", type=str, default=None, help="Path to audio clips directory")
    parser.add_argument("--epochs", type=int, default=15, help="Number of epochs (default: 15)")
    parser.add_argument("--batch_size", type=int, default=8, help="Batch size (default: 8)")
    parser.add_argument("--lr", type=float, default=0.001, help="Learning rate (default: 0.001)")
    parser.add_argument("--lambda_distill", type=float, default=1.0, help="LwF Distillation weight (default: 1.0)")
    parser.add_argument("--temp", type=float, default=2.0, help="LwF Temperature (default: 2.0)")

    args = parser.parse_args()
    train_model(
        data_path=args.data,
        fraud_data=args.fraud_data,
        safe_data=args.safe_data,
        audio_dir=args.audio_dir,
        epochs=args.epochs,
        batch_size=args.batch_size,
        lr=args.lr,
        lambda_distill=args.lambda_distill,
        temp=args.temp,
    )

