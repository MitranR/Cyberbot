import reflex as rx


def custom_shield_logo():
    """
    Inline SVG Shield Logo Mark for Cyber Fraud Shield (Dark Mode - Black & Dark Blue Theme).
    """
    return rx.html(
        """
        <svg width="36" height="40" viewBox="0 0 36 40" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M18 2L3 8V18C3 27.5 9.5 35.8 18 38C26.5 35.8 33 27.5 33 18V8L18 2Z" fill="#0F172A" stroke="#38BDF8" stroke-width="2.5" stroke-linejoin="round"/>
            <path d="M18 9L27 13.5V19.5C27 24.8 23.2 29.8 18 31.5C12.8 29.8 9 24.8 9 19.5V13.5L18 9Z" fill="#1E3A8A" opacity="0.9"/>
            <path d="M14 19.5L17 22.5L23 16.5" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        """
    )


def nav_link(label: str, href: str) -> rx.Component:
    """Helper for clean dark-theme navigation link."""
    return rx.link(
        rx.text(
            label,
            font_size="14px",
            font_weight="600",
            color="#E2E8F0",
            font_family="'Outfit', sans-serif",
            user_select="none",
        ),
        href=href,
        padding_x="14px",
        padding_y="8px",
        border_radius="6px",
        _hover={"background": "#1E293B", "color": "#38BDF8"},
        text_decoration="none",
    )


def mobile_nav_item(label: str, href: str, icon_name: str) -> rx.Component:
    """Helper for clean mobile menu item with icon and redirect."""
    return rx.menu.item(
        rx.hstack(
            rx.icon(icon_name, size=16, color="#38BDF8"),
            rx.text(
                label,
                font_size="13px",
                font_weight="600",
                color="#F1F5F9",
                font_family="'Outfit', sans-serif",
            ),
            spacing="2",
            align="center",
            width="100%",
        ),
        on_click=rx.redirect(href),
        cursor="pointer",
        padding="10px 14px",
        _hover={"background": "#1E293B"},
    )


def mobile_nav_menu() -> rx.Component:
    """Mobile Hamburger navigation dropdown menu for compact smartphone screens."""
    return rx.box(
        rx.menu.root(
            rx.menu.trigger(
                rx.button(
                    rx.icon("menu", size=22, color="#38BDF8"),
                    variant="surface",
                    color_scheme="blue",
                    size="2",
                    padding="8px 10px",
                    background="#0F172A",
                    border="1px solid rgba(56, 189, 248, 0.4)",
                    border_radius="8px",
                    cursor="pointer",
                    aria_label="Open navigation menu",
                    _hover={"background": "#1E293B", "box-shadow": "0 0 10px rgba(56, 189, 248, 0.4)"},
                ),
            ),
            rx.menu.content(
                mobile_nav_item("Home", "/", "house"),
                rx.menu.separator(),
                mobile_nav_item("Report Voice Fraud", "/scan", "mic"),
                rx.menu.separator(),
                mobile_nav_item("Volunteers", "/volunteers", "users"),
                rx.menu.separator(),
                mobile_nav_item("Help & Docs / FAQs", "/docs", "circle-help"),
                background="#0B132B",
                border="1px solid #1E293B",
                box_shadow="0 10px 30px rgba(0, 0, 0, 0.9)",
                border_radius="10px",
                padding="4px",
                min_width="220px",
            ),
        ),
        display={"initial": "flex", "md": "none"},
        align_items="center",
    )


def header() -> rx.Component:
    """
    Header Component with Black & Dark Blue theme styling, responsive mobile drawer,
    and adaptive alignment across all devices.
    """
    return rx.box(
        # Tier 1: Utility Strip (Pure Black background with Dark Blue accent border)
        rx.box(
            rx.box(
                rx.hstack(
                    rx.hstack(
                        rx.box(
                            width="6px",
                            height="6px",
                            border_radius="50%",
                            background="#38BDF8",
                            flex_shrink="0",
                        ),
                        rx.text(
                            "CYBER FRAUD SHIELD | AI-POWERED FRAUD INTELLIGENCE PORTAL",
                            font_size={"initial": "9.5px", "sm": "10.5px", "md": "11px"},
                            font_weight="700",
                            letter_spacing="0.08em",
                            color="#38BDF8",
                            font_family="'IBM Plex Mono', monospace",
                            user_select="none",
                            white_space="nowrap",
                            overflow="hidden",
                            text_overflow="ellipsis",
                        ),
                        spacing="2",
                        align="center",
                        width="100%",
                    ),
                    justify="start",
                    align="center",
                    height="32px",
                    width="100%",
                ),
                width="100%",
                max_width="1440px",
                margin_x="auto",
                padding_x={"initial": "12px", "sm": "24px", "md": "32px"},
            ),
            background="#030712",
            border_bottom="1px solid #1E293B",
            width="100%",
        ),
        
        # Tier 2: Main Navigation Bar (Dark Blue & Black background, Sticky)
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
                                    font_size={"initial": "16px", "sm": "18px", "md": "20px"},
                                    font_weight="800",
                                    color="#FFFFFF",
                                    font_family="'Space Grotesk', sans-serif",
                                    line_height="1.1",
                                    white_space="nowrap",
                                ),
                                rx.text(
                                    "Voice & Fraud Intelligence Platform",
                                    font_size={"initial": "9.5px", "sm": "10.5px", "md": "11px"},
                                    font_weight="600",
                                    color="#38BDF8",
                                    font_family="'Outfit', sans-serif",
                                    letter_spacing="0.02em",
                                    white_space="nowrap",
                                ),
                                spacing="0",
                                align="start",
                            ),
                            spacing={"initial": "2", "sm": "3"},
                            align="center",
                        ),
                        href="/",
                        text_decoration="none",
                    ),
                    
                    # Desktop Right Navigation Links (md and above)
                    rx.hstack(
                        nav_link("Home", "/"),
                        nav_link("Report Voice Fraud", "/scan"),
                        nav_link("Volunteers", "/volunteers"),
                        nav_link("Help & Docs / FAQs", "/docs"),
                        spacing="2",
                        align="center",
                        display={"initial": "none", "md": "flex"},
                    ),

                    # Mobile Hamburger Navigation Menu (below md)
                    mobile_nav_menu(),

                    justify="between",
                    align="center",
                    height="76px",
                    width="100%",
                ),
                width="100%",
                max_width="1440px",
                margin_x="auto",
                padding_x={"initial": "12px", "sm": "24px", "md": "32px"},
            ),
            background="#0B132B",
            border_bottom="1px solid #1E293B",
            box_shadow="0 4px 20px rgba(0, 0, 0, 0.5)",
            width="100%",
        ),
        position="sticky",
        top="0",
        z_index="50",
        width="100%",
    )
