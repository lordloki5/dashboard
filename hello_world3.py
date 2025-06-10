import reflex as rx
import asyncio
import websockets
import time

# Global dictionary to store WebSocket tasks for each cstn_name
_web_socket_tasks = {}

class MyState(rx.State):
    cstn_name: str = "u_in_omm_cstn_02"
    cstn_names: list[str] = [
        "d_in_omm_cstn_ss001", "p_in_omm_cstn_01",
        "p_in_omm_cstn_02", "p_in_omm_cstn_03", "p_in_omm_cstn_bse01",
        "p_in_omm_cstn_bse02", "p_in_omm_cstn_ss001", "u_in_omm_cstn_01",
        "u_in_omm_cstn_02"
    ]
    messages: dict[str, str] = {name: "Waiting for message..." for name in cstn_names}
    new_messages: dict[str, bool] = {name: False for name in cstn_names}
    show_refresh_text: bool = False

    @rx.var
    def button_color(self) -> str:
        return "orange" if self.new_messages.get(self.cstn_name, False) else "green"

    def acknowledge_message(self):
        if self.cstn_name in self.new_messages:
            self.new_messages[self.cstn_name] = False
            self.show_refresh_text = False

    @rx.event(background=True)
    async def run_websocket(self, name: str):
        # Placeholder URL; replace with get_ws_url_for(name) in production
        url = "wss://stream.binance.com:9443/ws/btcusdt@kline_1m"
        while True:
            try:
                async with websockets.connect(url, ping_interval=20, ping_timeout=20) as websocket:
                    print(f"WebSocket connected for {name}")
                    initial_msg = await websocket.recv()
                    print(f"Initial message for {name}: {initial_msg}")
                    async with self:
                        self.messages[name] = initial_msg
                        if name == self.cstn_name:
                            self.new_messages[name] = True
                            self.show_refresh_text = True
                    while True:
                        try:
                            msg = await asyncio.wait_for(websocket.recv(), timeout=30)
                            print(f"Received message for {name}: {msg}")
                            async with self:
                                self.messages[name] = msg
                                if name == self.cstn_name:
                                    self.new_messages[name] = True
                                    self.show_refresh_text = True
                        except asyncio.TimeoutError:
                            print(f"Timeout waiting for message for {name}, sending ping")
                            await websocket.ping()
                        except Exception as e:
                            print(f"Error in WebSocket loop for {name}: {str(e)}")
                            async with self:
                                self.messages[name] = f"Error for {name}: {str(e)}"
                                if name == self.cstn_name:
                                    self.new_messages[name] = True
                                    self.show_refresh_text = True
                            break  # Exit inner loop to reconnect
            except Exception as e:
                print(f"WebSocket connection failed for {name}: {str(e)}")
                async with self:
                    self.messages[name] = f"Connection error for {name}: {str(e)}"
                    if name == self.cstn_name:
                        self.new_messages[name] = True
                        self.show_refresh_text = True
                await asyncio.sleep(5)  # Wait before reconnecting

    def start_websocket_for(self, name: str):
        global _web_socket_tasks
        if name not in _web_socket_tasks or _web_socket_tasks[name].task.done():
            print(f"Starting WebSocket task for {name}")
            _web_socket_tasks[name] = self.run_websocket(name)

    def set_cstn_name(self, name: str):
        self.start_websocket_for(name)
        self.cstn_name = name
        self.show_refresh_text = self.new_messages.get(name, False)
        print(f"Selected cstn_name: {name}")

    def start_initial_websocket(self):
        self.start_websocket_for(self.cstn_name)

def index():
    return rx.box(
        rx.vstack(
            rx.select(MyState.cstn_names, value=MyState.cstn_name, on_change=MyState.set_cstn_name),
            rx.text(MyState.cstn_name),
            rx.text(MyState.messages.get(MyState.cstn_name, "No message")),
            rx.cond(
                MyState.show_refresh_text,
                rx.text("Refresh Now!", color="red"),
            ),
            rx.button("Acknowledge", bg=MyState.button_color, on_click=MyState.acknowledge_message),
        ),
        on_mount=MyState.start_initial_websocket,
    )

app = rx.App()
app.add_page(index)