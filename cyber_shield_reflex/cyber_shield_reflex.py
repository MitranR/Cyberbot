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
    helpline_ribbon,
    bot_agent,
    faq,
    volunteers_content,
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
        max_width="100vw",
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
        max_width="100vw",
        overflow_x="hidden",
        box_sizing="border-box",
        font_family="'Outfit', sans-serif",
        color="#FFFFFF",
    )




def volunteers_page() -> rx.Component:
    """Volunteers & Contributor Network Page."""
    return rx.box(
        header(),
        rx.box(
            volunteers_content(),
            width="100%",
            padding_x={"initial": "12px", "sm": "24px", "md": "48px"},
            padding_y={"initial": "16px", "sm": "24px"},
            flex="1",
        ),
        helpline_ribbon(),
        footer(show_helpline_ribbon=False),
        bot_agent(),
        background="linear-gradient(180deg, #0A0F1D 0%, #030712 100%)",
        min_height="100vh",
        display="flex",
        flex_direction="column",
        justify_content="space-between",
        width="100%",
        max_width="100vw",
        overflow_x="hidden",
        box_sizing="border-box",
        font_family="'Outfit', sans-serif",
        color="#FFFFFF",
    )


def docs_page() -> rx.Component:
    """Dedicated Help & Official FAQs Page (Clean FAQ Accordion View)."""
    return rx.box(
        header(),
        faq(),
        footer(show_helpline_ribbon=False),
        bot_agent(),
        background="linear-gradient(180deg, #0A0F1D 0%, #030712 100%)",
        min_height="100vh",
        width="100%",
        max_width="100vw",
        overflow_x="hidden",
        box_sizing="border-box",
        font_family="'Outfit', sans-serif",
        color="#FFFFFF",
    )


# App configuration with custom Google Fonts, responsive viewport, and dark styles
app = rx.App(
    head_components=[
        rx.script(src="/cyberbot_voice.js"),
    ],
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
            "-webkit-text-size-adjust": "100%",
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
