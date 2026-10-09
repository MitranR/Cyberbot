import reflex as rx
from cyber_shield_reflex.state import State


def verdict_badge():
    """Renders the executive verdict card banner based on State.verdict."""
    return rx.cond(
        State.verdict == "SPOOFED",
        rx.box(
            rx.hstack(
                rx.icon("triangle-alert", size=28, color="#FFFFFF"),
                rx.vstack(
                    rx.heading("HIGH RISK: AI CLONED / SYNTHETIC VOICE DETECTED", font_size="18px", font_weight="800", color="#FFFFFF", font_family="'Space Grotesk', sans-serif"),
                    rx.text(f"Synthetic Voice Confidence: {State.synthetic_confidence}% | Threat Level: {State.threat_level}", font_size="13px", color="rgba(255,255,255,0.9)", font_family="'IBM Plex Mono', monospace"),
                    spacing="0",
                    align="start",
                ),
                spacing="3",
                align="center",
            ),
            padding="20px 24px",
            background="#C4432E",  # Muted brick-red for spoof alerts
            border_radius="10px",
            box_shadow="0 4px 14px rgba(196, 67, 46, 0.25)",
            margin_bottom="20px",
            width="100%",
        ),
        rx.cond(
            State.verdict == "UNCERTAIN",
            rx.box(
                rx.hstack(
                    rx.icon("circle-alert", size=28, color="#FFFFFF"),
                    rx.vstack(
                        rx.heading("CAUTION: SUSPICIOUS ACOUSTIC PATTERN", font_size="18px", font_weight="800", color="#FFFFFF", font_family="'Space Grotesk', sans-serif"),
                        rx.text(f"Synthetic Voice Confidence: {State.synthetic_confidence}% | Threat Level: {State.threat_level}", font_size="13px", color="rgba(255,255,255,0.9)", font_family="'IBM Plex Mono', monospace"),
                        spacing="0",
                        align="start",
                    ),
                    spacing="3",
                    align="center",
                ),
                padding="20px 24px",
                background="#D97706",  # Amber caution
                border_radius="10px",
                box_shadow="0 4px 14px rgba(217, 119, 6, 0.25)",
                margin_bottom="20px",
                width="100%",
            ),
            # Default / GENUINE
            rx.box(
                rx.hstack(
                    rx.icon("shield-check", size=28, color="#FFFFFF"),
                    rx.vstack(
                        rx.heading("VERIFIED: NATURAL HUMAN VOICE SIGNATURE", font_size="18px", font_weight="800", color="#FFFFFF", font_family="'Space Grotesk', sans-serif"),
                        rx.text(f"Synthetic Voice Confidence: {State.synthetic_confidence}% | Threat Level: {State.threat_level}", font_size="13px", color="rgba(255,255,255,0.9)", font_family="'IBM Plex Mono', monospace"),
                        spacing="0",
                        align="start",
                    ),
                    spacing="3",
                    align="center",
                ),
                padding="20px 24px",
                background="#1B6E5B",  # Deep teal-green
                border_radius="10px",
                box_shadow="0 4px 14px rgba(27, 110, 91, 0.25)",
                margin_bottom="20px",
                width="100%",
            ),
        ),
    )


def analysis_panel() -> rx.Component:
    """
    Live Analysis Panel Component.
    Upload widget, sample test triggers, and interactive verdict report cards.
    """
    return rx.box(
        rx.box(
            rx.vstack(
                rx.heading(
                    "Live Voice & Content Fraud Scanner",
                    font_size="28px",
                    font_weight="800",
                    color="#0A1F2E",
                    font_family="'Space Grotesk', sans-serif",
                ),
                rx.text(
                    "Upload call audio or test pre-loaded sample scenarios to trigger real-time AI voice spoofing and text fraud analysis.",
                    font_size="15px",
                    color="#5A6E72",
                    font_family="'Inter', sans-serif",
                    margin_bottom="20px",
                ),
                
                # Tab Switcher: Voice Upload vs Text Input
                rx.hstack(
                    rx.button(
                        rx.hstack(rx.icon("mic", size=16), rx.text("Voice & Audio Upload"), spacing="2"),
                        size="2",
                        background=rx.cond(State.active_tab == "speech", "#1B6E5B", "#E2E8F0"),
                        color=rx.cond(State.active_tab == "speech", "#FFFFFF", "#0D1B1E"),
                        font_weight="600",
                        on_click=State.set_active_tab("speech"),  # type: ignore
                        cursor="pointer",
                        border_radius="6px",
                    ),
                    rx.button(
                        rx.hstack(rx.icon("file-text", size=16), rx.text("SMS & Message Text"), spacing="2"),
                        size="2",
                        background=rx.cond(State.active_tab == "text", "#1B6E5B", "#E2E8F0"),
                        color=rx.cond(State.active_tab == "text", "#FFFFFF", "#0D1B1E"),
                        font_weight="600",
                        on_click=State.set_active_tab("text"),  # type: ignore
                        cursor="pointer",
                        border_radius="6px",
                    ),
                    spacing="3",
                    margin_bottom="20px",
                ),
                
                # Main Widget Body (Conditionally rendered by tab)
                rx.cond(
                    State.active_tab == "speech",
                    # Tab 1: Voice Upload Widget
                    rx.vstack(
                        rx.box(
                            rx.upload(
                                rx.vstack(
                                    rx.icon("cloud-upload", size=42, color="#1B6E5B"),
                                    rx.heading("Drag and drop audio file here, or click to browse", font_size="16px", font_weight="600", color="#0A1F2E"),
                                    rx.text("Supports WAV, MP3, M4A, AAC audio files up to 25MB", font_size="12px", color="#5A6E72", font_family="'IBM Plex Mono', monospace"),
                                    spacing="2",
                                    align="center",
                                    padding="36px",
                                ),
                                id="audio_upload",
                                accept={
                                    "audio/wav": [".wav"],
                                    "audio/mpeg": [".mp3"],
                                    "audio/x-m4a": [".m4a"],
                                },
                                max_files=1,
                                border="2px dashed #1B6E5B",
                                border_radius="12px",
                                background="#F7F9F8",
                                width="100%",
                            ),
                            width="100%",
                        ),
                        
                        # Upload Trigger Button
                        rx.hstack(
                            rx.button(
                                rx.hstack(
                                    rx.icon("play", size=16),
                                    rx.text("Analyze Uploaded File"),
                                    spacing="2",
                                ),
                                background="#1B6E5B",
                                color="#FFFFFF",
                                font_weight="700",
                                padding_x="24px",
                                padding_y="12px",
                                border_radius="8px",
                                on_click=State.handle_upload(rx.upload_files(upload_id="audio_upload")),  # type: ignore
                                cursor="pointer",
                                _hover={"background": "#145C46"},
                            ),
                            rx.cond(
                                State.is_analyzing,
                                rx.hstack(
                                    rx.spinner(size="2", color="#1B6E5B"),
                                    rx.text("Extracting acoustic features & querying Hugging Face model...", font_size="13px", color="#1B6E5B", font_family="'IBM Plex Mono', monospace"),
                                    spacing="2",
                                    align="center",
                                ),
                            ),
                            spacing="4",
                            align="center",
                            margin_y="16px",
                        ),
                        
                        # Quick Demo Sample Scenarios
                        rx.box(
                            rx.vstack(
                                rx.text("OR TEST INSTANT PRE-LOADED DEMO SAMPLES:", font_size="11px", font_weight="700", color="#5A6E72", font_family="'IBM Plex Mono', monospace", letter_spacing="0.05em"),
                                rx.hstack(
                                    rx.button(
                                        "🚨 Try Bank Emergency Scam",
                                        size="2",
                                        variant="soft",
                                        color="#C4432E",
                                        background="rgba(196, 67, 46, 0.1)",
                                        border="1px solid rgba(196, 67, 46, 0.3)",
                                        on_click=State.run_sample_scan("bank_scam"),  # type: ignore
                                        cursor="pointer",
                                    ),
                                    rx.button(
                                        "🤖 Try Cloned Voice Demo",
                                        size="2",
                                        variant="soft",
                                        color="#D97706",
                                        background="rgba(217, 119, 6, 0.1)",
                                        border="1px solid rgba(217, 119, 6, 0.3)",
                                        on_click=State.run_sample_scan("cloned_voice"),  # type: ignore
                                        cursor="pointer",
                                    ),
                                    rx.button(
                                        "✅ Try Normal Human Call",
                                        size="2",
                                        variant="soft",
                                        color="#1B6E5B",
                                        background="rgba(27, 110, 91, 0.1)",
                                        border="1px solid rgba(27, 110, 91, 0.3)",
                                        on_click=State.run_sample_scan("legit_call"),  # type: ignore
                                        cursor="pointer",
                                    ),
                                    spacing="3",
                                    wrap="wrap",
                                ),
                                spacing="2",
                                align="start",
                            ),
                            padding="16px",
                            background="#FFFFFF",
                            border="1px solid #E2E8F0",
                            border_radius="10px",
                            width="100%",
                        ),
                        width="100%",
                    ),
                    
                    # Tab 2: Text Scam Input Widget
                    rx.vstack(
                        rx.text_area(
                            placeholder="Paste suspicious SMS text, email, or message transcript here to analyze for phishing and fraud tactics...",
                            value=State.text_input,
                            on_change=State.set_text_input,  # type: ignore
                            rows="5",
                            width="100%",
                            border="1px solid #CBD5E1",
                            border_radius="8px",
                            padding="12px",
                            font_family="'Inter', sans-serif",
                        ),
                        rx.button(
                            rx.hstack(rx.icon("search", size=16), rx.text("Scan Message for Fraud"), spacing="2"),
                            background="#1B6E5B",
                            color="#FFFFFF",
                            font_weight="700",
                            padding_x="24px",
                            padding_y="12px",
                            border_radius="8px",
                            on_click=State.run_text_scan,  # type: ignore
                            cursor="pointer",
                            margin_top="12px",
                        ),
                        width="100%",
                    ),
                ),
                
                # Results Verdict Card (Visible when analysis_done is True)
                rx.cond(
                    State.analysis_done,
                    rx.box(
                        verdict_badge(),
                        
                        rx.grid(
                            # Column 1: Voice & Transcription Analysis
                            rx.vstack(
                                rx.heading("Acoustic & Model Metrics", font_size="16px", font_weight="700", color="#0A1F2E", font_family="'Space Grotesk', sans-serif"),
                                rx.box(
                                    rx.vstack(
                                        rx.hstack(
                                            rx.text("Voice Signature:", font_size="13px", font_weight="600", color="#5A6E72"),
                                            rx.text(State.voice_nature, font_size="13px", font_weight="700", color="#0A1F2E"),
                                            justify="between",
                                            width="100%",
                                        ),
                                        rx.hstack(
                                            rx.text("Pitch Stability:", font_size="13px", font_weight="600", color="#5A6E72"),
                                            rx.text(State.pitch_stability, font_size="13px", color="#0A1F2E"),
                                            justify="between",
                                            width="100%",
                                        ),
                                        rx.hstack(
                                            rx.text("Classifier Engine:", font_size="13px", font_weight="600", color="#5A6E72"),
                                            rx.text(State.spoof_engine, font_size="12px", color="#1B6E5B", font_family="'IBM Plex Mono', monospace"),
                                            justify="between",
                                            width="100%",
                                        ),
                                        rx.cond(
                                            State.idempotent_hit,
                                            rx.box(
                                                rx.text("⚡ Idempotency Cache Hit (Instant DB Retrieval)", font_size="11px", color="#10B981", font_family="'IBM Plex Mono', monospace"),
                                                padding="4px 8px",
                                                background="rgba(16, 185, 129, 0.1)",
                                                border_radius="4px",
                                            ),
                                        ),
                                        spacing="3",
                                        align="start",
                                    ),
                                    padding="16px",
                                    background="#F7F9F8",
                                    border_radius="8px",
                                    border="1px solid #E2E8F0",
                                    width="100%",
                                ),
                                
                                rx.heading("Whisper STT Transcription", font_size="16px", font_weight="700", color="#0A1F2E", font_family="'Space Grotesk', sans-serif", margin_top="12px"),
                                rx.box(
                                    rx.text(f'"{State.transcription}"', font_size="14px", font_style="italic", color="#0D1B1E", font_family="'Inter', sans-serif"),
                                    rx.text(f"Engine: {State.transcription_engine}", font_size="11px", color="#5A6E72", font_family="'IBM Plex Mono', monospace", margin_top="8px"),
                                    padding="16px",
                                    background="#FFFFFF",
                                    border="1px solid #CBD5E1",
                                    border_radius="8px",
                                    width="100%",
                                ),
                                spacing="3",
                                align="start",
                                width="100%",
                            ),
                            
                            # Column 2: Content Fraud & Emergency Guidance
                            rx.vstack(
                                rx.heading("Fraud Content Evaluation", font_size="16px", font_weight="700", color="#0A1F2E", font_family="'Space Grotesk', sans-serif"),
                                rx.box(
                                    rx.vstack(
                                        rx.hstack(
                                            rx.text("Threat Classification:", font_size="13px", font_weight="600", color="#5A6E72"),
                                            rx.text(State.scam_type, font_size="13px", font_weight="700", color="#C4432E"),
                                            justify="between",
                                            width="100%",
                                        ),
                                        rx.hstack(
                                            rx.text("Combined Risk Score:", font_size="13px", font_weight="600", color="#5A6E72"),
                                            rx.text(f"{State.overall_voice_risk_score} / 100", font_size="14px", font_weight="800", color="#C4432E", font_family="'IBM Plex Mono', monospace"),
                                            justify="between",
                                            width="100%",
                                        ),
                                        rx.divider(margin_y="8px"),
                                        rx.text("Actionable Advisory:", font_size="12px", font_weight="700", color="#0A1F2E"),
                                        rx.text(State.actionable_advice, font_size="13px", color="#0D1B1E", font_family="'Inter', sans-serif"),
                                        spacing="2",
                                        align="start",
                                    ),
                                    padding="16px",
                                    background="#F7F9F8",
                                    border_radius="8px",
                                    border="1px solid #E2E8F0",
                                    width="100%",
                                ),
                                spacing="3",
                                align="start",
                                width="100%",
                            ),
                            columns=rx.breakpoints(initial="1", md="2"),
                            spacing="5",
                            width="100%",
                        ),
                        padding="24px",
                        background="#FFFFFF",
                        border="1px solid #E2E8F0",
                        border_radius="12px",
                        box_shadow="0 6px 20px rgba(0,0,0,0.06)",
                        margin_top="24px",
                        width="100%",
                    ),
                ),
                spacing="4",
                align="start",
                padding_y="40px",
            ),
            width="100%",
            padding_x={"initial": "16px", "md": "48px"},
        ),
        background="#F7F9F8",
        border_bottom="1px solid #E2E8F0",
        id="analysis-panel",
    )
