import reflex as rx


def pricing_tier_card(
    title: str,
    price: str,
    period: str,
    description: str,
    features: list[str],
    cta_text: str,
    cta_href: str,
    is_popular: bool = False,
) -> rx.Component:
    """Next.js SaaS Starter styled Pricing Tier Card Component."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.heading(
                        title,
                        font_size="18px",
                        font_weight="800",
                        color="#0A1F2E",
                        font_family="'Space Grotesk', sans-serif",
                    ),
                    rx.text(
                        description,
                        font_size="13px",
                        color="#64748B",
                        font_family="'Outfit', sans-serif",
                    ),
                    spacing="0",
                    align="start",
                ),
                rx.cond(
                    is_popular,
                    rx.box(
                        rx.text("POPULAR", font_size="10px", font_weight="800", color="#FFFFFF", font_family="'IBM Plex Mono', monospace"),
                        padding="4px 10px",
                        background="#1B6E5B",
                        border_radius="20px",
                    ),
                ),
                justify="between",
                align="start",
                width="100%",
            ),
            
            # Price Tag
            rx.hstack(
                rx.heading(
                    price,
                    font_size="36px",
                    font_weight="800",
                    color="#0A1F2E",
                    font_family="'Space Grotesk', sans-serif",
                ),
                rx.text(
                    period,
                    font_size="13px",
                    color="#64748B",
                    font_family="'Outfit', sans-serif",
                ),
                spacing="1",
                align="baseline",
                margin_y="12px",
            ),
            
            rx.divider(margin_y="8px", color="#E2E8F0"),
            
            # Feature List
            rx.vstack(
                *[
                    rx.hstack(
                        rx.icon("circle-check", size=16, color="#10B981"),
                        rx.text(
                            feat,
                            font_size="13px",
                            color="#334155",
                            font_family="'Outfit', sans-serif",
                        ),
                        spacing="2",
                        align="center",
                    )
                    for feat in features
                ],
                spacing="2",
                align="start",
                width="100%",
                margin_bottom="16px",
            ),
            
            rx.link(
                rx.button(
                    cta_text,
                    width="100%",
                    size="3",
                    background=rx.cond(is_popular, "#0A1F2E", "#F1F5F9"),
                    color=rx.cond(is_popular, "#FFFFFF", "#0F172A"),
                    font_weight="700",
                    font_family="'Space Grotesk', sans-serif",
                    border_radius="8px",
                    cursor="pointer",
                    _hover={"background": rx.cond(is_popular, "#1B6E5B", "#E2E8F0")},
                    transition="all 0.2s ease",
                ),
                href=cta_href,
                width="100%",
                text_decoration="none",
            ),
            spacing="2",
            align="start",
        ),
        padding="28px",
        background="#FFFFFF",
        border=rx.cond(is_popular, "2px solid #1B6E5B", "1px solid #E2E8F0"),
        border_radius="16px",
        box_shadow=rx.cond(is_popular, "0 12px 32px rgba(27, 110, 91, 0.15)", "0 4px 14px rgba(0,0,0,0.03)"),
        position="relative",
        height="100%",
    )


def pricing_tiers() -> rx.Component:
    """
    Next.js SaaS Starter Pricing & Coverage Tiers Component.
    """
    return rx.box(
        rx.box(
            rx.vstack(
                rx.vstack(
                    rx.text(
                        "PROTECTION COVERAGE & TIERS",
                        font_size="11px",
                        font_weight="800",
                        color="#1B6E5B",
                        font_family="'IBM Plex Mono', monospace",
                        letter_spacing="0.1em",
                    ),
                    rx.heading(
                        "Tailored Protection for Citizens & Institutions",
                        font_size={"initial": "26px", "sm": "34px", "md": "40px"},
                        font_weight="800",
                        color="#0A1F2E",
                        font_family="'Space Grotesk', sans-serif",
                        text_align="center",
                        margin_top="10px",
                    ),
                    rx.text(
                        "From free citizen emergency call verifications to high-throughput institutional API scanner integrations.",
                        font_size={"initial": "15px", "sm": "16px", "md": "17px"},
                        color="#64748B",
                        font_family="'Outfit', sans-serif",
                        text_align="center",
                        max_width="720px",
                    ),
                    spacing="2",
                    align="center",
                ),
                
                rx.grid(
                    pricing_tier_card(
                        "Citizen Shield",
                        "Free",
                        "/ forever",
                        "Complete protection for individual citizens & helpline callers.",
                        [
                            "Unlimited Voice Call Deepfake Audits",
                            "SMS Phishing & WhatsApp Link Scanner",
                            "Suspect UPI & Phone Number Lookup",
                            "24/7 AI Emergency Guidance Assistant",
                        ],
                        "Start Free Audit",
                        "/scan",
                        is_popular=False,
                    ),
                    pricing_tier_card(
                        "Institutional Pro",
                        "1930",
                        "/ helpline edition",
                        "Designed for Banks, Cyber Crime Cells & Financial Fraud Teams.",
                        [
                            "All Citizen Shield Features Included",
                            "High-Speed Parallel Multi-Agent Pipeline",
                            "Bulk Batch Call Recording Ingestion",
                            "Central Suspect Database Deduplication",
                            "Automated National Portal Case Reports",
                        ],
                        "Launch Pro Scanner",
                        "/scan",
                        is_popular=True,
                    ),
                    pricing_tier_card(
                        "Enterprise Threat Intelligence",
                        "Custom",
                        "/ enterprise",
                        "For Law Enforcement Agencies & Telecom Infrastructure.",
                        [
                            "Dedicated Private Cloud & On-Prem Deployment",
                            "Custom Regional Whisper Language Fine-tunes",
                            "Real-Time Telephony Stream Hook Integrations",
                            "24/7 Priority SLA & Dedicated AI Engineers",
                        ],
                        "Contact Engineering",
                        "/docs",
                        is_popular=False,
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
            margin_x="auto",
        ),
        background="#FFFFFF",
        border_bottom="1px solid #E2E8F0",
        width="100%",
    )
