import reflex as rx
from cyber_shield_reflex.state import State


def render_message(msg: rx.Var[dict]) -> rx.Component:
    """Renders an individual chat message in the Bot Popup."""
    is_bot = msg["sender"] == "bot"  # type: ignore
    return rx.hstack(
        rx.cond(
            is_bot,
            rx.box(
                rx.icon("bot", size=18, color="#FFFFFF"),
                background="#1B6E5B",
                padding="6px",
                border_radius="50%",
                flex_shrink="0",
            ),
        ),
        rx.box(
            rx.text(
                msg["text"],  # type: ignore
                font_size="13px",
                color=rx.cond(is_bot, "#0D1B1E", "#FFFFFF"),
                font_family="'Outfit', sans-serif",
                white_space="pre-wrap",
            ),
            background=rx.cond(is_bot, "#F0F4F3", "#1B6E5B"),
            padding="10px 14px",
            border_radius="12px",
            max_width="80%",
        ),
        justify=rx.cond(is_bot, "start", "end"),
        width="100%",
        spacing="2",
        align="start",
        margin_y="4px",
    )


def bot_agent() -> rx.Component:
    """
    Floating AI Bot Agent Widget.
    Toggles a floating interactive chat popup window in bottom-right corner.
    """
    return rx.box(
        # Floating Chat Window Popup
        rx.cond(
            State.bot_open,
            rx.box(
                # Header Bar
                rx.hstack(
                    rx.hstack(
                        rx.icon("bot", size=22, color="#38BDF8"),
                        rx.vstack(
                            rx.text("Cyber Shield AI Assistant", font_size="14px", font_weight="700", color="#FFFFFF", font_family="'Space Grotesk', sans-serif"),
                            rx.text("Online • Real-time Threat Intelligence", font_size="11px", color="#A7F3D0", font_family="'Outfit', sans-serif"),
                            spacing="0",
                        ),
                        spacing="2",
                        align="center",
                    ),
                    rx.icon(
                        "x",
                        size=20,
                        color="#F0F4F3",
                        cursor="pointer",
                        on_click=State.toggle_bot,  # type: ignore
                        _hover={"color": "#38BDF8"},
                    ),
                    justify="between",
                    align="center",
                    padding="14px 16px",
                    background="#0B3D2E",
                    border_top_left_radius="16px",
                    border_top_right_radius="16px",
                ),
                
                # Chat Messages Container
                rx.vstack(
                    rx.foreach(State.bot_messages, render_message),
                    padding="16px",
                    height="340px",
                    overflow_y="auto",
                    width="100%",
                    spacing="2",
                ),
                
                # Bottom Input Area
                rx.hstack(
                    rx.input(
                        placeholder="Ask about scam calls, text fraud...",
                        value=State.bot_input,
                        on_change=State.set_bot_input,  # type: ignore
                        font_size="13px",
                        border="1px solid #CBD5E1",
                        border_radius="8px",
                        width="100%",
                        padding_x="10px",
                    ),
                    rx.button(
                        rx.icon("send", size=16, color="#FFFFFF"),
                        on_click=State.send_bot_message,  # type: ignore
                        background="#1B6E5B",
                        cursor="pointer",
                        border_radius="8px",
                        padding_x="12px",
                        _hover={"background": "#145C46"},
                    ),
                    padding="12px 16px",
                    border_top="1px solid #E2E8F0",
                    background="#FFFFFF",
                    border_bottom_left_radius="16px",
                    border_bottom_right_radius="16px",
                    width="100%",
                ),
                position="fixed",
                bottom="86px",
                right="24px",
                width="360px",
                max_width="calc(100vw - 48px)",
                height="480px",
                background="#FFFFFF",
                border_radius="16px",
                box_shadow="0 12px 36px rgba(11, 61, 46, 0.2)",
                border="1px solid #CBD5E1",
                z_index="1000",
            ),
        ),
        
        # Floating Trigger Circle Button
        rx.button(
            rx.hstack(
                rx.icon("bot", size=24, color="#FFFFFF"),
                rx.text("AI Shield", font_size="13px", font_weight="700", color="#FFFFFF", display={"initial": "none", "sm": "block"}),
                spacing="2",
                align="center",
            ),
            on_click=State.toggle_bot,  # type: ignore
            position="fixed",
            bottom="24px",
            right="24px",
            background="#1B6E5B",
            color="#FFFFFF",
            padding="12px 18px",
            border_radius="30px",
            box_shadow="0 6px 20px rgba(27, 110, 91, 0.4)",
            cursor="pointer",
            z_index="999",
            _hover={"transform": "scale(1.05)", "background": "#145C46"},
            transition="all 0.2s ease-in-out",
        ),
    )
