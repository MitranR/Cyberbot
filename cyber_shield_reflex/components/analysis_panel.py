import reflex as rx
from cyber_shield_reflex.state import State


def voice_analysis_report_card() -> rx.Component:
    """
    Unified Executive Voice Threat Intelligence Report Card.
    Streamlined single-card design with executive header banner, aligned 4-metric strip,
    actionable advisory, and the transcribed call script note positioned directly BELOW the report.
    """
    return rx.box(
        # 1. Executive Status Header Banner
        rx.box(
            rx.hstack(
                rx.icon(
                    rx.cond(
                        State.threat_verdict == "THREAT DETECTED",
                        "triangle-alert",
                        rx.cond(State.verdict == "UNCERTAIN", "circle-alert", "shield-check")
                    ),
                    size=26,
                    color="#FFFFFF"
                ),
                rx.vstack(
                    rx.hstack(
                        rx.heading(
                            rx.cond(
                                State.threat_verdict == "THREAT DETECTED",
                                "HIGH RISK: VOICE THREAT DETECTED",
                                rx.cond(State.verdict == "UNCERTAIN", "CAUTION: SUSPICIOUS CALL PATTERN", "SAFE: NO THREAT DETECTED (LEGITIMATE CALL)")
                            ),
                            font_size="17px",
                            font_weight="800",
                            color="#FFFFFF",
                            font_family="'Space Grotesk', sans-serif"
                        ),
                        rx.badge(
                            "Cross-Attention Transformer & LwF",
                            color_scheme=rx.cond(State.threat_verdict == "THREAT DETECTED", "red", rx.cond(State.verdict == "UNCERTAIN", "orange", "green")),
                            variant="solid",
                            size="1",
                        ),
                        spacing="2",
                        align="center",
                        wrap="wrap",
                    ),
                    rx.text(
                        f"Threat Probability: {State.threat_probability}%  •  Classification: {State.scam_type}  •  Severity: {State.threat_level}",
                        font_size="12.5px",
                        color="rgba(255,255,255,0.92)",
                        font_family="'IBM Plex Mono', monospace"
                    ),
                    spacing="1",
                    align="start",
                ),
                rx.spacer(),
                # Dismiss / Clear Report Button
                rx.button(
                    rx.hstack(
                        rx.icon("x", size=14),
                        rx.text("Clear Report", font_size="12px", font_weight="600"),
                        spacing="1",
                    ),
                    size="1",
                    variant="surface",
                    color_scheme="gray",
                    cursor="pointer",
                    on_click=State.clear_uploaded_file,
                    _hover={"background": "rgba(255,255,255,0.2)"},
                ),
                spacing="3",
                align="center",
                width="100%",
            ),
            padding="16px 20px",
            background=rx.cond(
                State.threat_verdict == "THREAT DETECTED",
                "linear-gradient(90deg, #DC2626 0%, #B91C1C 100%)",
                rx.cond(
                    State.verdict == "UNCERTAIN",
                    "linear-gradient(90deg, #D97706 0%, #B45309 100%)",
                    "linear-gradient(90deg, #16A34A 0%, #15803D 100%)"
                )
            ),
            border_radius="10px",
            box_shadow=rx.cond(
                State.threat_verdict == "THREAT DETECTED",
                "0 4px 18px rgba(220, 38, 38, 0.35)",
                "0 4px 18px rgba(22, 163, 74, 0.35)"
            ),
            width="100%",
            margin_bottom="16px",
        ),
        
        # 2. Clean Aligned Intelligence Metrics Grid (4 Aligned Metric Cards)
        rx.grid(
            # Metric 1: Threat Classification
            rx.box(
                rx.text("Threat Classification", font_size="11.5px", font_weight="600", color="#94A3B8", text_transform="uppercase", letter_spacing="0.5px"),
                rx.text(State.scam_type, font_size="14px", font_weight="700", color=rx.cond(State.threat_verdict == "THREAT DETECTED", "#F87171", "#34D399"), margin_top="4px"),
                padding="12px 14px",
                background="#0F172A",
                border="1px solid #1E293B",
                border_radius="8px",
            ),
            # Metric 2: Threat Probability
            rx.box(
                rx.text("Threat Probability", font_size="11.5px", font_weight="600", color="#94A3B8", text_transform="uppercase", letter_spacing="0.5px"),
                rx.text(f"{State.threat_probability}%", font_size="15px", font_weight="800", color=rx.cond(State.threat_probability > 50, "#F87171", "#34D399"), font_family="'IBM Plex Mono', monospace", margin_top="4px"),
                padding="12px 14px",
                background="#0F172A",
                border="1px solid #1E293B",
                border_radius="8px",
            ),
            # Metric 3: Cross-Attention Alignment
            rx.box(
                rx.text("Attention Alignment", font_size="11.5px", font_weight="600", color="#94A3B8", text_transform="uppercase", letter_spacing="0.5px"),
                rx.text(f"{State.cross_attention_alignment}%", font_size="15px", font_weight="800", color="#38BDF8", font_family="'IBM Plex Mono', monospace", margin_top="4px"),
                padding="12px 14px",
                background="#0F172A",
                border="1px solid #1E293B",
                border_radius="8px",
            ),
            # Metric 4: Combined Risk Score
            rx.box(
                rx.text("Combined Risk Score", font_size="11.5px", font_weight="600", color="#94A3B8", text_transform="uppercase", letter_spacing="0.5px"),
                rx.text(f"{State.overall_voice_risk_score} / 100", font_size="15px", font_weight="800", color=rx.cond(State.overall_voice_risk_score > 50, "#F87171", "#34D399"), font_family="'IBM Plex Mono', monospace", margin_top="4px"),
                padding="12px 14px",
                background="#0F172A",
                border="1px solid #1E293B",
                border_radius="8px",
            ),
            columns=rx.breakpoints(initial="1", sm="2", md="4"),
            spacing="3",
            width="100%",
            margin_bottom="16px",
        ),
        
        # 3. Actionable Advisory Card
        rx.box(
            rx.hstack(
                rx.icon(
                    rx.cond(State.threat_verdict == "THREAT DETECTED", "shield-alert", "shield-check"),
                    size=22,
                    color=rx.cond(State.threat_verdict == "THREAT DETECTED", "#EF4444", "#10B981")
                ),
                rx.vstack(
                    rx.text("Actionable Advisory & Protective Measures", font_size="12.5px", font_weight="700", color=rx.cond(State.threat_verdict == "THREAT DETECTED", "#FCA5A5", "#6EE7B7"), font_family="'Space Grotesk', sans-serif"),
                    rx.text(State.actionable_advice, font_size="13.5px", color="#E2E8F0", line_height="1.5", font_family="'Outfit', sans-serif"),
                    spacing="1",
                    align="start",
                    width="100%",
                ),
                spacing="3",
                align="start",
                width="100%",
            ),
            padding="14px 18px",
            background=rx.cond(State.threat_verdict == "THREAT DETECTED", "rgba(239, 68, 68, 0.08)", "rgba(16, 185, 129, 0.08)"),
            border=rx.cond(State.threat_verdict == "THREAT DETECTED", "1px solid rgba(239, 68, 68, 0.35)", "1px solid rgba(16, 185, 129, 0.35)"),
            border_radius="8px",
            width="100%",
            margin_bottom="16px",
        ),

        # 4. Transcribed Call Audio Note (Displayed BELOW the report as requested)
        rx.box(
            rx.hstack(
                rx.hstack(
                    rx.icon("notebook-pen", size=16, color="#38BDF8"),
                    rx.text("Transcribed Call Audio Note (Audio-to-Text Converted Script)", font_size="13px", font_weight="700", color="#38BDF8", font_family="'Space Grotesk', sans-serif"),
                    spacing="2",
                    align="center",
                ),
                rx.spacer(),
                rx.badge(
                    rx.cond(State.transcription_engine != "", State.transcription_engine, "Speech-to-Text Engine"),
                    color_scheme="blue",
                    variant="surface",
                    size="1"
                ),
                width="100%",
                align="center",
                margin_bottom="10px",
            ),
            rx.text(
                f'"{State.transcription}"',
                font_size="14px",
                color="#F1F5F9",
                font_style="italic",
                line_height="1.6",
                font_family="'Outfit', sans-serif"
            ),
            rx.box(
                rx.hstack(
                    rx.icon("info", size=13, color="#94A3B8"),
                    rx.text(
                        "Note: This audio recording was converted into text above and evaluated against the Cross-Attention Transformer & LwF continual learning model to produce the analysis report.",
                        font_size="11.5px",
                        color="#94A3B8",
                        font_family="'IBM Plex Mono', monospace"
                    ),
                    spacing="2",
                    align="center",
                ),
                margin_top="10px",
                padding_top="8px",
                border_top="1px solid rgba(56, 189, 248, 0.15)",
            ),
            padding="14px 18px",
            background="rgba(15, 23, 42, 0.9)",
            border_left="4px solid #38BDF8",
            border="1px solid rgba(56, 189, 248, 0.25)",
            border_radius="8px",
            width="100%",
        ),
        
        padding="22px 24px",
        background="#090E1A",
        border="1px solid #1E293B",
        border_radius="12px",
        box_shadow="0 10px 30px rgba(0,0,0,0.5)",
        margin_top="24px",
        width="100%",
    )


def text_analysis_report_card() -> rx.Component:
    """
    Unified Executive SMS & Text Scam Intelligence Report Card.
    Strictly isolated for SMS & Message Scan tab.
    """
    return rx.box(
        # 1. Executive Status Header Banner
        rx.box(
            rx.hstack(
                rx.icon(
                    rx.cond(
                        State.text_risk_score > 60,
                        "triangle-alert",
                        rx.cond(State.text_risk_score > 35, "circle-alert", "shield-check")
                    ),
                    size=26,
                    color="#FFFFFF"
                ),
                rx.vstack(
                    rx.hstack(
                        rx.heading(
                            rx.cond(
                                State.text_risk_score > 60,
                                "HIGH RISK: MALICIOUS SMS / MESSAGE THREAT",
                                rx.cond(State.text_risk_score > 35, "CAUTION: SUSPICIOUS MESSAGE PATTERN", "SAFE: NO PHISHING THREAT DETECTED (LEGITIMATE)")
                            ),
                            font_size="17px",
                            font_weight="800",
                            color="#FFFFFF",
                            font_family="'Space Grotesk', sans-serif"
                        ),
                        rx.badge(
                            "NLP Scam Classifier",
                            color_scheme=rx.cond(State.text_risk_score > 60, "red", rx.cond(State.text_risk_score > 35, "orange", "green")),
                            variant="solid",
                            size="1",
                        ),
                        spacing="2",
                        align="center",
                        wrap="wrap",
                    ),
                    rx.text(
                        f"Threat Probability: {State.text_threat_probability}%  •  Classification: {State.text_scam_type}  •  Severity: {State.text_threat_level}",
                        font_size="12.5px",
                        color="rgba(255,255,255,0.92)",
                        font_family="'IBM Plex Mono', monospace"
                    ),
                    spacing="1",
                    align="start",
                ),
                rx.spacer(),
                # Dismiss / Clear Report Button
                rx.button(
                    rx.hstack(
                        rx.icon("x", size=14),
                        rx.text("Clear Report", font_size="12px", font_weight="600"),
                        spacing="1",
                    ),
                    size="1",
                    variant="surface",
                    color_scheme="gray",
                    cursor="pointer",
                    on_click=State.clear_text_scan,
                    _hover={"background": "rgba(255,255,255,0.2)"},
                ),
                spacing="3",
                align="center",
                width="100%",
            ),
            padding="16px 20px",
            background=rx.cond(
                State.text_risk_score > 60,
                "linear-gradient(90deg, #DC2626 0%, #B91C1C 100%)",
                rx.cond(
                    State.text_risk_score > 35,
                    "linear-gradient(90deg, #D97706 0%, #B45309 100%)",
                    "linear-gradient(90deg, #16A34A 0%, #15803D 100%)"
                )
            ),
            border_radius="10px",
            box_shadow=rx.cond(
                State.text_risk_score > 60,
                "0 4px 18px rgba(220, 38, 38, 0.35)",
                "0 4px 18px rgba(22, 163, 74, 0.35)"
            ),
            width="100%",
            margin_bottom="16px",
        ),
        
        # 2. Clean Aligned Intelligence Metrics Grid
        rx.grid(
            # Metric 1: Threat Classification
            rx.box(
                rx.text("Threat Classification", font_size="11.5px", font_weight="600", color="#94A3B8", text_transform="uppercase", letter_spacing="0.5px"),
                rx.text(State.text_scam_type, font_size="14px", font_weight="700", color=rx.cond(State.text_risk_score > 35, "#F87171", "#34D399"), margin_top="4px"),
                padding="12px 14px",
                background="#0F172A",
                border="1px solid #1E293B",
                border_radius="8px",
            ),
            # Metric 2: Threat Probability
            rx.box(
                rx.text("Threat Probability", font_size="11.5px", font_weight="600", color="#94A3B8", text_transform="uppercase", letter_spacing="0.5px"),
                rx.text(f"{State.text_threat_probability}%", font_size="15px", font_weight="800", color=rx.cond(State.text_threat_probability > 35, "#F87171", "#34D399"), font_family="'IBM Plex Mono', monospace", margin_top="4px"),
                padding="12px 14px",
                background="#0F172A",
                border="1px solid #1E293B",
                border_radius="8px",
            ),
            # Metric 3: Severity Level
            rx.box(
                rx.text("Risk Severity", font_size="11.5px", font_weight="600", color="#94A3B8", text_transform="uppercase", letter_spacing="0.5px"),
                rx.text(State.text_threat_level, font_size="15px", font_weight="800", color=rx.cond(State.text_risk_score > 60, "#EF4444", rx.cond(State.text_risk_score > 35, "#F59E0B", "#10B981")), font_family="'IBM Plex Mono', monospace", margin_top="4px"),
                padding="12px 14px",
                background="#0F172A",
                border="1px solid #1E293B",
                border_radius="8px",
            ),
            # Metric 4: Scam Risk Score
            rx.box(
                rx.text("Scam Risk Score", font_size="11.5px", font_weight="600", color="#94A3B8", text_transform="uppercase", letter_spacing="0.5px"),
                rx.text(f"{State.text_risk_score} / 100", font_size="15px", font_weight="800", color=rx.cond(State.text_risk_score > 35, "#F87171", "#34D399"), font_family="'IBM Plex Mono', monospace", margin_top="4px"),
                padding="12px 14px",
                background="#0F172A",
                border="1px solid #1E293B",
                border_radius="8px",
            ),
            columns=rx.breakpoints(initial="1", sm="2", md="4"),
            spacing="3",
            width="100%",
            margin_bottom="16px",
        ),
        
        # 3. Actionable Advisory Card
        rx.box(
            rx.hstack(
                rx.icon(
                    rx.cond(State.text_risk_score > 35, "shield-alert", "shield-check"),
                    size=22,
                    color=rx.cond(State.text_risk_score > 35, "#EF4444", "#10B981")
                ),
                rx.vstack(
                    rx.text("Actionable Advisory & Protective Measures", font_size="12.5px", font_weight="700", color=rx.cond(State.text_risk_score > 35, "#FCA5A5", "#6EE7B7"), font_family="'Space Grotesk', sans-serif"),
                    rx.text(State.text_actionable_advice, font_size="13.5px", color="#E2E8F0", line_height="1.5", font_family="'Outfit', sans-serif"),
                    spacing="1",
                    align="start",
                    width="100%",
                ),
                spacing="3",
                align="start",
                width="100%",
            ),
            padding="14px 18px",
            background=rx.cond(State.text_risk_score > 35, "rgba(239, 68, 68, 0.08)", "rgba(16, 185, 129, 0.08)"),
            border=rx.cond(State.text_risk_score > 35, "1px solid rgba(239, 68, 68, 0.35)", "1px solid rgba(16, 185, 129, 0.35)"),
            border_radius="8px",
            width="100%",
            margin_bottom="16px",
        ),
        
        # 4. Scanned Message Content Note
        rx.box(
            rx.hstack(
                rx.hstack(
                    rx.icon("file-text", size=15, color="#38BDF8"),
                    rx.text("Scanned Message Content Note", font_size="12.5px", font_weight="700", color="#38BDF8", font_family="'Space Grotesk', sans-serif"),
                    spacing="2",
                    align="center",
                ),
                rx.spacer(),
                rx.badge("SMS & Text Scam Agent", color_scheme="blue", variant="surface", size="1"),
                width="100%",
                align="center",
                margin_bottom="8px",
            ),
            rx.text(
                f'"{State.text_scanned_content}"',
                font_size="13.5px",
                color="#F1F5F9",
                font_style="italic",
                line_height="1.6",
                font_family="'Outfit', sans-serif"
            ),
            padding="12px 16px",
            background="rgba(15, 23, 42, 0.85)",
            border_left="4px solid #38BDF8",
            border="1px solid rgba(56, 189, 248, 0.25)",
            border_radius="8px",
            width="100%",
        ),
        
        padding="22px 24px",
        background="#090E1A",
        border="1px solid #1E293B",
        border_radius="12px",
        box_shadow="0 10px 30px rgba(0,0,0,0.5)",
        margin_top="24px",
        width="100%",
    )


def upload_success_toast() -> rx.Component:
    """Floating Cyber Toast notification displaying upload success for 2-3 seconds."""
    return rx.cond(
        State.show_upload_toast,
        rx.box(
            rx.hstack(
                rx.box(
                    rx.icon("circle-check", size=24, color="#10B981"),
                    padding="8px",
                    background="rgba(16, 185, 129, 0.15)",
                    border_radius="50%",
                    border="1px solid rgba(16, 185, 129, 0.4)",
                ),
                rx.vstack(
                    rx.hstack(
                        rx.text("File Uploaded Successfully!", font_weight="700", font_size="15px", color="#FFFFFF"),
                        rx.badge("✓ Ready", color_scheme="green", variant="solid", size="1"),
                        spacing="2",
                        align="center",
                    ),
                    rx.text(State.upload_toast_message, font_size="12px", color="#94A3B8", font_family="'IBM Plex Mono', monospace"),
                    spacing="1",
                    align="start",
                ),
                rx.spacer(),
                rx.icon(
                    "x",
                    size=16,
                    color="#94A3B8",
                    cursor="pointer",
                    _hover={"color": "#FFFFFF"},
                    on_click=State.dismiss_upload_toast,
                ),
                spacing="3",
                align="center",
                width="100%",
            ),
            # Progress bar indicator
            rx.box(
                height="3px",
                width="100%",
                background="linear-gradient(90deg, #10B981 0%, #38BDF8 100%)",
                border_radius="2px",
                margin_top="10px",
            ),
            position="fixed",
            top="32px",
            right="32px",
            z_index="9999",
            background="#0F172A",
            border="1px solid #10B981",
            box_shadow="0 10px 30px -5px rgba(16, 185, 129, 0.4), 0 0 20px rgba(16, 185, 129, 0.25)",
            border_radius="12px",
            padding="16px 20px",
            min_width="340px",
            max_width="480px",
            transition="all 0.3s ease-in-out",
        ),
    )


def analysis_panel() -> rx.Component:
    """
    Live Voice & Content Fraud Scanner Component.
    Features strict separation between Voice & Audio Upload and SMS & Message Text tabs.
    """
    return rx.box(
        upload_success_toast(),
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
                    # ==========================================
                    # TAB 1: VOICE & AUDIO UPLOAD WIDGET
                    # ==========================================
                    rx.vstack(
                        rx.box(
                            rx.upload(
                                rx.cond(
                                    State.uploaded_filename != "",
                                    # State when a file has been selected/uploaded
                                    rx.vstack(
                                        rx.box(
                                            rx.icon("file-audio", size=48, color="#10B981"),
                                            padding="14px",
                                            background="rgba(16, 185, 129, 0.15)",
                                            border_radius="50%",
                                            border="2px solid #10B981",
                                        ),
                                        rx.heading("Audio File Uploaded Successfully!", font_size="17px", font_weight="700", color="#10B981"),
                                        rx.text(State.uploaded_filename, font_size="15px", font_weight="600", color="#FFFFFF", text_align="center"),
                                        rx.hstack(
                                            rx.badge(rx.cond(State.uploaded_file_size != "", State.uploaded_file_size, "Audio File"), color_scheme="blue", variant="surface"),
                                            rx.badge("✓ Ready for AI Analysis", color_scheme="green", variant="solid"),
                                            spacing="2",
                                            align="center",
                                        ),
                                        rx.text("Click or drop another audio file to change or replace", font_size="12px", color="#94A3B8"),
                                        spacing="2",
                                        align="center",
                                        padding="28px",
                                    ),
                                    # Default initial state when no file has been loaded
                                    rx.vstack(
                                        rx.icon("cloud-upload", size=42, color="#38BDF8"),
                                        rx.heading("Drag and drop audio file here, or click to browse", font_size="16px", font_weight="600", color="#FFFFFF"),
                                        rx.text("Supports WAV, MP3, M4A, AAC, OGG audio files up to 25MB", font_size="12px", color="#94A3B8", font_family="'IBM Plex Mono', monospace"),
                                        spacing="2",
                                        align="center",
                                        padding="36px",
                                    ),
                                ),
                                id="audio_upload",
                                accept={
                                    "audio/*": [".wav", ".mp3", ".m4a", ".aac", ".ogg", ".flac", ".opus"],
                                    "audio/wav": [".wav"],
                                    "audio/mpeg": [".mp3"],
                                    "audio/mp4": [".m4a"],
                                    "audio/x-m4a": [".m4a"],
                                    "audio/aac": [".aac"],
                                    "audio/ogg": [".ogg", ".opus"],
                                },
                                max_files=1,
                                on_drop=State.handle_file_upload(rx.upload_files(upload_id="audio_upload")),  # type: ignore
                                border=rx.cond(State.uploaded_filename != "", "2px solid #10B981", "2px dashed #38BDF8"),
                                box_shadow=rx.cond(State.uploaded_filename != "", "0 0 25px rgba(16, 185, 129, 0.25)", "none"),
                                border_radius="12px",
                                background=rx.cond(State.uploaded_filename != "", "rgba(16, 185, 129, 0.05)", "#0F172A"),
                                width="100%",
                                cursor="pointer",
                            ),
                            width="100%",
                        ),
                        
                        # Uploaded File Status Confirmation Card (With Remove button that clears audio & report)
                        rx.cond(
                            State.uploaded_filename != "",
                            rx.hstack(
                                rx.hstack(
                                    rx.box(
                                        rx.icon("music", size=22, color="#10B981"),
                                        padding="10px",
                                        background="rgba(16, 185, 129, 0.15)",
                                        border_radius="8px",
                                        border="1px solid rgba(16, 185, 129, 0.3)",
                                    ),
                                    rx.vstack(
                                        rx.hstack(
                                            rx.text(State.uploaded_filename, font_size="15px", font_weight="700", color="#FFFFFF"),
                                            rx.badge("✓ Upload Verified", color_scheme="green", variant="surface", font_weight="600"),
                                            spacing="2",
                                            align="center",
                                            wrap="wrap",
                                        ),
                                        rx.hstack(
                                            rx.text(
                                                rx.cond(State.uploaded_file_size != "", f"Size: {State.uploaded_file_size}", "Audio File"),
                                                font_size="12px",
                                                color="#94A3B8",
                                                font_family="'IBM Plex Mono', monospace",
                                            ),
                                            rx.text("• Ready for Deep Acoustic & Content Analysis", font_size="12px", color="#38BDF8", font_family="'IBM Plex Mono', monospace"),
                                            spacing="3",
                                        ),
                                        spacing="1",
                                        align="start",
                                    ),
                                    spacing="3",
                                    align="center",
                                ),
                                rx.spacer(),
                                rx.button(
                                    rx.hstack(
                                        rx.icon("trash-2", size=14),
                                        rx.text("Remove"),
                                        spacing="1",
                                    ),
                                    size="2",
                                    variant="surface",
                                    color_scheme="red",
                                    cursor="pointer",
                                    on_click=State.clear_uploaded_file,
                                ),
                                width="100%",
                                padding="14px 18px",
                                background="linear-gradient(90deg, rgba(16, 185, 129, 0.08) 0%, rgba(15, 23, 42, 0.9) 100%)",
                                border="1px solid rgba(16, 185, 129, 0.4)",
                                border_radius="10px",
                                align="center",
                                margin_top="12px",
                            ),
                        ),
                        
                        # Upload Trigger Button & Status Indicators
                        rx.hstack(
                            rx.button(
                                rx.hstack(
                                    rx.icon("play", size=16),
                                    rx.text("Analyze Uploaded File"),
                                    spacing="2",
                                ),
                                background=rx.cond(
                                    State.uploaded_filename != "",
                                    "linear-gradient(90deg, #10B981 0%, #1D4ED8 100%)",
                                    "#1D4ED8",
                                ),
                                color="#FFFFFF",
                                font_weight="700",
                                padding_x="24px",
                                padding_y="12px",
                                border_radius="8px",
                                on_click=State.handle_upload(rx.upload_files(upload_id="audio_upload")),  # type: ignore
                                cursor="pointer",
                                _hover={"opacity": 0.95, "transform": "scale(1.02)"},
                                transition="all 0.2s ease",
                            ),
                            rx.cond(
                                State.is_analyzing,
                                rx.hstack(
                                    rx.spinner(size="2", color="#38BDF8"),
                                    rx.text("Transcribing speech & analyzing via Cross-Attention Transformer & LwF...", font_size="13px", color="#38BDF8", font_family="'IBM Plex Mono', monospace"),
                                    spacing="2",
                                    align="center",
                                ),
                                rx.cond(
                                    State.uploaded_filename != "",
                                    rx.hstack(
                                        rx.icon("check-check", size=16, color="#10B981"),
                                        rx.text("Audio ready! Click Analyze to inspect spoofing & scam risk", font_size="13px", color="#10B981", font_family="'IBM Plex Mono', monospace"),
                                        spacing="2",
                                        align="center",
                                    ),
                                ),
                            ),
                            spacing="4",
                            align="center",
                            width="100%",
                            margin_top="16px",
                        ),
                        
                        # Quick Demonstration Test Buttons
                        rx.hstack(
                            rx.text("Test Scenarios:", font_size="12px", color="#94A3B8", font_weight="600"),
                            rx.button(
                                "Bank Scam Call",
                                size="1",
                                variant="surface",
                                color_scheme="red",
                                cursor="pointer",
                                on_click=State.run_sample_scan("bank_scam"),
                            ),
                            rx.button(
                                "AI Cloned Voice",
                                size="1",
                                variant="surface",
                                color_scheme="orange",
                                cursor="pointer",
                                on_click=State.run_sample_scan("cloned_voice"),
                            ),
                            rx.button(
                                "Legitimate Call",
                                size="1",
                                variant="surface",
                                color_scheme="green",
                                cursor="pointer",
                                on_click=State.run_sample_scan("natural_voice"),
                            ),
                            spacing="2",
                            align="center",
                            wrap="wrap",
                            margin_top="10px",
                        ),
                        
                        # Voice Analysis Report Card (Strictly nested inside Tab 1)
                        rx.cond(
                            State.voice_analysis_done,
                            voice_analysis_report_card(),
                        ),
                        width="100%",
                    ),
                    
                    # ==========================================
                    # TAB 2: SMS & MESSAGE TEXT SCAN WIDGET
                    # ==========================================
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
                            rx.button(
                                rx.hstack(
                                    rx.icon("trash-2", size=14),
                                    rx.text("Clear Message & Report"),
                                    spacing="1",
                                ),
                                size="2",
                                variant="surface",
                                color_scheme="red",
                                cursor="pointer",
                                on_click=State.clear_text_scan,
                            ),
                            spacing="3",
                            align="center",
                            width="100%",
                            margin_top="12px",
                        ),
                        
                        # Pre-configured sample test scenarios for SMS & Text
                        rx.hstack(
                            rx.text("Quick Test Scenarios:", font_size="12px", color="#94A3B8", font_weight="600"),
                            rx.button(
                                "Bank OTP Fraud",
                                size="1",
                                variant="surface",
                                color_scheme="red",
                                cursor="pointer",
                                on_click=State.run_sample_text_scan("bank_otp"),
                            ),
                            rx.button(
                                "Customs Package Seizure",
                                size="1",
                                variant="surface",
                                color_scheme="orange",
                                cursor="pointer",
                                on_click=State.run_sample_text_scan("delivery"),
                            ),
                            rx.button(
                                "Tech Support Scam",
                                size="1",
                                variant="surface",
                                color_scheme="yellow",
                                cursor="pointer",
                                on_click=State.run_sample_text_scan("tech_support"),
                            ),
                            spacing="2",
                            align="center",
                            wrap="wrap",
                            margin_top="10px",
                        ),
                        
                        # Text Analysis Report Card (Strictly nested inside Tab 2)
                        rx.cond(
                            State.text_analysis_done,
                            text_analysis_report_card(),
                        ),
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
