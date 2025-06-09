import reflex as rx
from dashboard.components.navbar import navbar_icons

def status() -> rx.Component:
    return rx.vstack(
        navbar_icons(),
        rx.text("Our status", size="6", margin_top="2em"),
    )

