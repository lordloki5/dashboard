import reflex as rx
import asyncio
from typing import cast


async def fetch_cstn_to_cfsh_data() -> dict[str, list[str]]:
    """Mock API function to fetch CSTN to CFSH data."""
    await asyncio.sleep(0.5)
    return {
        "cstn_alpha": ["cfsh_A", "cfsh_B", "cfsh_C"],
        "cstn_beta": ["cfsh_D", "cfsh_E"],
        "cstn_gamma": ["cfsh_F"],
    }


async def fetch_cfsh_to_engine_data() -> (
    dict[str, list[str]]
):
    """Mock API function to fetch CFSH to Engine data."""
    await asyncio.sleep(0.5)
    return {
        "cfsh_A": ["engine_1", "engine_2"],
        "cfsh_B": ["engine_3"],
        "cfsh_C": ["engine_4", "engine_5"],
        "cfsh_D": ["engine_6"],
        "cfsh_E": ["engine_7", "engine_8"],
        "cfsh_F": ["engine_9"],
    }


async def fetch_engine_to_group_data() -> (
    dict[str, list[str]]
):
    """Mock API function to fetch Engine to Group data."""
    await asyncio.sleep(0.5)
    return {
        "engine_1": ["group_X", "group_Y"],
        "engine_2": ["group_Z"],
        "engine_3": ["group_X", "group_W"],
        "engine_4": ["group_V"],
        "engine_5": ["group_Y", "group_Z"],
        "engine_6": ["group_U"],
        "engine_7": ["group_T"],
        "engine_8": ["group_S", "group_X"],
        "engine_9": ["group_R"],
    }


async def fetch_group_to_stack_data() -> (
    dict[str, list[str]]
):
    """Mock API function to fetch Group to Stack data."""
    await asyncio.sleep(0.5)
    return {
        "group_X": ["stack_alpha", "stack_beta"],
        "group_Y": ["stack_gamma"],
        "group_Z": ["stack_delta", "stack_epsilon"],
        "group_W": ["stack_zeta"],
        "group_V": ["stack_eta"],
        "group_U": ["stack_theta"],
        "group_T": ["stack_iota"],
        "group_S": ["stack_kappa"],
        "group_R": ["stack_lambda"],
    }


async def fetch_engine_status_data() -> dict[str, str]:
    """Mock API function to fetch Engine status data."""
    await asyncio.sleep(0.5)
    return {
        "engine_1": "working",
        "engine_2": "stopped",
        "engine_3": "working",
        "engine_4": "working",
        "engine_5": "stopped",
        "engine_6": "working",
        "engine_7": "stopped",
        "engine_8": "working",
        "engine_9": "working",
    }


class AppState(rx.State):
    is_loading: bool = True
    cstn_to_cfsh: dict[str, list[str]] = {}
    cfsh_to_engine: dict[str, list[str]] = {}
    engine_to_group: dict[str, list[str]] = {}
    group_to_stack: dict[str, list[str]] = {}
    engine_status: dict[str, str] = {}
    selected_cstn: str = ""
    selected_cfsh: str = ""
    selected_engine: str = ""
    selected_group: str = ""
    selected_stack: str = ""
    info_tab_toggle: bool = True
    search_query: str = ""
    sidebar_open: bool = False

    @rx.event(background=True)
    async def load_data(self):
        async with self:
            self.is_loading = True
        results = await asyncio.gather(
            fetch_cstn_to_cfsh_data(),
            fetch_cfsh_to_engine_data(),
            fetch_engine_to_group_data(),
            fetch_group_to_stack_data(),
            fetch_engine_status_data(),
        )
        async with self:
            (
                self.cstn_to_cfsh,
                self.cfsh_to_engine,
                self.engine_to_group,
                self.group_to_stack,
                self.engine_status,
            ) = results
            if self.cstn_to_cfsh:
                current_cstn_exists = (
                    self.selected_cstn in self.cstn_to_cfsh
                )
                if not current_cstn_exists:
                    self.selected_cstn = list(
                        self.cstn_to_cfsh.keys()
                    )[0]
            self.selected_cfsh = ""
            self.selected_engine = ""
            self.selected_group = ""
            self.selected_stack = ""
            self.is_loading = False

    def refresh_data(self):
        return AppState.load_data

    @rx.var
    def cstn_options(self) -> list[str]:
        return list(self.cstn_to_cfsh.keys())

    @rx.var
    def current_cfsh_names(self) -> list[str]:
        return self.cstn_to_cfsh.get(self.selected_cstn, [])

    @rx.var
    def current_groups(self) -> list[str]:
        groups = set()
        if self.selected_engine:
            groups.update(
                self.engine_to_group.get(
                    self.selected_engine, []
                )
            )
        elif self.selected_cfsh:
            engines_on_cfsh = self.cfsh_to_engine.get(
                self.selected_cfsh, []
            )
            for engine in engines_on_cfsh:
                groups.update(
                    self.engine_to_group.get(engine, [])
                )
        else:
            cfsh_names = self.cstn_to_cfsh.get(
                self.selected_cstn, []
            )
            for cfsh in cfsh_names:
                engines_on_cfsh = self.cfsh_to_engine.get(
                    cfsh, []
                )
                for engine in engines_on_cfsh:
                    groups.update(
                        self.engine_to_group.get(engine, [])
                    )
        sorted_groups = sorted(list(groups))
        if self.search_query:
            return [
                g
                for g in sorted_groups
                if self.search_query.lower() in g.lower()
            ]
        return sorted_groups

    @rx.var
    def current_stacks(self) -> list[str]:
        if not self.selected_group:
            return []
        return self.group_to_stack.get(
            self.selected_group, []
        )

    def open_sidebar(self):
        self.sidebar_open = True

    def close_sidebar(self):
        self.sidebar_open = False

    def select_cstn(self, name: str):
        self.selected_cstn = name
        self.selected_cfsh = ""
        self.selected_engine = ""
        self.selected_group = ""
        self.selected_stack = ""
        self.sidebar_open = False

    def select_cfsh(self, name: str):
        if self.selected_cfsh == name:
            self.selected_cfsh = ""
        else:
            self.selected_cfsh = name
        self.selected_engine = ""
        self.selected_group = ""
        self.selected_stack = ""
        self.sidebar_open = False

    def select_engine(
        self, engine_name: str, cfsh_name: str
    ):
        if self.selected_engine == engine_name:
            self.selected_engine = ""
        else:
            self.selected_engine = engine_name
            self.selected_cfsh = cfsh_name
            self.sidebar_open = True
        self.selected_group = ""
        self.selected_stack = ""

    def _find_parent_engine_and_cfsh(
        self, group_name: str
    ) -> tuple[str, str]:
        for engine, groups in self.engine_to_group.items():
            if group_name in groups:
                for (
                    cfsh,
                    engines,
                ) in self.cfsh_to_engine.items():
                    if engine in engines:
                        return (engine, cfsh)
        return ("", "")

    def select_group(self, group_name: str):
        if self.selected_group == group_name:
            self.selected_group = ""
            self.selected_engine = ""
            self.selected_cfsh = ""
        else:
            engine, cfsh = (
                self._find_parent_engine_and_cfsh(
                    group_name
                )
            )
            self.selected_group = group_name
            self.selected_engine = engine
            self.selected_cfsh = cfsh
        self.selected_stack = ""
        self.sidebar_open = False

    def select_stack(self, stack_name: str):
        if self.selected_stack == stack_name:
            self.selected_stack = ""
        else:
            self.selected_stack = stack_name
            self.sidebar_open = True

    def toggle_info_tab(self):
        self.info_tab_toggle = not self.info_tab_toggle

    def set_search_query(self, query: str):
        self.search_query = query


def sidebar() -> rx.Component:
    return rx.el.div(
        rx.el.aside(
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Details",
                        class_name="text-lg font-semibold text-white",
                    ),
                    rx.el.button(
                        rx.icon(
                            tag="x", class_name="text-white"
                        ),
                        on_click=AppState.close_sidebar,
                        class_name="p-1 rounded-full hover:bg-gray-700",
                    ),
                    class_name="flex justify-between items-center mb-4",
                ),
                rx.el.div(
                    rx.el.details(
                        rx.el.summary(
                            f"CSTN: {AppState.selected_cstn}",
                            class_name="font-semibold text-white cursor-pointer",
                        ),
                        rx.el.p(
                            "Details about the cstn...",
                            class_name="text-gray-300 mt-2 text-sm",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.details(
                        rx.el.summary(
                            f"CFSH: {AppState.selected_cfsh}",
                            class_name="font-semibold text-white cursor-pointer",
                        ),
                        rx.el.p(
                            "Details about the cfsh...",
                            class_name="text-gray-300 mt-2 text-sm",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.details(
                        rx.el.summary(
                            f"Engine: {AppState.selected_engine}",
                            class_name="font-semibold text-white cursor-pointer",
                        ),
                        rx.el.p(
                            "Details about the engine...",
                            class_name="text-gray-300 mt-2 text-sm",
                        ),
                    ),
                    class_name="space-y-2",
                ),
                class_name="p-4",
            ),
            class_name="w-64 bg-gray-800 text-white h-full",
        ),
        class_name=rx.cond(
            AppState.sidebar_open,
            "fixed top-0 right-0 h-full bg-gray-800 text-white transition-transform transform translate-x-0 duration-300 z-50",
            "fixed top-0 right-0 h-full bg-gray-800 text-white transition-transform transform translate-x-full duration-300 z-50",
        ),
    )


def engine_icon(
    engine_name: str, cfsh_name: str
) -> rx.Component:
    is_selected = AppState.selected_engine == engine_name
    engine_status = AppState.engine_status.get(
        engine_name, "stopped"
    )
    return rx.el.label(
        rx.el.input(
            type="radio",
            name="engine_selection",
            class_name="hidden",
            on_click=lambda: AppState.select_engine(
                engine_name, cfsh_name
            ),
            checked=is_selected,
            default_value=engine_name,
        ),
        rx.el.div(
            rx.tooltip(
                rx.icon(
                    "heart",
                    class_name=rx.cond(
                        engine_status == "working",
                        "text-green-500",
                        "text-red-500",
                    ),
                ),
                content=engine_name,
            ),
            class_name=rx.cond(
                is_selected,
                "p-1 rounded-full bg-blue-200 cursor-pointer",
                "p-1 rounded-full hover:bg-gray-200 cursor-pointer",
            ),
        ),
        class_name="flex items-center",
    )


def top_row() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                "CSTN:", class_name="font-semibold mr-2"
            ),
            rx.el.p(
                AppState.selected_cstn,
                class_name="font-bold text-indigo-600",
            ),
            class_name="flex items-center",
        ),
        rx.el.div(
            rx.el.select(
                rx.foreach(
                    AppState.cstn_options,
                    lambda name: rx.el.option(
                        name, value=name
                    ),
                ),
                value=AppState.selected_cstn,
                on_change=AppState.select_cstn,
                class_name="p-2 border rounded-md shadow-sm",
                placeholder="Select CSTN",
            ),
            rx.el.button(
                rx.icon("refresh-cw", class_name="w-4 h-4"),
                "Refresh",
                on_click=AppState.refresh_data,
                is_loading=AppState.is_loading,
                class_name="flex items-center gap-2 p-2 bg-blue-500 text-white rounded-md shadow-sm hover:bg-blue-600 disabled:opacity-50",
            ),
            class_name="flex items-center space-x-4",
        ),
        class_name="flex justify-between items-center p-4 bg-white rounded-lg shadow",
    )


def cfsh_row() -> rx.Component:
    return rx.el.div(
        rx.foreach(
            AppState.current_cfsh_names,
            lambda cfsh: rx.el.div(
                rx.el.label(
                    rx.el.input(
                        type="radio",
                        name="cfsh_selection",
                        class_name="mr-2",
                        on_click=lambda: AppState.select_cfsh(
                            cfsh
                        ),
                        checked=AppState.selected_cfsh
                        == cfsh,
                        default_value=cfsh,
                    ),
                    cfsh,
                    class_name="flex items-center font-medium cursor-pointer w-32 shrink-0",
                ),
                rx.el.div(
                    rx.foreach(
                        AppState.cfsh_to_engine.get(
                            cfsh, []
                        ),
                        lambda engine: engine_icon(
                            engine, cfsh
                        ),
                    ),
                    class_name="flex items-center space-x-2",
                ),
                class_name="flex items-center p-3 bg-gray-50 rounded-md",
            ),
        ),
        class_name="flex flex-col space-y-2 p-4",
    )


def groups_column() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Groups",
            class_name="text-lg font-semibold mb-2",
        ),
        rx.el.input(
            placeholder="Search groups...",
            on_change=AppState.set_search_query,
            class_name="w-full p-2 border rounded-md mb-4",
        ),
        rx.el.div(
            rx.foreach(
                AppState.current_groups,
                lambda group: rx.el.label(
                    rx.el.input(
                        type="radio",
                        name="group_selection",
                        class_name="mr-2",
                        on_click=lambda: AppState.select_group(
                            group
                        ),
                        checked=AppState.selected_group
                        == group,
                        default_value=group,
                    ),
                    group,
                    class_name="flex items-center p-2 hover:bg-gray-100 rounded-md cursor-pointer",
                ),
            ),
            class_name="space-y-1 overflow-y-auto h-96",
        ),
        class_name="p-4 bg-white rounded-lg shadow",
    )


def stacks_column() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Stacks",
            class_name="text-lg font-semibold mb-2",
        ),
        rx.el.div(
            rx.cond(
                AppState.selected_group,
                rx.foreach(
                    AppState.current_stacks,
                    lambda stack: rx.el.label(
                        rx.el.input(
                            type="radio",
                            name="stack_selection",
                            class_name="mr-2",
                            on_click=lambda: AppState.select_stack(
                                stack
                            ),
                            checked=AppState.selected_stack
                            == stack,
                            default_value=stack,
                        ),
                        stack,
                        class_name="flex items-center p-2 hover:bg-gray-100 rounded-md cursor-pointer",
                    ),
                ),
                rx.el.p(
                    "Select a group to see stacks.",
                    class_name="text-gray-500",
                ),
            ),
            class_name="space-y-1 overflow-y-auto h-96",
        ),
        class_name="p-4 bg-white rounded-lg shadow",
    )


def info_column() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.label(
                "Toggle Info",
                class_name="font-medium text-gray-700",
            ),
            rx.el.div(
                rx.el.span("Tab 1", class_name="mr-2"),
                rx.el.button(
                    rx.el.div(
                        class_name="w-4 h-4 bg-white rounded-full shadow-md transform transition-transform"
                    ),
                    on_click=AppState.toggle_info_tab,
                    class_name=rx.cond(
                        AppState.info_tab_toggle,
                        "w-12 h-6 flex items-center bg-gray-300 rounded-full p-1 duration-300 ease-in-out",
                        "w-12 h-6 flex items-center bg-blue-500 rounded-full p-1 duration-300 ease-in-out justify-end",
                    ),
                ),
                rx.el.span("Tab 2", class_name="ml-2"),
                class_name="flex items-center",
            ),
            class_name="flex items-center justify-between mb-4",
        ),
        rx.cond(
            AppState.info_tab_toggle,
            rx.el.div(
                "Displaying info for Tab 1.",
                class_name="p-4 bg-gray-50 rounded h-80",
            ),
            rx.el.div(
                "Displaying info for Tab 2.",
                class_name="p-4 bg-gray-50 rounded h-80",
            ),
        ),
        class_name="p-4 bg-white rounded-lg shadow",
    )


def main_content() -> rx.Component:
    return rx.el.main(
        top_row(),
        cfsh_row(),
        rx.el.div(
            groups_column(),
            stacks_column(),
            info_column(),
            class_name="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4",
        ),
        class_name="flex-1 p-6",
    )


def loading_overlay() -> rx.Component:
    return rx.el.div(
        rx.spinner(class_name="w-12 h-12 text-blue-500"),
        class_name="absolute inset-0 bg-gray-100 bg-opacity-75 flex items-center justify-center z-50",
    )


def index() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            sidebar(),
            rx.el.div(
                rx.cond(
                    AppState.is_loading,
                    loading_overlay(),
                    main_content(),
                ),
                class_name="flex-1 relative",
            ),
            class_name="flex flex-1",
        ),
        on_mount=AppState.load_data,
        class_name="min-h-screen bg-gray-100 font-['Inter']",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(
            rel="preconnect",
            href="https://fonts.googleapis.com",
        ),
        rx.el.link(
            rel="preconnect",
            href="https://fonts.gstatic.com",
            crossorigin="",
        ),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, title="Deployment Dashboard")
