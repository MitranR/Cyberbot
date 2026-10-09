import reflex as rx


def arch_card(title: str, subtitle: str, path_info: str, status: str, icon_name: str, color_accent: str = "#1B6E5B"):
    """Architecture component card with monospace status pill."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.icon(icon_name, size=22, color=color_accent),
                rx.box(
                    rx.text(status, font_size="10px", font_weight="700", color="#FFFFFF", font_family="'IBM Plex Mono', monospace"),
                    padding="3px 8px",
                    background=color_accent,
                    border_radius="4px",
                ),
                justify="between",
                align="center",
                width="100%",
            ),
            rx.heading(title, font_size="16px", font_weight="700", color="#0A1F2E", font_family="'Space Grotesk', sans-serif", margin_top="10px"),
            rx.text(subtitle, font_size="13px", color="#5A6E72", font_family="'Inter', sans-serif"),
            rx.divider(margin_y="8px"),
            rx.text(path_info, font_size="11px", color="#1B6E5B", font_family="'IBM Plex Mono', monospace"),
            spacing="1",
            align="start",
        ),
        padding="20px",
        background="#F7F9F8",
        border="1px solid #E2E8F0",
        border_radius="10px",
        height="100%",
    )


def architecture() -> rx.Component:
    """
    System Architecture & Model Transparency Component.
    """
    return rx.box(
        rx.box(
            rx.vstack(
                rx.vstack(
                    rx.text("TECHNICAL MODEL TRANSPARENCY", font_size="11px", font_weight="700", color="#1B6E5B", font_family="'IBM Plex Mono', monospace", letter_spacing="0.1em"),
                    rx.heading("System Architecture & Failover Stack", font_size="28px", font_weight="800", color="#0A1F2E", font_family="'Space Grotesk', sans-serif"),
                    rx.text("Direct Python module execution with multi-model Hugging Face failover.", font_size="15px", color="#5A6E72", font_family="'Inter', sans-serif"),
                    spacing="1",
                    align="center",
                    text_align="center",
                ),
                
                # Component Cards Grid
                rx.grid(
                    arch_card(
                        "Voice Spoof Agent",
                        "Primary AI classifier calling Hugging Face Inference API with fallback stack.",
                        "src/agents/speech_agent.py",
                        "Mitran14/speach-agent",
                        "mic",
                        "#1B6E5B",
                    ),
                    arch_card(
                        "Text Fraud Agent",
                        "Evaluates phishing tactics using TF-IDF + Logistic Regression and Groq Llama 3.3.",
                        "src/agents/text_agent.py",
                        "Llama-3.3-70B",
                        "file-text",
                        "#0F3D3E",
                    ),
                    arch_card(
                        "Idempotency DB Engine",
                        "Thread-safe SQLite database manager providing instant cached response hits.",
                        "src/database/db_manager.py",
                        "SQLite3 Active",
                        "database",
                        "#38BDF8",
                    ),
                    arch_card(
                        "Reflex Web Frontend",
                        "Institutional portal invoking agent event handlers directly in Python.",
                        "cyber_shield_reflex/",
                        "Reflex 0.9.7",
                        "layout-grid",
                        "#10B981",
                    ),
                    columns=rx.breakpoints(initial="1", sm="2", md="4"),
                    spacing="4",
                    margin_top="32px",
                    width="100%",
                ),
                
                # Model Failover Transparency Box
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.icon("layers", size=20, color="#1B6E5B"),
                            rx.heading("Hugging Face Automatic Failover Priority Chain", font_size="16px", font_weight="700", color="#0A1F2E", font_family="'Space Grotesk', sans-serif"),
                            spacing="2",
                            align="center",
                        ),
                        rx.hstack(
                            rx.text("1. Mitran14/speach-agent", font_size="12px", font_weight="700", color="#1B6E5B", font_family="'IBM Plex Mono', monospace"),
                            rx.text("→", color="#CBD5E1"),
                            rx.text("2. speechbrain/spkrec-ecapa-voxceleb", font_size="12px", color="#5A6E72", font_family="'IBM Plex Mono', monospace"),
                            rx.text("→", color="#CBD5E1"),
                            rx.text("3. facebook/wav2vec2-base-960h", font_size="12px", color="#5A6E72", font_family="'IBM Plex Mono', monospace"),
                            rx.text("→", color="#CBD5E1"),
                            rx.text("4. Built-in Acoustic FFT Evaluator", font_size="12px", color="#0A1F2E", font_family="'IBM Plex Mono', monospace"),
                            spacing="3",
                            wrap="wrap",
                            margin_top="8px",
                        ),
                        spacing="2",
                        align="start",
                    ),
                    padding="20px",
                    background="#FFFFFF",
                    border="1px solid #E2E8F0",
                    border_radius="10px",
                    margin_top="24px",
                    width="100%",
                ),
                spacing="4",
                align="center",
                padding_y="60px",
            ),
            width="100%",
            padding_x={"initial": "16px", "md": "48px"},
        ),
        background="#F7F9F8",
        border_bottom="1px solid #E2E8F0",
        id="architecture",
    )
