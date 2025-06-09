import reflex as rx
from dashboard.components.navbar import navbar_icons

def live() -> rx.Component:
    return rx.vstack(
        navbar_icons(),
        rx.text("We are live", size="6", margin_top="2em"),
    )


