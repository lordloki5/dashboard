import reflex as rx
from dashboard.components.navbar import navbar_icons

def versioncmp() -> rx.Component:
    return rx.vstack(
        navbar_icons(),
        rx.text("Version Compare", size="6", margin_top="2em"),
    )