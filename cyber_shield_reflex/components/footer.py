import reflex as rx
from cyber_shield_reflex.state import State
from cyber_shield_reflex.components.modals import complaint_prerequisites_modal, disclaimer_modal


def footer(show_helpline_ribbon: bool = False) -> rx.Component:
    """
    Minimal modern footer component with optional helpline ribbon and copyright bar.
    """
    return rx.box(
        complaint_prerequisites_modal(),
        disclaimer_modal(),
        
        # Upper Helpline & Complaint Action Ribbon
        rx.cond(
            show_helpline_ribbon,
            rx.box(
                rx.box(
                    rx.vstack(
                        rx.text(
                            "Any victim of financial cyber fraud can dial helpline number 1930",
                            font_size="16px",
                            font_weight="600",
                            color="#0284C7",
                            font_family="'Outfit', sans-serif",
                        ),
                        rx.button(
                            "Register a Complaint",
                            background="linear-gradient(90deg, #00A3E0 0%, #0077C5 100%)",
                            color="#FFFFFF",
                            font_weight="700",
                            font_size="14px",
                            font_family="'Outfit', sans-serif",
                            padding_x="24px",
                            padding_y="12px",
                            border_radius="6px",
                            box_shadow="0 4px 12px rgba(0, 163, 224, 0.3)",
                            cursor="pointer",
                            on_click=State.toggle_complaint_modal,  # type: ignore
                            _hover={"opacity": 0.9},
                        ),
                        spacing="3",
                        align="start",
                    ),
                    width="100%",
                    padding_x={"initial": "16px", "md": "48px"},
                    padding_y="28px",
                ),
                background="#FFFFFF",
                border_bottom="1px solid #E2E8F0",
                width="100%",
            ),
        ),
        
        # Clean Copyright Bar
        rx.box(
            rx.hstack(
                rx.text(
                    "© 2026 Cyber Fraud Shield. All rights reserved.",
                    font_size="14px",
                    color="#64748B",
                    font_family="'Outfit', sans-serif",
                ),
                justify="center",
                align="center",
                width="100%",
                padding_y="24px",
                padding_x={"initial": "16px", "md": "48px"},
            ),
            background="#F8FAFC",
            border_top="1px solid #E2E8F0",
            width="100%",
            id="contact-us",
        ),
        width="100%",
    )
