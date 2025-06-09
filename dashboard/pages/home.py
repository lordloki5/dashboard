import reflex as rx
from dashboard.components.navbar import navbar_icons

def home() -> rx.Component:
    return rx.vstack(
        navbar_icons(),
        rx.container(
            rx.heading("Dashboard Home", size="4"),
            rx.text("Welcome to the Battlestation Dashboard", size="2"),
            padding="2em",
            width="100%",
        ),
        width="100%",
    )