import reflex as rx

config = rx.Config(
    app_name="cyber_shield_reflex",
    frontend_port=3000,
    backend_port=8000,
    plugins=[
        rx.plugins.RadixThemesPlugin(
            theme=rx.theme(
                appearance="light",
                accent_color="teal",
                radius="medium",
            )
        )
    ],
)
