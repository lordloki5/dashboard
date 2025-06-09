import reflex as rx
from dashboard.components.navbar import navbar_icons

def diff() -> rx.Component:
    return rx.vstack(
        navbar_icons(),
        rx.text("diff Plans", size="6", margin_top="2em"),
    )

