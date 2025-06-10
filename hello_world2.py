import reflex as rx
import asyncio
import websockets

class MyState(rx.State):
    message: str = "Waiting for message..."
    new_message_received: bool = False

    @rx.var
    def button_color(self) -> str:
        return "orange" if self.new_message_received else "green"

    @rx.event(background=True)
    async def websocket_listener(self):
        try:
            async with websockets.connect("wss://stream.binance.com:9443/ws/btcusdt@kline_1m") as websocket:
                initial_msg = await websocket.recv()
                print(f"Initial message received: {initial_msg}")
                while True:
                    msg = await websocket.recv()
                    async with self:
                        self.message = msg
                        self.new_message_received = True
        except Exception as e:
            async with self:
                self.message = f"Error: {str(e)}"
                self.new_message_received = True

    def acknowledge_message(self):
        self.new_message_received = False

def index():
    return rx.box(
        rx.vstack(
            rx.text(MyState.message),
            rx.button("Acknowledge", bg=MyState.button_color, on_click=MyState.acknowledge_message),
        ),
        on_mount=MyState.websocket_listener
    )

app = rx.App()
app.add_page(index)