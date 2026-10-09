import reflex as rx


def cta_banner() -> rx.Component:
    """
    Next.js SaaS Starter Styled CTA Banner Component.
    """
    return rx.box(
        rx.box(
            rx.box(
                rx.vstack(
                    rx.heading(
                        "Ready to Protect Your Citizens & Organization?",
                        font_size={"initial": "26px", "sm": "34px", "md": "40px"},
                        font_weight="800",
                        color="#FFFFFF",
                        font_family="'Space Grotesk', sans-serif",
                        text_align="center",
                        line_height="1.15",
                    ),
                    rx.text(
                        "Analyze suspicious call recordings, scan text phishing links, or query suspect threat registries in sub-second real-time.",
                        font_size={"initial": "15px", "sm": "16px", "md": "18px"},
                        color="rgba(240, 244, 243, 0.85)",
                        font_family="'Outfit', sans-serif",
                        text_align="center",
                        max_width="720px",
                        margin_top="10px",
                    ),
                    rx.hstack(
                        rx.link(
                            rx.button(
                                rx.hstack(
                                    rx.icon("shield-alert", size=18),
                                    rx.text("Analyze a Call Now"),
                                    rx.icon("arrow-right", size=16),
                                    spacing="2",
                                ),
                                size="3",
                                background="#FFFFFF",
                                color="#0A1F2E",
                                font_weight="700",
                                font_family="'Space Grotesk', sans-serif",
                                padding_x="28px",
                                padding_y="22px",
                                border_radius="8px",
                                cursor="pointer",
                                _hover={"background": "#F0F4F3", "transform": "translateY(-2px)"},
                                transition="all 0.2s ease",
                            ),
                            href="/scan",
                            text_decoration="none",
                        ),
                        rx.link(
                            rx.button(
                                rx.hstack(
                                    rx.icon("file-text", size=18),
                                    rx.text("Help & FAQs"),
                                    spacing="2",
                                ),
                                size="3",
                                variant="outline",
                                color="#FFFFFF",
                                border="1px solid rgba(255, 255, 255, 0.3)",
                                font_weight="600",
                                font_family="'Space Grotesk', sans-serif",
                                padding_x="24px",
                                padding_y="22px",
                                border_radius="8px",
                                cursor="pointer",
                                _hover={"background": "rgba(255, 255, 255, 0.1)", "transform": "translateY(-2px)"},
                                transition="all 0.2s ease",
                            ),
                            href="/docs",
                            text_decoration="none",
                        ),
                        spacing="3",
                        align="center",
                        justify="center",
                        wrap="wrap",
                        margin_top="24px",
                    ),
                    spacing="3",
                    align="center",
                ),
                padding={"initial": "36px 20px", "sm": "48px 36px", "md": "60px 48px"},
                background="linear-gradient(135deg, #0A1F2E 0%, #0B3D2E 50%, #0F4C3A 100%)",
                border_radius="20px",
                border="1px solid rgba(56, 189, 248, 0.2)",
                box_shadow="0 20px 40px rgba(10, 31, 46, 0.15)",
                width="100%",
            ),
            width="100%",
            max_width="1200px",
            padding_x={"initial": "16px", "md": "32px"},
            padding_y={"initial": "40px", "md": "60px"},
            margin_x="auto",
        ),
        background="#F8FAFC",
        width="100%",
    )
