import reflex as rx
from cyber_shield_reflex.state import State
from cyber_shield_reflex.components.modals import complaint_prerequisites_modal, disclaimer_modal


def footer(show_helpline_ribbon: bool = False) -> rx.Component:
    """
    Minimal modern footer component with optional helpline ribbon and dark-theme copyright bar.
    """
    return rx.box(
        complaint_prerequisites_modal(),
        disclaimer_modal(),
        
        # Upper Helpline & Complaint Action Ribbon (Dark Blue & Black background)
        rx.cond(
            show_helpline_ribbon,
            rx.box(
                rx.box(
                    rx.vstack(
                        rx.text(
                            "Any victim of financial cyber fraud can dial helpline number 1930",
                            font_size="16px",
                            font_weight="600",
                            color="#38BDF8",
                            font_family="'Outfit', sans-serif",
                        ),
                        rx.button(
                            "Register a Complaint",
                            background="linear-gradient(90deg, #1D4ED8 0%, #1E40AF 100%)",
                            color="#FFFFFF",
                            font_weight="700",
                            font_size="14px",
                            font_family="'Outfit', sans-serif",
                            padding_x="24px",
                            padding_y="12px",
                            border_radius="6px",
                            box_shadow="0 4px 14px rgba(29, 78, 216, 0.4)",
                            cursor="pointer",
                            on_click=State.toggle_complaint_modal,  # type: ignore
                            _hover={"opacity": 0.9, "transform": "translateY(-1px)"},
                        ),
                        spacing="3",
                        align="start",
                    ),
                    width="100%",
                    padding_x={"initial": "16px", "md": "48px"},
                    padding_y="28px",
                ),
                background="#0F172A",
                border_bottom="1px solid #1E293B",
                width="100%",
            ),
        ),
        
        # Clean Copyright Bar (Black background)
        rx.box(
            rx.hstack(
                rx.text(
                    "© 2026 Cyber Fraud Shield. All rights reserved.",
                    font_size="14px",
                    color="#94A3B8",
                    font_family="'Outfit', sans-serif",
                ),
                justify="center",
                align="center",
                width="100%",
                padding_y="24px",
                padding_x={"initial": "16px", "md": "48px"},
            ),
            background="#030712",
            border_top="1px solid #1E293B",
            width="100%",
            id="contact-us",
        ),
        width="100%",
    )
