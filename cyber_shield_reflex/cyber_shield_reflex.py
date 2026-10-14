import reflex as rx
from cyber_shield_reflex.components import (
    header,
    hero,
    animated_hero,
    agent_ecosystem,
    how_it_works,
    pricing_tiers,
    cta_banner,
    analysis_panel,
    architecture,
    footer,
    bot_agent,
    faq,
)


def index() -> rx.Component:
    """Home Landing Page Component with interactive animated Cyberbot motion hero."""
    return rx.box(
        header(),
        animated_hero(),
        footer(show_helpline_ribbon=False),
        bot_agent(),
        background="linear-gradient(180deg, #0A0F1D 0%, #030712 100%)",
        min_height="100vh",
        width="100%",
        max_width="100%",
        overflow_x="hidden",
        box_sizing="border-box",
        font_family="'Outfit', sans-serif",
        color="#FFFFFF",
    )


def scan_page() -> rx.Component:
    """Report Voice Fraud & Live Scanner Page."""
    return rx.box(
        header(),
        analysis_panel(),
        footer(show_helpline_ribbon=False),
        bot_agent(),
        background="linear-gradient(180deg, #0A0F1D 0%, #030712 100%)",
        min_height="100vh",
        width="100%",
        overflow_x="hidden",
        font_family="'Outfit', sans-serif",
        color="#FFFFFF",
    )




def volunteers_page() -> rx.Component:
    """Volunteers & Contributor Network Page."""
    return rx.box(
        header(),
        rx.box(
            rx.vstack(
                rx.heading("Volunteers & Contributor Community", font_size="32px", font_weight="800", color="#FFFFFF", font_family="'Space Grotesk', sans-serif"),
                rx.text("Join security researchers, data scientists, and developers building open-source AI fraud defense.", font_size="16px", color="#94A3B8"),
                padding_y="60px",
                align="start",
                width="100%",
            ),
            width="100%",
            padding_x={"initial": "16px", "md": "48px"},
            flex="1",
        ),
        footer(show_helpline_ribbon=False),
        bot_agent(),
        background="linear-gradient(180deg, #0A0F1D 0%, #030712 100%)",
        min_height="100vh",
        display="flex",
        flex_direction="column",
        justify_content="space-between",
        width="100%",
        overflow_x="hidden",
        font_family="'Outfit', sans-serif",
        color="#FFFFFF",
    )


def docs_page() -> rx.Component:
    """Dedicated Help & Official FAQs Page (Clean FAQ Accordion View)."""
    return rx.box(
        header(),
        faq(),
        footer(show_helpline_ribbon=True),
        bot_agent(),
        background="linear-gradient(180deg, #0A0F1D 0%, #030712 100%)",
        min_height="100vh",
        width="100%",
        overflow_x="hidden",
        font_family="'Outfit', sans-serif",
        color="#FFFFFF",
    )


# App configuration with custom Google Fonts and clean global dark styles
app = rx.App(
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@600;700;800&family=IBM+Plex Mono:wght@400;600;700&display=swap",
    ],
    style={
        "font_family": "'Outfit', sans-serif",
        "color": "#FFFFFF",
        "background_color": "#030712",
        "user_select": "none",
        "cursor": "default",
        "*, *::before, *::after": {
            "box_sizing": "border-box !important",
        },
        "html, body, #root, .radix-themes, .rt-Theme, .rt-Container": {
            "max_width": "100% !important",
            "width": "100% !important",
            "margin": "0",
            "padding": "0",
            "box_sizing": "border-box !important",
            "overflow_x": "hidden !important",
            "background_color": "#030712 !important",
            "color": "#FFFFFF !important",
        },
        "::selection": {
            "background": "#2563EB",
            "color": "#FFFFFF",
        },
    },
)

# Clean Page Routes
app.add_page(index, route="/", title="Cyber Fraud Shield | Home")
app.add_page(scan_page, route="/scan", title="Cyber Fraud Shield | Report & Scan")
app.add_page(volunteers_page, route="/volunteers", title="Cyber Fraud Shield | Volunteers")
app.add_page(docs_page, route="/docs", title="Cyber Fraud Shield | Help & FAQs")
