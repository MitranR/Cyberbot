import reflex as rx


def custom_shield_logo():
    """
    Original inline SVG Shield Logo Mark for Cyber Fraud Shield.
    Designed with institutional trust aesthetic without using official government seals.
    """
    return rx.html(
        """
        <svg width="36" height="40" viewBox="0 0 36 40" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M18 2L3 8V18C3 27.5 9.5 35.8 18 38C26.5 35.8 33 27.5 33 18V8L18 2Z" fill="#0A1F2E" stroke="#1B6E5B" stroke-width="2.5" stroke-linejoin="round"/>
            <path d="M18 9L27 13.5V19.5C27 24.8 23.2 29.8 18 31.5C12.8 29.8 9 24.8 9 19.5V13.5L18 9Z" fill="#1B6E5B" opacity="0.85"/>
            <path d="M14 19.5L17 22.5L23 16.5" stroke="#F0F4F3" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        """
    )


def nav_link(label: str, href: str) -> rx.Component:
    """Helper for clean full-page navigation link."""
    return rx.link(
        rx.text(
            label,
            font_size="14px",
            font_weight="600",
            color="#0D1B1E",
            font_family="'Outfit', sans-serif",
            user_select="none",
        ),
        href=href,
        padding_x="14px",
        padding_y="8px",
        border_radius="6px",
        _hover={"background": "#F0F4F3", "color": "#1B6E5B"},
        text_decoration="none",
    )


def header() -> rx.Component:
    """
    Header Component with full-width responsive ribbon layout and clean navigation links.
    """
    return rx.box(
        # Tier 1: Utility Strip (Deep Green background)
        rx.box(
            rx.box(
                rx.hstack(
                    rx.hstack(
                        rx.box(
                            width="6px",
                            height="6px",
                            border_radius="50%",
                            background="#38BDF8",
                        ),
                        rx.text(
                            "CYBER FRAUD SHIELD | AI-POWERED FRAUD INTELLIGENCE PORTAL",
                            font_size="11px",
                            font_weight="700",
                            letter_spacing="0.08em",
                            color="#F0F4F3",
                            font_family="'IBM Plex Mono', monospace",
                            user_select="none",
                        ),
                        spacing="2",
                        align="center",
                    ),
                    justify="start",
                    align="center",
                    height="32px",
                ),
                width="100%",
                padding_x="32px",
            ),
            background="#0B3D2E",
            border_bottom="1px solid #145C46",
            width="100%",
        ),
        
        # Tier 2: Main Navigation Bar (White background, Sticky)
        rx.box(
            rx.box(
                rx.hstack(
                    # Left Logo + Wordmark (Clickable Home link)
                    rx.link(
                        rx.hstack(
                            custom_shield_logo(),
                            rx.vstack(
                                rx.heading(
                                    "Cyber Fraud Shield",
                                    font_size="20px",
                                    font_weight="800",
                                    color="#0A1F2E",
                                    font_family="'Space Grotesk', sans-serif",
                                    line_height="1.1",
                                ),
                                rx.text(
                                    "Voice & Fraud Intelligence Platform",
                                    font_size="11px",
                                    font_weight="600",
                                    color="#1B6E5B",
                                    font_family="'Outfit', sans-serif",
                                    letter_spacing="0.02em",
                                ),
                                spacing="0",
                                align="start",
                            ),
                            spacing="3",
                            align="center",
                        ),
                        href="/",
                        text_decoration="none",
                    ),
                    
                    # Right Navigation Links
                    rx.hstack(
                        nav_link("Home", "/"),
                        nav_link("Report Voice Fraud", "/scan"),
                        nav_link("Suspect Intelligence", "/suspect-intelligence"),
                        nav_link("Volunteers", "/volunteers"),
                        nav_link("Help & Docs / FAQs", "/docs"),
                        spacing="2",
                        align="center",
                        display={"initial": "none", "md": "flex"},
                    ),
                    justify="between",
                    align="center",
                    height="76px",
                ),
                width="100%",
                padding_x="32px",
            ),
            background="#FFFFFF",
            border_bottom="1px solid rgba(13, 27, 30, 0.08)",
            box_shadow="0 2px 8px rgba(10, 31, 46, 0.04)",
            width="100%",
        ),
        position="sticky",
        top="0",
        z_index="50",
        width="100%",
    )
