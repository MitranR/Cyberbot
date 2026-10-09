import reflex as rx


def step_card(num: str, title: str, subtitle: str, icon_name: str, color_accent: str = "#1B6E5B"):
    """Sleek multi-modal pipeline step card with glowing step number."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.box(
                    rx.text(
                        f"STEP 0{num}",
                        font_size="11px",
                        font_weight="800",
                        color="#FFFFFF",
                        font_family="'IBM Plex Mono', monospace",
                        letter_spacing="0.08em",
                    ),
                    padding="5px 12px",
                    background=color_accent,
                    border_radius="6px",
                    box_shadow=f"0 2px 8px {color_accent}40",
                ),
                rx.icon(icon_name, size=24, color=color_accent),
                justify="between",
                align="center",
                width="100%",
            ),
            rx.heading(
                title,
                font_size="17px",
                font_weight="800",
                color="#0A1F2E",
                font_family="'Space Grotesk', sans-serif",
                margin_top="14px",
            ),
            rx.text(
                subtitle,
                font_size="13px",
                color="#5A6E72",
                font_family="'Outfit', sans-serif",
                line_height="1.5",
            ),
            spacing="2",
            align="start",
        ),
        padding="24px",
        background="#FFFFFF",
        border="1px solid #E2E8F0",
        border_radius="14px",
        box_shadow="0 4px 14px rgba(10, 31, 46, 0.03)",
        _hover={
            "border_color": color_accent,
            "transform": "translateY(-4px)",
            "box_shadow": f"0 10px 24px rgba(15, 76, 58, 0.1)",
        },
        transition="all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
        height="100%",
    )


def how_it_works() -> rx.Component:
    """
    End-to-End Multi-Modal Verification Pipeline Component.
    Explains the sub-second workflow across Voice, Text, and Suspect Database analysis.
    """
    return rx.box(
        rx.box(
            rx.vstack(
                rx.vstack(
                    rx.hstack(
                        rx.box(
                            width="6px",
                            height="6px",
                            border_radius="50%",
                            background="#38BDF8",
                        ),
                        rx.text(
                            "REAL-TIME VERIFICATION WORKFLOW",
                            font_size="11px",
                            font_weight="800",
                            color="#1B6E5B",
                            font_family="'IBM Plex Mono', monospace",
                            letter_spacing="0.1em",
                        ),
                        spacing="2",
                        align="center",
                        padding_x="12px",
                        padding_y="4px",
                        background="rgba(27, 110, 91, 0.08)",
                        border_radius="16px",
                    ),
                    rx.heading(
                        "End-to-End Multi-Modal Fraud Detection Flow",
                        font_size={"initial": "26px", "sm": "34px", "md": "40px"},
                        font_weight="800",
                        color="#0A1F2E",
                        font_family="'Space Grotesk', sans-serif",
                        text_align="center",
                        margin_top="10px",
                    ),
                    rx.text(
                        "From audio sample uploads to SMS phishing text analysis and suspect UPI lookups — our sub-second pipeline evaluates every incident thoroughly.",
                        font_size={"initial": "15px", "sm": "16px", "md": "17px"},
                        color="#5A6E72",
                        font_family="'Outfit', sans-serif",
                        text_align="center",
                        max_width="800px",
                    ),
                    spacing="2",
                    align="center",
                ),
                
                rx.grid(
                    step_card(
                        "1",
                        "Multi-Modal Ingestion",
                        "Accepts call audio files (.mp3, .wav), SMS phishing text clips, or suspect UPI IDs and mobile numbers into the execution queue.",
                        "cloud-upload",
                        color_accent="#0088FF",
                    ),
                    step_card(
                        "2",
                        "Feature & Signal Extraction",
                        "Performs acoustic FFT spectral profiling, pitch micro-fluctuation tracking, NLP tf-idf tokenization, and database index lookups.",
                        "activity",
                        color_accent="#10B981",
                    ),
                    step_card(
                        "3",
                        "Agent Consensus Evaluation",
                        "Runs Speech Agent, Llama 3.3 RAG Phishing Agent, and Threat Database lookup in parallel to generate a fused risk score.",
                        "cpu",
                        color_accent="#F59E0B",
                    ),
                    step_card(
                        "4",
                        "Executive Verdict & Playbook",
                        "Delivers an instant synthetic verdict (GENUINE / SPOOFED / UNCERTAIN), confidence %, key warning signs, and bank protection advice.",
                        "shield-check",
                        color_accent="#1B6E5B",
                    ),
                    columns=rx.breakpoints(initial="1", sm="2", md="4"),
                    spacing="5",
                    margin_top="36px",
                    width="100%",
                ),
                spacing="4",
                align="center",
                padding_y={"initial": "50px", "md": "70px"},
            ),
            width="100%",
            max_width="1200px",
            padding_x={"initial": "16px", "md": "32px"},
        ),
        background="#FFFFFF",
        border_bottom="1px solid #E2E8F0",
        width="100%",
    )
