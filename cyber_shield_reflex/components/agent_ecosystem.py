import reflex as rx


def agent_card(
    agent_id: str,
    title: str,
    subtitle: str,
    tech_stack: str,
    description: str,
    capabilities: list[str],
    icon_name: str,
    accent_color: str = "#1B6E5B",
    badge_color: str = "rgba(27, 110, 91, 0.15)",
) -> rx.Component:
    """
    Sleek, modern glassmorphic card presenting a specialized AI Agent in the ecosystem.
    """
    return rx.box(
        rx.vstack(
            # Top Header Row: Icon + Agent Badge + ID
            rx.hstack(
                rx.hstack(
                    rx.box(
                        rx.icon(icon_name, size=22, color=accent_color),
                        padding="10px",
                        background=badge_color,
                        border_radius="10px",
                        border=f"1px solid {accent_color}33",
                    ),
                    rx.vstack(
                        rx.text(
                            agent_id,
                            font_size="10px",
                            font_weight="800",
                            color=accent_color,
                            font_family="'IBM Plex Mono', monospace",
                            letter_spacing="0.1em",
                        ),
                        rx.heading(
                            title,
                            font_size="17px",
                            font_weight="800",
                            color="#0A1F2E",
                            font_family="'Space Grotesk', sans-serif",
                            margin_top="0",
                        ),
                        spacing="0",
                        align="start",
                    ),
                    spacing="3",
                    align="center",
                ),
                rx.box(
                    rx.text(
                        tech_stack,
                        font_size="11px",
                        font_weight="700",
                        color=accent_color,
                        font_family="'IBM Plex Mono', monospace",
                    ),
                    padding="4px 10px",
                    background=badge_color,
                    border=f"1px solid {accent_color}40",
                    border_radius="20px",
                ),
                justify="between",
                align="center",
                width="100%",
            ),
            
            # Subtitle / Model Tag
            rx.text(
                subtitle,
                font_size="13px",
                font_weight="600",
                color="#5A6E72",
                font_family="'Outfit', sans-serif",
                margin_top="4px",
            ),
            
            # Agent Core Description
            rx.text(
                description,
                font_size="13px",
                color="#475569",
                font_family="'Outfit', sans-serif",
                line_height="1.5",
                margin_top="4px",
            ),
            
            rx.divider(margin_y="12px", color="#E2E8F0"),
            
            # Capabilities Checklist
            rx.vstack(
                *[
                    rx.hstack(
                        rx.icon("circle-check", size=15, color=accent_color),
                        rx.text(
                            cap,
                            font_size="12px",
                            font_weight="500",
                            color="#334155",
                            font_family="'Outfit', sans-serif",
                        ),
                        spacing="2",
                        align="center",
                    )
                    for cap in capabilities
                ],
                spacing="2",
                align="start",
                width="100%",
            ),
            spacing="1",
            align="start",
        ),
        padding="24px",
        background="#FFFFFF",
        border="1px solid #E2E8F0",
        border_radius="14px",
        box_shadow="0 4px 16px rgba(10, 31, 46, 0.04)",
        transition="all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
        _hover={
            "border_color": accent_color,
            "transform": "translateY(-4px)",
            "box_shadow": f"0 12px 28px rgba(15, 76, 58, 0.12)",
        },
        height="100%",
    )


def agent_ecosystem() -> rx.Component:
    """
    Landing Page Section: Multi-Agent Intelligence Ecosystem.
    Exposition of all specialized AI agents working together across the platform.
    """
    return rx.box(
        rx.box(
            rx.vstack(
                # Section Title & Subtitle Header
                rx.vstack(
                    rx.hstack(
                        rx.box(
                            width="6px",
                            height="6px",
                            border_radius="50%",
                            background="#10B981",
                        ),
                        rx.text(
                            "MULTI-AGENT INTELLIGENCE ARCHITECTURE",
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
                        "Autonomous Multi-Agent AI Defense Network",
                        font_size={"initial": "26px", "sm": "34px", "md": "40px"},
                        font_weight="800",
                        color="#0A1F2E",
                        font_family="'Space Grotesk', sans-serif",
                        text_align="center",
                        margin_top="10px",
                    ),
                    rx.text(
                        "Five specialized AI agents run in parallel to detect voice cloning, dissect SMS phishing, query suspect database registries, and guide citizens in real-time.",
                        font_size={"initial": "15px", "sm": "16px", "md": "17px"},
                        color="#5A6E72",
                        font_family="'Outfit', sans-serif",
                        text_align="center",
                        max_width="820px",
                        line_height="1.5",
                    ),
                    spacing="2",
                    align="center",
                ),
                
                # 5-Agent Grid Showcase
                rx.grid(
                    # Agent 1: Speech Analysis Agent
                    agent_card(
                        "AGENT 01",
                        "Speech Analysis Agent",
                        "Acoustic AI & Voice Spoof Classifier",
                        "HF Mitran14 + Groq Whisper",
                        "Analyzes raw call recordings and voice notes for synthetic frequency patterns, spectral centroid anomalies, and pitch micro-fluctuations.",
                        [
                            "Real-time spectral FFT acoustic waveform profiling",
                            "Pitch stability & phase coherence analysis",
                            "Groq Whisper v3 fast multilingual transcription",
                            "Synthetic confidence score % verdict generation",
                        ],
                        "mic",
                        accent_color="#0088FF",
                        badge_color="rgba(0, 136, 255, 0.08)",
                    ),
                    
                    # Agent 2: Text Scam & Phishing Agent
                    agent_card(
                        "AGENT 02",
                        "Text Scam & Phishing Agent",
                        "NLP Phishing & RAG Taxonomy Engine",
                        "Llama 3.3 70B + TF-IDF Model",
                        "Scans incoming SMS, WhatsApp messages, and email text for high-pressure urgency tactics, malicious banking URLs, and imposter prompts.",
                        [
                            "TF-IDF Logistic Regression scam classification",
                            "Llama 3.3 70B RAG fraud tactic breakdown",
                            "Malicious link & phishing URL risk scoring",
                            "Key warning sign & urgency pattern extraction",
                        ],
                        "message-square-warning",
                        accent_color="#10B981",
                        badge_color="rgba(16, 185, 129, 0.08)",
                    ),
                    
                    # Agent 3: Suspect Intelligence Agent
                    agent_card(
                        "AGENT 03",
                        "Suspect Intelligence Agent",
                        "Threat Registry & Idempotency Database",
                        "Thread-Safe Idempotent Engine",
                        "Queries central cybercrime database records for flagged UPI IDs, mobile numbers, and bank account handles to return instant risk scores.",
                        [
                            "UPI ID, phone number & bank account lookup",
                            "Multi-factor threat score calculation (0 - 100)",
                            "Idempotent hash caching for instant responses",
                            "Incident deduplication & suspect fraud history",
                        ],
                        "shield-alert",
                        accent_color="#F59E0B",
                        badge_color="rgba(245, 158, 11, 0.08)",
                    ),
                    
                    # Agent 4: Citizen Emergency AI Assistant
                    agent_card(
                        "AGENT 04",
                        "Citizen AI Assistant",
                        "24/7 Emergency Guidance Bot",
                        "RAG Knowledge Assistant",
                        "Interactive floating assistant providing citizens with step-by-step advice when targeted by scam calls, phishing links, or financial fraud.",
                        [
                            "Instant 24/7 scam triage & emergency advice",
                            "Step-by-step National Cyber Portal filing guidance",
                            "Bank account blocking & SIM swap action steps",
                            "Multi-language natural conversational responses",
                        ],
                        "bot",
                        accent_color="#8B5CF6",
                        badge_color="rgba(139, 92, 246, 0.08)",
                    ),
                    
                    # Agent 5: Multi-Agent Consensus Orchestrator
                    agent_card(
                        "AGENT 05",
                        "Consensus Orchestrator",
                        "Parallel Pipeline & Fusion Engine",
                        "Multi-Agent Fusion Model",
                        "Harmonizes output signals from Speech, Text, and Database agents to compute a unified threat verdict and institutional confidence score.",
                        [
                            "Parallel multi-modal agent invocation",
                            "Weighted threat verdict fusion algorithm",
                            "Sub-second end-to-end processing pipeline",
                            "Failover model switching on network latency",
                        ],
                        "cpu",
                        accent_color="#1B6E5B",
                        badge_color="rgba(27, 110, 91, 0.08)",
                    ),
                    columns=rx.breakpoints(initial="1", sm="2", md="3"),
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
        background="linear-gradient(180deg, #FFFFFF 0%, #F8FAFC 100%)",
        border_bottom="1px solid #E2E8F0",
        width="100%",
    )
