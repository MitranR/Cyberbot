import reflex as rx
from cyber_shield_reflex.state import State


def suspect_verdict_card() -> rx.Component:
    """Renders verdict banner for suspect text intelligence analysis (Dark Theme)."""
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
                box_shadow="0 4px 20px rgba(217, 119, 6, 0.4)",
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
                background="#16A34A",
                border_radius="10px",
                box_shadow="0 4px 20px rgba(22, 163, 74, 0.4)",
                margin_bottom="20px",
                width="100%",
            ),
        ),
    )


def suspect_intelligence() -> rx.Component:
    """
    Suspect Intelligence Database & Text Agent Scanner Page (Dark Theme - Black, Dark Blue, White).
    """
    return rx.box(
        rx.box(
            rx.vstack(
                # Header Section
                rx.vstack(
                    rx.text("THREAT INTELLIGENCE ENGINE", font_size="11px", font_weight="700", color="#38BDF8", font_family="'IBM Plex Mono', monospace", letter_spacing="0.1em"),
                    rx.heading("Suspect Intelligence Database & Text Fraud Scanner", font_size="28px", font_weight="800", color="#FFFFFF", font_family="'Space Grotesk', sans-serif"),
                    rx.text("Query suspect phone numbers, phishing URLs, or analyze suspicious SMS and email messages using our Llama 3.3 threat prompt engine.", font_size="15px", color="#94A3B8", font_family="'Outfit', sans-serif"),
                    spacing="1",
                    align="start",
                    margin_bottom="24px",
                ),
                
                # Section 1: Interactive Scanner Box
                rx.box(
                    rx.vstack(
                        rx.heading("Query Threat Intelligence Database", font_size="18px", font_weight="700", color="#FFFFFF", font_family="'Space Grotesk', sans-serif"),
                        rx.text_area(
                            placeholder="Enter suspect phone number (+91-XXXXX), email address, URL link, or full SMS phishing message text...",
                            value=State.text_input,
                            on_change=State.set_text_input,  # type: ignore
                            height="120px",
                            width="100%",
                            background="#030712",
                            color="#FFFFFF",
                            border="1px solid #1E293B",
                            border_radius="8px",
                            font_size="14px",
                            font_family="'Outfit', sans-serif",
                            _focus={"border": "1px solid #38BDF8"},
                        ),
                        rx.hstack(
                            rx.button(
                                rx.hstack(
                                    rx.icon("search", size=16),
                                    rx.text("Run Threat Scan"),
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
                            rx.cond(
                                State.is_analyzing,
                                rx.hstack(
                                    rx.spinner(size="2", color="#38BDF8"),
                                    rx.text("Evaluating message against Llama 3.3 threat taxonomy & TF-IDF model...", font_size="13px", color="#38BDF8", font_family="'IBM Plex Mono', monospace"),
                                    spacing="2",
                                    align="center",
                                ),
                            ),
                            spacing="4",
                            align="center",
                            width="100%",
                        ),
                        spacing="3",
                        align="start",
                    ),
                    padding="24px",
                    background="#0F172A",
                    border="1px solid #1E293B",
                    border_radius="12px",
                    box_shadow="0 10px 30px rgba(0,0,0,0.5)",
                    width="100%",
                    margin_bottom="32px",
                ),
                
                # Render Scan Result
                rx.cond(
                    State.analysis_done,
                    rx.box(
                        suspect_verdict_card(),
                        rx.box(
                            rx.vstack(
                                rx.heading("Threat Assessment Analysis", font_size="16px", font_weight="700", color="#FFFFFF", font_family="'Space Grotesk', sans-serif"),
                                rx.hstack(
                                    rx.text("Scam Category:", font_size="14px", font_weight="600", color="#94A3B8"),
                                    rx.text(State.scam_type, font_size="14px", font_weight="700", color="#38BDF8"),
                                    spacing="2",
                                ),
                                rx.hstack(
                                    rx.text("Calculated Risk Score:", font_size="14px", font_weight="600", color="#94A3B8"),
                                    rx.text(f"{State.overall_voice_risk_score} / 100", font_size="15px", font_weight="800", color="#F87171", font_family="'IBM Plex Mono', monospace"),
                                    spacing="2",
                                ),
                                rx.divider(margin_y="8px", border_color="#334155"),
                                rx.text("Safety & Mitigation Protocol:", font_size="13px", font_weight="700", color="#FFFFFF"),
                                rx.text(State.actionable_advice, font_size="14px", color="#E2E8F0", font_family="'Outfit', sans-serif", line_height="1.6"),
                                spacing="2",
                                align="start",
                            ),
                            padding="20px",
                            background="#0F172A",
                            border="1px solid #1E293B",
                            border_radius="12px",
                            width="100%",
                            margin_bottom="32px",
                        ),
                    ),
                ),
                
                # Section 2: Known Threat Vector Playbooks Grid
                rx.vstack(
                    rx.heading("Known Cyber Fraud Vectors & Threat Categories", font_size="20px", font_weight="800", color="#FFFFFF", font_family="'Space Grotesk', sans-serif"),
                    rx.text("Recognized cyber crime tactics tracked in our database:", font_size="14px", color="#94A3B8"),
                    rx.grid(
                        rx.box(
                            rx.vstack(
                                rx.hstack(
                                    rx.icon("phone-off", size=22, color="#38BDF8"),
                                    rx.heading("Fake Police / Customs Arrest Scam", font_size="16px", font_weight="700", color="#FFFFFF"),
                                    justify="between",
                                    width="100%",
                                ),
                                rx.text("Callers impersonating CBI, ED, Telecom Authority, or Police claiming illegal packages or pending arrest warrants to coerce immediate wire transfers.", font_size="13px", color="#94A3B8"),
                                rx.text("Detection: Urgency & Authority Impersonation", font_size="11px", font_weight="700", color="#38BDF8", font_family="'IBM Plex Mono', monospace"),
                                spacing="2",
                            ),
                            padding="20px",
                            background="#0F172A",
                            border="1px solid #1E293B",
                            border_radius="10px",
                        ),
                        rx.box(
                            rx.vstack(
                                rx.hstack(
                                    rx.icon("credit-card", size=22, color="#38BDF8"),
                                    rx.heading("APK / Malicious App Phishing", font_size="16px", font_weight="700", color="#FFFFFF"),
                                    justify="between",
                                    width="100%",
                                ),
                                rx.text("SMS containing links to download fake banking or electricity bill updates via .APK files that install keyloggers and SMS forwarders on victim devices.", font_size="13px", color="#94A3B8"),
                                rx.text("Detection: Suspicious URL & Package Signature", font_size="11px", font_weight="700", color="#38BDF8", font_family="'IBM Plex Mono', monospace"),
                                spacing="2",
                            ),
                            padding="20px",
                            background="#0F172A",
                            border="1px solid #1E293B",
                            border_radius="10px",
                        ),
                        rx.box(
                            rx.vstack(
                                rx.hstack(
                                    rx.icon("laptop", size=22, color="#38BDF8"),
                                    rx.heading("Tech Support Remote Access", font_size="16px", font_weight="700", color="#FFFFFF"),
                                    justify="between",
                                    width="100%",
                                ),
                                rx.text("Popups and messages urging victims to call fake helpline numbers or install remote access software (AnyDesk, TeamViewer) under threat of malware.", font_size="13px", color="#94A3B8"),
                                rx.text("Detection: Authority Impersonation Classifier", font_size="11px", font_weight="700", color="#38BDF8", font_family="'IBM Plex Mono', monospace"),
                                spacing="2",
                            ),
                            padding="20px",
                            background="#0F172A",
                            border="1px solid #1E293B",
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
        background="linear-gradient(180deg, #0A0F1D 0%, #030712 100%)",
    )
