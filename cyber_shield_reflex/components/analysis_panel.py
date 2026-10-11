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
            background="#DC2626",
            border_radius="10px",
            box_shadow="0 4px 20px rgba(220, 38, 38, 0.4)",
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
                background="#D97706",
                border_radius="10px",
                box_shadow="0 4px 20px rgba(217, 119, 6, 0.4)",
                margin_bottom="20px",
                width="100%",
            ),
            # Default / GENUINE
            rx.box(
                rx.hstack(
                    rx.icon("shield-check", size=28, color="#FFFFFF"),
                    rx.vstack(
                        rx.heading("SAFE: NATURAL VOICE ACOUSTICS VERIFIED", font_size="18px", font_weight="800", color="#FFFFFF", font_family="'Space Grotesk', sans-serif"),
                        rx.text(f"Synthetic Voice Confidence: {State.synthetic_confidence}% | Threat Level: {State.threat_level}", font_size="13px", color="rgba(255,255,255,0.9)", font_family="'IBM Plex Mono', monospace"),
                        spacing="0",
                        align="start",
                    ),
                    spacing="3",
                    align="center",
                ),
                padding="20px 24px",
                background="#16A34A",
                border_radius="10px",
                box_shadow="0 4px 20px rgba(22, 163, 74, 0.4)",
                margin_bottom="20px",
                width="100%",
            ),
        ),
    )


def analysis_panel() -> rx.Component:
    """
    Live Voice & Content Fraud Scanner Component (Dark Theme - Black, Dark Blue, White).
    """
    return rx.box(
        rx.box(
            rx.vstack(
                rx.heading(
                    "Live Voice & Content Fraud Scanner",
                    font_size="28px",
                    font_weight="800",
                    color="#FFFFFF",
                    font_family="'Space Grotesk', sans-serif",
                ),
                rx.text(
                    "Upload call audio or test pre-loaded sample scenarios to trigger real-time AI voice spoofing and text fraud analysis.",
                    font_size="15px",
                    color="#94A3B8",
                    font_family="'Outfit', sans-serif",
                    margin_bottom="20px",
                ),
                
                # Tab Switcher: Voice Upload vs Text Input
                rx.hstack(
                    rx.button(
                        rx.hstack(rx.icon("mic", size=16), rx.text("Voice & Audio Upload"), spacing="2"),
                        size="2",
                        background=rx.cond(State.active_tab == "speech", "#1D4ED8", "#1E293B"),
                        color=rx.cond(State.active_tab == "speech", "#FFFFFF", "#94A3B8"),
                        font_weight="600",
                        on_click=State.set_active_tab("speech"),  # type: ignore
                        cursor="pointer",
                        border_radius="6px",
                    ),
                    rx.button(
                        rx.hstack(rx.icon("file-text", size=16), rx.text("SMS & Message Text"), spacing="2"),
                        size="2",
                        background=rx.cond(State.active_tab == "text", "#1D4ED8", "#1E293B"),
                        color=rx.cond(State.active_tab == "text", "#FFFFFF", "#94A3B8"),
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
                                    rx.icon("cloud-upload", size=42, color="#38BDF8"),
                                    rx.heading("Drag and drop audio file here, or click to browse", font_size="16px", font_weight="600", color="#FFFFFF"),
                                    rx.text("Supports WAV, MP3, M4A, AAC audio files up to 25MB", font_size="12px", color="#94A3B8", font_family="'IBM Plex Mono', monospace"),
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
                                border="2px dashed #38BDF8",
                                border_radius="12px",
                                background="#0F172A",
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
                                background="#1D4ED8",
                                color="#FFFFFF",
                                font_weight="700",
                                padding_x="24px",
                                padding_y="12px",
                                border_radius="8px",
                                on_click=State.handle_upload(rx.upload_files(upload_id="audio_upload")),  # type: ignore
                                cursor="pointer",
                                _hover={"background": "#1E40AF"},
                            ),
                            rx.cond(
                                State.is_analyzing,
                                rx.hstack(
                                    rx.spinner(size="2", color="#38BDF8"),
                                    rx.text("Extracting acoustic features & querying Hugging Face model...", font_size="13px", color="#38BDF8", font_family="'IBM Plex Mono', monospace"),
                                    spacing="2",
                                    align="center",
                                ),
                            ),
                            spacing="4",
                            align="center",
                            width="100%",
                            margin_top="16px",
                        ),
                        width="100%",
                    ),
                    
                    # Tab 2: Text Scam Analyzer
                    rx.vstack(
                        rx.text_area(
                            placeholder="Paste suspicious SMS, email, or WhatsApp message text here...",
                            value=State.text_input,
                            on_change=State.set_text_input,  # type: ignore
                            height="140px",
                            width="100%",
                            background="#0F172A",
                            color="#FFFFFF",
                            border="1px solid #1E293B",
                            border_radius="10px",
                            font_size="14px",
                            font_family="'Outfit', sans-serif",
                            _focus={"border": "1px solid #38BDF8"},
                        ),
                        rx.hstack(
                            rx.button(
                                rx.hstack(
                                    rx.icon("search", size=16),
                                    rx.text("Scan Message for Fraud"),
                                    spacing="2",
                                ),
                                background="#1D4ED8",
                                color="#FFFFFF",
                                font_weight="700",
                                padding_x="24px",
                                padding_y="12px",
                                border_radius="8px",
                                on_click=State.run_text_scan,  # type: ignore
                                cursor="pointer",
                                _hover={"background": "#1E40AF"},
                            ),
                            width="100%",
                            margin_top="12px",
                        ),
                        width="100%",
                    ),
                ),
                
                # Analysis Output Panel (Rendered if analysis_done is True)
                rx.cond(
                    State.analysis_done,
                    rx.box(
                        verdict_badge(),
                        rx.grid(
                            # Col 1: Audio Transcript & Content Analysis
                            rx.vstack(
                                rx.heading("Extracted Audio Transcript", font_size="16px", font_weight="700", color="#FFFFFF", font_family="'Space Grotesk', sans-serif"),
                                rx.box(
                                    rx.text(State.transcription, font_size="14px", color="#E2E8F0", font_family="'Outfit', sans-serif", line_height="1.6"),
                                    padding="16px",
                                    background="#1E293B",
                                    border_radius="8px",
                                    border="1px solid #334155",
                                    width="100%",
                                ),
                                spacing="2",
                                align="start",
                                width="100%",
                            ),
                            
                            # Col 2: Fraud Evaluation & Advisory
                            rx.vstack(
                                rx.heading("AI Fraud Intelligence Report", font_size="16px", font_weight="700", color="#FFFFFF", font_family="'Space Grotesk', sans-serif"),
                                rx.box(
                                    rx.vstack(
                                        rx.hstack(
                                            rx.text("Threat Classification:", font_size="13px", font_weight="600", color="#94A3B8"),
                                            rx.text(State.scam_type, font_size="13px", font_weight="700", color="#F87171"),
                                            justify="between",
                                            width="100%",
                                        ),
                                        rx.hstack(
                                            rx.text("Combined Risk Score:", font_size="13px", font_weight="600", color="#94A3B8"),
                                            rx.text(f"{State.overall_voice_risk_score} / 100", font_size="14px", font_weight="800", color="#F87171", font_family="'IBM Plex Mono', monospace"),
                                            justify="between",
                                            width="100%",
                                        ),
                                        rx.divider(margin_y="8px", border_color="#334155"),
                                        rx.text("Actionable Advisory:", font_size="12px", font_weight="700", color="#38BDF8"),
                                        rx.text(State.actionable_advice, font_size="13px", color="#E2E8F0", font_family="'Outfit', sans-serif"),
                                        spacing="2",
                                        align="start",
                                    ),
                                    padding="16px",
                                    background="#1E293B",
                                    border_radius="8px",
                                    border="1px solid #334155",
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
                        background="#0F172A",
                        border="1px solid #1E293B",
                        border_radius="12px",
                        box_shadow="0 10px 30px rgba(0,0,0,0.5)",
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
        background="linear-gradient(180deg, #0A0F1D 0%, #030712 100%)",
        border_bottom="1px solid #1E293B",
        id="analysis-panel",
    )
