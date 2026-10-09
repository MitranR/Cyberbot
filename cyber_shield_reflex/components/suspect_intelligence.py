import reflex as rx
from cyber_shield_reflex.state import State


def suspect_verdict_card() -> rx.Component:
    """Renders verdict banner for suspect text intelligence analysis."""
    return rx.cond(
        State.verdict == "SPOOFED",
        rx.box(
            rx.hstack(
                rx.icon("triangle-alert", size=28, color="#FFFFFF"),
                rx.vstack(
                    rx.heading("CRITICAL PHISHING THREAT DETECTED", font_size="18px", font_weight="800", color="#FFFFFF", font_family="'Space Grotesk', sans-serif"),
                    rx.text(f"Fraud Risk Score: {State.overall_voice_risk_score}/100 | Threat Level: {State.threat_level} | Classification: {State.scam_type}", font_size="13px", color="rgba(255,255,255,0.9)", font_family="'IBM Plex Mono', monospace"),
                    spacing="0",
                    align="start",
                ),
                spacing="3",
                align="center",
            ),
            padding="20px 24px",
            background="#C4432E",
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
                        rx.heading("CAUTION: SUSPICIOUS COMMUNICATION PATTERN", font_size="18px", font_weight="800", color="#FFFFFF", font_family="'Space Grotesk', sans-serif"),
                        rx.text(f"Fraud Risk Score: {State.overall_voice_risk_score}/100 | Threat Level: {State.threat_level} | Classification: {State.scam_type}", font_size="13px", color="rgba(255,255,255,0.9)", font_family="'IBM Plex Mono', monospace"),
                        spacing="0",
                        align="start",
                    ),
                    spacing="3",
                    align="center",
                ),
                padding="20px 24px",
                background="#D97706",
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
                        rx.heading("VERIFIED: LEGITIMATE COMMUNICATION", font_size="18px", font_weight="800", color="#FFFFFF", font_family="'Space Grotesk', sans-serif"),
                        rx.text(f"Fraud Risk Score: {State.overall_voice_risk_score}/100 | Threat Level: {State.threat_level} | Classification: {State.scam_type}", font_size="13px", color="rgba(255,255,255,0.9)", font_family="'IBM Plex Mono', monospace"),
                        spacing="0",
                        align="start",
                    ),
                    spacing="3",
                    align="center",
                ),
                padding="20px 24px",
                background="#1B6E5B",
                border_radius="10px",
                box_shadow="0 4px 14px rgba(27, 110, 91, 0.25)",
                margin_bottom="20px",
                width="100%",
            ),
        ),
    )


def render_bullet_item(item: rx.Var[str]) -> rx.Component:
    return rx.hstack(
        rx.icon("circle-check", size=14, color="#1B6E5B"),
        rx.text(item, font_size="13px", color="#0D1B1E", font_family="'Outfit', sans-serif"),
        spacing="2",
        align="center",
    )


def suspect_intelligence() -> rx.Component:
    """
    Suspect Intelligence Component utilizing full features of TextScamDetectorAgent.
    Stretches edge-to-edge full width across the screen.
    """
    return rx.box(
        rx.box(
            rx.vstack(
                # Page Header Banner
                rx.vstack(
                    rx.hstack(
                        rx.icon("shield-alert", size=32, color="#1B6E5B"),
                        rx.vstack(
                            rx.heading(
                                "Suspect Intelligence & Text Scam Detector",
                                font_size="32px",
                                font_weight="800",
                                color="#0A1F2E",
                                font_family="'Space Grotesk', sans-serif",
                            ),
                            rx.text(
                                "Leverages Llama-3.3-70B, TF-IDF + Logistic Regression ML Classifier, and Heuristic Rule Engines to detect text fraud, phishing tactics, and fake sender signatures.",
                                font_size="16px",
                                color="#5A6E72",
                                font_family="'Outfit', sans-serif",
                            ),
                            spacing="1",
                            align="start",
                        ),
                        spacing="3",
                        align="center",
                    ),
                    width="100%",
                    margin_bottom="28px",
                ),
                
                # Interactive Text Agent Scanner Widget
                rx.box(
                    rx.vstack(
                        rx.heading("Analyze Suspicious Message or Transcript", font_size="18px", font_weight="700", color="#0A1F2E", font_family="'Space Grotesk', sans-serif"),
                        rx.text("Paste SMS, email text, call transcripts, or WhatsApp messages to extract scam patterns.", font_size="13px", color="#5A6E72"),
                        
                        rx.text_area(
                            placeholder="Paste suspect text message, SMS phishing alert, or email transcript here...",
                            value=State.text_input,
                            on_change=State.set_text_input,  # type: ignore
                            rows="4",
                            width="100%",
                            border="1px solid #CBD5E1",
                            border_radius="8px",
                            padding="14px",
                            font_family="'Outfit', sans-serif",
                            font_size="14px",
                        ),
                        
                        rx.hstack(
                            rx.button(
                                rx.hstack(rx.icon("search", size=18), rx.text("Run Text Fraud Analysis"), spacing="2"),
                                background="#1B6E5B",
                                color="#FFFFFF",
                                font_weight="700",
                                padding_x="28px",
                                padding_y="14px",
                                border_radius="8px",
                                on_click=State.run_text_scan,  # type: ignore
                                cursor="pointer",
                                _hover={"background": "#145C46"},
                            ),
                            spacing="4",
                            align="center",
                        ),
                        
                        # Pre-configured Suspect Test Scenarios
                        rx.box(
                            rx.vstack(
                                rx.text("INSTANT SUSPECT SCENARIO SAMPLES:", font_size="11px", font_weight="700", color="#5A6E72", font_family="'IBM Plex Mono', monospace"),
                                rx.hstack(
                                    rx.button(
                                        "🚨 Try Bank OTP Scam",
                                        size="2",
                                        variant="soft",
                                        color="#C4432E",
                                        background="rgba(196, 67, 46, 0.1)",
                                        border="1px solid rgba(196, 67, 46, 0.3)",
                                        on_click=State.run_suspect_text_sample("bank_otp"),  # type: ignore
                                        cursor="pointer",
                                    ),
                                    rx.button(
                                        "📦 Try Delivery Customs Fee",
                                        size="2",
                                        variant="soft",
                                        color="#D97706",
                                        background="rgba(217, 119, 6, 0.1)",
                                        border="1px solid rgba(217, 119, 6, 0.3)",
                                        on_click=State.run_suspect_text_sample("delivery"),  # type: ignore
                                        cursor="pointer",
                                    ),
                                    rx.button(
                                        "💻 Try Tech Support Remote Access",
                                        size="2",
                                        variant="soft",
                                        color="#1B6E5B",
                                        background="rgba(27, 110, 91, 0.1)",
                                        border="1px solid rgba(27, 110, 91, 0.3)",
                                        on_click=State.run_suspect_text_sample("tech_support"),  # type: ignore
                                        cursor="pointer",
                                    ),
                                    spacing="3",
                                    wrap="wrap",
                                ),
                                spacing="2",
                                align="start",
                            ),
                            margin_top="16px",
                            padding="16px",
                            background="#F7F9F8",
                            border_radius="8px",
                            width="100%",
                        ),
                        spacing="3",
                        align="start",
                        width="100%",
                    ),
                    padding="28px",
                    background="#FFFFFF",
                    border="1px solid #E2E8F0",
                    border_radius="12px",
                    box_shadow="0 4px 16px rgba(0,0,0,0.04)",
                    width="100%",
                    margin_bottom="32px",
                ),
                
                # Text Agent Analysis Results Output Card
                rx.cond(
                    State.analysis_done,
                    rx.box(
                        suspect_verdict_card(),
                        
                        rx.grid(
                            # Column 1: Threat Assessment & ML Model Metadata
                            rx.vstack(
                                rx.heading("Threat & ML Intelligence", font_size="16px", font_weight="700", color="#0A1F2E", font_family="'Space Grotesk', sans-serif"),
                                rx.box(
                                    rx.vstack(
                                        rx.hstack(
                                            rx.text("Classification Category:", font_size="13px", font_weight="600", color="#5A6E72"),
                                            rx.text(State.scam_type, font_size="14px", font_weight="700", color="#C4432E"),
                                            justify="between",
                                            width="100%",
                                        ),
                                        rx.hstack(
                                            rx.text("Risk Rating Score:", font_size="13px", font_weight="600", color="#5A6E72"),
                                            rx.text(f"{State.overall_voice_risk_score} / 100", font_size="15px", font_weight="800", color="#C4432E", font_family="'IBM Plex Mono', monospace"),
                                            justify="between",
                                            width="100%",
                                        ),
                                        rx.hstack(
                                            rx.text("Threat Level:", font_size="13px", font_weight="600", color="#5A6E72"),
                                            rx.text(State.threat_level, font_size="14px", font_weight="700", color="#D97706"),
                                            justify="between",
                                            width="100%",
                                        ),
                                        rx.hstack(
                                            rx.text("Detector Engine:", font_size="13px", font_weight="600", color="#5A6E72"),
                                            rx.text(State.engine_used, font_size="12px", color="#1B6E5B", font_family="'IBM Plex Mono', monospace"),
                                            justify="between",
                                            width="100%",
                                        ),
                                        spacing="3",
                                        align="start",
                                    ),
                                    padding="18px",
                                    background="#F7F9F8",
                                    border_radius="8px",
                                    border="1px solid #E2E8F0",
                                    width="100%",
                                ),
                                spacing="3",
                                align="start",
                                width="100%",
                            ),
                            
                            # Column 2: Matched Phishing Tactics & Red Flags
                            rx.vstack(
                                rx.heading("Matched Tactics & Key Red Flags", font_size="16px", font_weight="700", color="#0A1F2E", font_family="'Space Grotesk', sans-serif"),
                                rx.box(
                                    rx.vstack(
                                        rx.text("Identified Scam Tactics:", font_size="12px", font_weight="700", color="#0A1F2E"),
                                        rx.foreach(State.matched_tactics, render_bullet_item),
                                        rx.divider(margin_y="8px"),
                                        rx.text("Key Warning Indicators:", font_size="12px", font_weight="700", color="#0A1F2E"),
                                        rx.foreach(State.warning_signs, render_bullet_item),
                                        rx.divider(margin_y="8px"),
                                        rx.text("Recommended Action:", font_size="12px", font_weight="700", color="#0A1F2E"),
                                        rx.text(State.actionable_advice, font_size="13px", color="#0D1B1E", font_family="'Outfit', sans-serif"),
                                        spacing="2",
                                        align="start",
                                    ),
                                    padding="18px",
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
                        padding="28px",
                        background="#FFFFFF",
                        border="1px solid #E2E8F0",
                        border_radius="12px",
                        box_shadow="0 6px 20px rgba(0,0,0,0.06)",
                        margin_bottom="32px",
                        width="100%",
                    ),
                ),
                
                # Known Threat Vectors Grid
                rx.vstack(
                    rx.heading("Active Fraud Vectors & Threat Telemetry", font_size="22px", font_weight="700", color="#0A1F2E", font_family="'Space Grotesk', sans-serif"),
                    rx.grid(
                        rx.box(
                            rx.vstack(
                                rx.hstack(
                                    rx.icon("landmark", size=22, color="#C4432E"),
                                    rx.heading("Banking & KYC Impersonation", font_size="16px", font_weight="700", color="#0A1F2E"),
                                    justify="between",
                                    width="100%",
                                ),
                                rx.text("SMS phishing using artificial urgency, fake account block warnings, and unverified KYC web links to steal OTPs and login credentials.", font_size="13px", color="#5A6E72"),
                                rx.text("Detection: Text Agent TF-IDF + Groq Llama 3.3", font_size="11px", font_weight="700", color="#1B6E5B", font_family="'IBM Plex Mono', monospace"),
                                spacing="2",
                            ),
                            padding="20px",
                            background="#FFFFFF",
                            border="1px solid #E2E8F0",
                            border_radius="10px",
                        ),
                        rx.box(
                            rx.vstack(
                                rx.hstack(
                                    rx.icon("package", size=22, color="#D97706"),
                                    rx.heading("Courier Customs Fee Scam", font_size="16px", font_weight="700", color="#0A1F2E"),
                                    justify="between",
                                    width="100%",
                                ),
                                rx.text("Fake delivery notifications demanding small immediate payments (e.g. Rs 499) via malicious payment gateways to compromise credit cards.", font_size="13px", color="#5A6E72"),
                                rx.text("Detection: Link Pattern & Urgency Heuristic Engine", font_size="11px", font_weight="700", color="#1B6E5B", font_family="'IBM Plex Mono', monospace"),
                                spacing="2",
                            ),
                            padding="20px",
                            background="#FFFFFF",
                            border="1px solid #E2E8F0",
                            border_radius="10px",
                        ),
                        rx.box(
                            rx.vstack(
                                rx.hstack(
                                    rx.icon("laptop", size=22, color="#38BDF8"),
                                    rx.heading("Tech Support Remote Access", font_size="16px", font_weight="700", color="#0A1F2E"),
                                    justify="between",
                                    width="100%",
                                ),
                                rx.text("Popups and messages urging victims to call fake helpline numbers or install remote access software (AnyDesk, TeamViewer) under threat of malware.", font_size="13px", color="#5A6E72"),
                                rx.text("Detection: Authority Impersonation Classifier", font_size="11px", font_weight="700", color="#1B6E5B", font_family="'IBM Plex Mono', monospace"),
                                spacing="2",
                            ),
                            padding="20px",
                            background="#FFFFFF",
                            border="1px solid #E2E8F0",
                            border_radius="10px",
                        ),
                        columns=rx.breakpoints(initial="1", md="3"),
                        spacing="4",
                        width="100%",
                        margin_top="16px",
                    ),
                    width="100%",
                    align="start",
                    spacing="2",
                ),
                padding_y="40px",
                width="100%",
                align="start",
            ),
            width="100%",
            padding_x={"initial": "16px", "md": "48px"},
        ),
        width="100%",
        background="#F7F9F8",
    )
