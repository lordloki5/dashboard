import reflex as rx
import asyncio
import websockets

class MyState(rx.State):
    message: str = "Waiting for message..."

    @rx.event(background=True)
    async def websocket_listener(self):
        try:
            async with websockets.connect("wss://stream.binance.com:9443/ws/btcusdt@kline_1m") as websocket:
                # Ignore the initial message
                initial_msg = await websocket.recv()
                print(f"Initial message received: {initial_msg}")
                while True:
                    msg = await websocket.recv()
                    async with self:
                        self.message = msg
        except Exception as e:
            async with self:
                self.message = f"Error: {str(e)}"

def index():
    return rx.vstack(
        rx.text(MyState.message),
        rx.button("Start Listener", on_click=MyState.websocket_listener),
    )

app = rx.App()
app.add_page(index)