# # # # import reflex as rx
# # # # from typing import TypedDict, Union, cast


# # # # class Engine(TypedDict):
# # # #     name: str
# # # #     info: str


# # # # class Stack(TypedDict):
# # # #     name: str
# # # #     info: str


# # # # class SidebarEngineDetails(TypedDict):
# # # #     cstn_name: str
# # # #     cfsh_name: str
# # # #     engine: Engine


# # # # class SidebarStackDetails(TypedDict):
# # # #     group_name: str
# # # #     stack: Stack


# # # # CSTN_DATA: dict[str, list[str]] = {
# # # #     "CSTN_Alpha": ["CFSH_101", "CFSH_102", "CFSH_103"],
# # # #     "CSTN_Beta": ["CFSH_201", "CFSH_202"],
# # # #     "CSTN_Gamma": ["CFSH_301"],
# # # # }
# # # # CFSH_DATA: dict[str, list[Engine]] = {
# # # #     "CFSH_101": [
# # # #         {
# # # #             "name": "EngineA1",
# # # #             "info": "High-performance data processing engine.",
# # # #         },
# # # #         {
# # # #             "name": "EngineA2",
# # # #             "info": "Real-time analytics engine.",
# # # #         },
# # # #     ],
# # # #     "CFSH_102": [
# # # #         {
# # # #             "name": "EngineB1",
# # # #             "info": "Machine learning model serving.",
# # # #         }
# # # #     ],
# # # #     "CFSH_103": [
# # # #         {
# # # #             "name": "EngineC1",
# # # #             "info": "Batch processing tasks.",
# # # #         },
# # # #         {"name": "EngineC2", "info": "API gateway engine."},
# # # #     ],
# # # #     "CFSH_201": [
# # # #         {
# # # #             "name": "EngineD1",
# # # #             "info": "User authentication service.",
# # # #         }
# # # #     ],
# # # #     "CFSH_202": [
# # # #         {
# # # #             "name": "EngineE1",
# # # #             "info": "Notification and alert system.",
# # # #         },
# # # #         {
# # # #             "name": "EngineE2",
# # # #             "info": "Logging and monitoring service.",
# # # #         },
# # # #     ],
# # # #     "CFSH_301": [
# # # #         {
# # # #             "name": "EngineF1",
# # # #             "info": "Content delivery network.",
# # # #         }
# # # #     ],
# # # # }
# # # # GROUP_DATA: dict[str, list[Stack]] = {
# # # #     "Data Pipelines": [
# # # #         {
# # # #             "name": "DataIngest-v1",
# # # #             "info": "Handles ingestion from various sources.",
# # # #         },
# # # #         {
# # # #             "name": "DataTransform-v2",
# # # #             "info": "Performs ETL transformations.",
# # # #         },
# # # #     ],
# # # #     "Analytics Services": [
# # # #         {
# # # #             "name": "Reporting-API-v3",
# # # #             "info": "Serves reporting data.",
# # # #         },
# # # #         {
# # # #             "name": "ML-Scoring-v1",
# # # #             "info": "Scores data using ML models.",
# # # #         },
# # # #     ],
# # # #     "Core Infrastructure": [
# # # #         {
# # # #             "name": "AuthN-Service",
# # # #             "info": "Central authentication service.",
# # # #         },
# # # #         {
# # # #             "name": "ServiceDiscovery",
# # # #             "info": "Handles service registration.",
# # # #         },
# # # #     ],
# # # #     "Frontend Services": [
# # # #         {
# # # #             "name": "WebApp-Gateway",
# # # #             "info": "Main gateway for web applications.",
# # # #         }
# # # #     ],
# # # # }


# # # # class AppState(rx.State):
# # # #     """The application state."""

# # # #     selected_cstn_name: str = "CSTN_Alpha"
# # # #     selected_cfsh: dict[str, bool] = {}
# # # #     selected_engines: dict[str, bool] = {}
# # # #     group_search_query: str = ""
# # # #     selected_group: str = ""
# # # #     selected_stack: str = ""
# # # #     info_toggle: bool = False
# # # #     sidebar_visible: bool = False
# # # #     sidebar_content_type: str = ""
# # # #     sidebar_item_details: Union[
# # # #         SidebarEngineDetails, SidebarStackDetails, dict
# # # #     ] = {}

# # # #     @rx.var
# # # #     def cstn_options(self) -> list[str]:
# # # #         return list(CSTN_DATA.keys())

# # # #     @rx.var
# # # #     def current_cfsh_names(self) -> list[str]:
# # # #         return CSTN_DATA.get(self.selected_cstn_name, [])

# # # #     @rx.var
# # # #     def all_engines(self) -> dict[str, list[Engine]]:
# # # #         return CFSH_DATA

# # # #     @rx.var
# # # #     def filtered_groups(self) -> list[str]:
# # # #         if not self.group_search_query:
# # # #             return list(GROUP_DATA.keys())
# # # #         return [
# # # #             group
# # # #             for group in GROUP_DATA.keys()
# # # #             if self.group_search_query.lower()
# # # #             in group.lower()
# # # #         ]

# # # #     @rx.var
# # # #     def current_stack_options(self) -> list[Stack]:
# # # #         return GROUP_DATA.get(self.selected_group, [])

# # # #     def set_cstn_name(self, name: str):
# # # #         self.selected_cstn_name = name
# # # #         self.selected_cfsh = {}
# # # #         self.selected_engines = {}

# # # #     def toggle_cfsh_selection(self, name: str):
# # # #         self.selected_cfsh[name] = (
# # # #             not self.selected_cfsh.get(name, False)
# # # #         )

# # # #     def toggle_engine_selection(
# # # #         self, cfsh_name: str, engine_name: str
# # # #     ):
# # # #         is_selected = not self.selected_engines.get(
# # # #             engine_name, False
# # # #         )
# # # #         self.selected_engines[engine_name] = is_selected
# # # #         if is_selected:
# # # #             engine_details = next(
# # # #                 (
# # # #                     e
# # # #                     for e in CFSH_DATA.get(cfsh_name, [])
# # # #                     if e["name"] == engine_name
# # # #                 ),
# # # #                 None,
# # # #             )
# # # #             if engine_details:
# # # #                 self.sidebar_visible = True
# # # #                 self.sidebar_content_type = "engine"
# # # #                 self.sidebar_item_details = {
# # # #                     "cstn_name": self.selected_cstn_name,
# # # #                     "cfsh_name": cfsh_name,
# # # #                     "engine": engine_details,
# # # #                 }
# # # #         elif self.sidebar_content_type == "engine":
# # # #             engine_in_sidebar = cast(
# # # #                 SidebarEngineDetails,
# # # #                 self.sidebar_item_details,
# # # #             ).get("engine", {})
# # # #             if (
# # # #                 isinstance(engine_in_sidebar, dict)
# # # #                 and engine_in_sidebar.get("name")
# # # #                 == engine_name
# # # #             ):
# # # #                 self.sidebar_visible = False

# # # #     def select_group(self, group_name: str):
# # # #         self.selected_group = group_name
# # # #         self.selected_stack = ""

# # # #     def select_stack(self, stack_name: str):
# # # #         if not stack_name:
# # # #             self.selected_stack = ""
# # # #             if self.sidebar_content_type == "stack":
# # # #                 self.sidebar_visible = False
# # # #             return
# # # #         self.selected_stack = stack_name
# # # #         self.sidebar_visible = True
# # # #         self.sidebar_content_type = "stack"
# # # #         stack_details = next(
# # # #             (
# # # #                 s
# # # #                 for s in self.current_stack_options
# # # #                 if s["name"] == stack_name
# # # #             ),
# # # #             {"name": "", "info": ""},
# # # #         )
# # # #         self.sidebar_item_details = {
# # # #             "group_name": self.selected_group,
# # # #             "stack": stack_details,
# # # #         }

# # # #     def toggle_info(self):
# # # #         self.info_toggle = not self.info_toggle

# # # #     def hide_sidebar(self):
# # # #         self.sidebar_visible = False


# # # # def engine_icon(
# # # #     cfsh_name: str, engine: rx.Var[Engine]
# # # # ) -> rx.Component:
# # # #     engine_name = engine["name"]
# # # #     return rx.el.div(
# # # #         rx.el.input(
# # # #             type="checkbox",
# # # #             class_name="mr-2 h-4 w-4 accent-pink-500",
# # # #             checked=AppState.selected_engines[engine_name],
# # # #             on_change=lambda is_checked: AppState.toggle_engine_selection(
# # # #                 cfsh_name, engine_name
# # # #             ),
# # # #         ),
# # # #         rx.el.div(
# # # #             rx.icon(
# # # #                 tag="heart",
# # # #                 class_name="h-5 w-5 text-red-500",
# # # #             ),
# # # #             title=engine_name,
# # # #             class_name="cursor-pointer",
# # # #         ),
# # # #         class_name="flex items-center",
# # # #     )


# # # # def cfsh_item(cfsh_name: str) -> rx.Component:
# # # #     return rx.el.div(
# # # #         rx.el.input(
# # # #             type="checkbox",
# # # #             class_name="mr-2 h-4 w-4 accent-indigo-500",
# # # #             on_change=lambda: AppState.toggle_cfsh_selection(
# # # #                 cfsh_name
# # # #             ),
# # # #             checked=AppState.selected_cfsh.get(
# # # #                 cfsh_name, False
# # # #             ),
# # # #         ),
# # # #         rx.el.span(
# # # #             cfsh_name,
# # # #             class_name="font-semibold text-gray-700",
# # # #         ),
# # # #         rx.el.div(
# # # #             rx.foreach(
# # # #                 AppState.all_engines[cfsh_name],
# # # #                 lambda engine: engine_icon(
# # # #                     cfsh_name, engine
# # # #                 ),
# # # #             ),
# # # #             class_name="flex items-center gap-x-3 ml-4",
# # # #         ),
# # # #         class_name="flex items-center p-2 bg-gray-50 rounded-lg",
# # # #     )


# # # # def groups_column() -> rx.Component:
# # # #     return rx.el.div(
# # # #         rx.el.input(
# # # #             placeholder="Search Groups...",
# # # #             on_change=AppState.set_group_search_query,
# # # #             class_name="w-full p-2 mb-4 border rounded-lg",
# # # #         ),
# # # #         rx.el.div(
# # # #             rx.foreach(
# # # #                 AppState.filtered_groups,
# # # #                 lambda group: rx.el.div(
# # # #                     group,
# # # #                     on_click=lambda: AppState.select_group(
# # # #                         group
# # # #                     ),
# # # #                     class_name=rx.cond(
# # # #                         AppState.selected_group == group,
# # # #                         "p-2 rounded-lg cursor-pointer bg-indigo-500 text-white",
# # # #                         "p-2 rounded-lg cursor-pointer hover:bg-gray-100",
# # # #                     ),
# # # #                 ),
# # # #             ),
# # # #             class_name="space-y-2 overflow-y-auto h-64",
# # # #         ),
# # # #         class_name="p-4 border-r",
# # # #     )


# # # # def stacks_column() -> rx.Component:
# # # #     return rx.el.div(
# # # #         rx.el.select(
# # # #             rx.el.option("Select a stack", value=""),
# # # #             rx.foreach(
# # # #                 AppState.current_stack_options,
# # # #                 lambda stack: rx.el.option(
# # # #                     stack["name"], value=stack["name"]
# # # #                 ),
# # # #             ),
# # # #             on_change=AppState.select_stack,
# # # #             value=AppState.selected_stack,
# # # #             class_name="w-full p-2 border rounded-lg",
# # # #             disabled=AppState.selected_group == "",
# # # #         ),
# # # #         class_name="p-4 border-r",
# # # #     )


# # # # def info_column() -> rx.Component:
# # # #     return rx.el.div(
# # # #         rx.el.label(
# # # #             rx.el.input(
# # # #                 type="checkbox",
# # # #                 on_change=AppState.toggle_info,
# # # #                 class_name="hidden peer",
# # # #             ),
# # # #             rx.el.div(
# # # #                 class_name="w-14 h-8 bg-gray-200 rounded-full peer peer-focus:outline-none peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-7 after:w-7 after:transition-all peer-checked:bg-indigo-600"
# # # #             ),
# # # #             rx.el.span(
# # # #                 rx.cond(
# # # #                     AppState.info_toggle,
# # # #                     "Info Tab 2",
# # # #                     "Info Tab 1",
# # # #                 ),
# # # #                 class_name="ml-3 text-sm font-medium text-gray-900",
# # # #             ),
# # # #             class_name="relative inline-flex items-center cursor-pointer mb-4",
# # # #         ),
# # # #         rx.cond(
# # # #             AppState.info_toggle,
# # # #             rx.el.div(
# # # #                 rx.el.h4(
# # # #                     "Info Tab 2 Details",
# # # #                     class_name="font-bold",
# # # #                 ),
# # # #                 rx.el.p(
# # # #                     "This is the content for the second information tab. It can contain different components and data."
# # # #                 ),
# # # #                 class_name="p-4 bg-purple-50 rounded-lg",
# # # #             ),
# # # #             rx.el.div(
# # # #                 rx.el.h4(
# # # #                     "Info Tab 1 Details",
# # # #                     class_name="font-bold",
# # # #                 ),
# # # #                 rx.el.p(
# # # #                     "This is the content for the first information tab."
# # # #                 ),
# # # #                 class_name="p-4 bg-blue-50 rounded-lg",
# # # #             ),
# # # #         ),
# # # #         class_name="p-4",
# # # #     )


# # # # def sidebar() -> rx.Component:

# # # #     def dropdown(title: str, content: str) -> rx.Component:
# # # #         return rx.el.details(
# # # #             rx.el.summary(
# # # #                 title,
# # # #                 class_name="font-semibold cursor-pointer py-2",
# # # #             ),
# # # #             rx.el.p(
# # # #                 content,
# # # #                 class_name="px-4 py-2 bg-gray-100 rounded-b-lg",
# # # #             ),
# # # #             class_name="border-b",
# # # #         )

# # # #     engine_details = cast(
# # # #         dict,
# # # #         AppState.sidebar_item_details.get("engine", {}),
# # # #     )
# # # #     engine_info = engine_details.get(
# # # #         "info", "No info available."
# # # #     )
# # # #     engine_name = engine_details.get("name", "")
# # # #     stack_details = cast(
# # # #         dict, AppState.sidebar_item_details.get("stack", {})
# # # #     )
# # # #     stack_info = stack_details.get(
# # # #         "info", "No info available."
# # # #     )
# # # #     stack_name = stack_details.get("name", "")
# # # #     return rx.cond(
# # # #         AppState.sidebar_visible,
# # # #         rx.el.div(
# # # #             rx.el.button(
# # # #                 rx.icon(tag="x", class_name="h-6 w-6"),
# # # #                 on_click=AppState.hide_sidebar,
# # # #                 class_name="absolute top-2 right-2 text-gray-500 hover:text-gray-800",
# # # #             ),
# # # #             rx.el.h3(
# # # #                 "Details",
# # # #                 class_name="text-xl font-bold mb-4",
# # # #             ),
# # # #             rx.cond(
# # # #                 AppState.sidebar_content_type == "engine",
# # # #                 rx.el.div(
# # # #                     rx.el.p(
# # # #                         f"CSTN: {AppState.sidebar_item_details.get('cstn_name', '')}",
# # # #                         class_name="text-sm text-gray-500",
# # # #                     ),
# # # #                     rx.el.p(
# # # #                         f"CFSH: {AppState.sidebar_item_details.get('cfsh_name', '')}",
# # # #                         class_name="text-sm text-gray-500",
# # # #                     ),
# # # #                     rx.el.h4(
# # # #                         f"Engine: {engine_name}",
# # # #                         class_name="text-lg font-semibold my-2",
# # # #                     ),
# # # #                     dropdown("Engine Info", engine_info),
# # # #                     dropdown(
# # # #                         "Configuration",
# # # #                         "Placeholder for configuration details.",
# # # #                     ),
# # # #                     dropdown(
# # # #                         "Metrics",
# # # #                         "Placeholder for performance metrics.",
# # # #                     ),
# # # #                 ),
# # # #                 rx.el.div(
# # # #                     rx.el.p(
# # # #                         f"Group: {AppState.sidebar_item_details.get('group_name', '')}",
# # # #                         class_name="text-sm text-gray-500",
# # # #                     ),
# # # #                     rx.el.h4(
# # # #                         f"Stack: {stack_name}",
# # # #                         class_name="text-lg font-semibold my-2",
# # # #                     ),
# # # #                     dropdown("Stack Info", stack_info),
# # # #                     dropdown(
# # # #                         "Deployment History",
# # # #                         "Placeholder for deployment history.",
# # # #                     ),
# # # #                     dropdown(
# # # #                         "Resources",
# # # #                         "Placeholder for allocated resources.",
# # # #                     ),
# # # #                 ),
# # # #             ),
# # # #             class_name="fixed top-0 right-0 h-full w-80 bg-white shadow-2xl p-6 transform transition-transform duration-300 ease-in-out z-50",
# # # #             style={
# # # #                 "transform": rx.cond(
# # # #                     AppState.sidebar_visible,
# # # #                     "translateX(0)",
# # # #                     "translateX(100%)",
# # # #                 )
# # # #             },
# # # #         ),
# # # #         rx.fragment(),
# # # #     )


# # # # def index() -> rx.Component:
# # # #     return rx.el.div(
# # # #         rx.el.div(
# # # #             rx.el.div(
# # # #                 rx.el.div(
# # # #                     rx.el.h2(
# # # #                         "Selected CSTN: ",
# # # #                         rx.el.span(
# # # #                             AppState.selected_cstn_name,
# # # #                             class_name="text-indigo-600 font-bold",
# # # #                         ),
# # # #                         class_name="text-xl font-semibold text-gray-800",
# # # #                     ),
# # # #                     rx.el.select(
# # # #                         rx.foreach(
# # # #                             AppState.cstn_options,
# # # #                             lambda name: rx.el.option(
# # # #                                 name, value=name
# # # #                             ),
# # # #                         ),
# # # #                         value=AppState.selected_cstn_name,
# # # #                         on_change=AppState.set_cstn_name,
# # # #                         class_name="p-2 border rounded-lg shadow-sm",
# # # #                     ),
# # # #                     class_name="flex items-center justify-between p-4 border-b bg-white",
# # # #                 ),
# # # #                 rx.el.div(
# # # #                     rx.el.div(
# # # #                         rx.foreach(
# # # #                             AppState.current_cfsh_names,
# # # #                             cfsh_item,
# # # #                         ),
# # # #                         class_name="flex flex-wrap gap-4 p-4",
# # # #                     ),
# # # #                     class_name="border-b bg-white",
# # # #                 ),
# # # #                 rx.el.div(
# # # #                     groups_column(),
# # # #                     stacks_column(),
# # # #                     info_column(),
# # # #                     class_name="grid grid-cols-1 md:grid-cols-3 bg-gray-50",
# # # #                 ),
# # # #                 class_name="flex-1 transition-all duration-300 ease-in-out",
# # # #                 style={
# # # #                     "margin_right": rx.cond(
# # # #                         AppState.sidebar_visible,
# # # #                         "20rem",
# # # #                         "0",
# # # #                     )
# # # #                 },
# # # #             ),
# # # #             sidebar(),
# # # #             class_name="relative min-h-screen bg-gray-100 font-['Inter']",
# # # #         )
# # # #     )


# # # # app = rx.App(
# # # #     # head_components=[
# # # #     #     rx.el.link(
# # # #     #         rel="preconnect",
# # # #     #         href="https://fonts.googleapis.com",
# # # #     #     ),
# # # #     #     rx.el.link(
# # # #     #         rel="preconnect",
# # # #     #         href="https://fonts.gstatic.com",
# # # #     #         crossorigin="",
# # # #     #     ),
# # # #     #     rx.el.link(
# # # #     #         href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap",
# # # #     #         rel="stylesheet",
# # # #     #     ),
# # # #     # ],
# # # #     # theme=rx.theme(appearance="light"),
# # # # )
# # # # app.add_page(index)

# # # # ------------------------------------------------------------------------------------------------------------------------------------------


# # # import reflex as rx
# # # from typing import cast

# # # cstn_to_cfsh_data: dict[str, list[str]] = {
# # #     "cstn_alpha": ["cfsh_A", "cfsh_B", "cfsh_C"],
# # #     "cstn_beta": ["cfsh_D", "cfsh_E"],
# # #     "cstn_gamma": ["cfsh_F"],
# # # }
# # # cfsh_to_engine_data: dict[str, list[str]] = {
# # #     "cfsh_A": ["engine_1", "engine_2"],
# # #     "cfsh_B": ["engine_3"],
# # #     "cfsh_C": ["engine_4", "engine_5"],
# # #     "cfsh_D": ["engine_6"],
# # #     "cfsh_E": ["engine_7", "engine_8"],
# # #     "cfsh_F": ["engine_9"],
# # # }
# # # engine_to_group_data: dict[str, list[str]] = {
# # #     "engine_1": ["group_X", "group_Y"],
# # #     "engine_2": ["group_Z"],
# # #     "engine_3": ["group_X", "group_W"],
# # #     "engine_4": ["group_V"],
# # #     "engine_5": ["group_Y", "group_Z"],
# # #     "engine_6": ["group_U"],
# # #     "engine_7": ["group_T"],
# # #     "engine_8": ["group_S", "group_X"],
# # #     "engine_9": ["group_R"],
# # # }
# # # group_to_stack_data: dict[str, list[str]] = {
# # #     "group_X": ["stack_alpha", "stack_beta"],
# # #     "group_Y": ["stack_gamma"],
# # #     "group_Z": ["stack_delta", "stack_epsilon"],
# # #     "group_W": ["stack_zeta"],
# # #     "group_V": ["stack_eta"],
# # #     "group_U": ["stack_theta"],
# # #     "group_T": ["stack_iota"],
# # #     "group_S": ["stack_kappa"],
# # #     "group_R": ["stack_lambda"],
# # # }
# # # engine_status_data: dict[str, str] = {
# # #     "engine_1": "working",
# # #     "engine_2": "stopped",
# # #     "engine_3": "working",
# # #     "engine_4": "working",
# # #     "engine_5": "stopped",
# # #     "engine_6": "working",
# # #     "engine_7": "stopped",
# # #     "engine_8": "working",
# # #     "engine_9": "working",
# # # }


# # # class AppState(rx.State):
# # #     cstn_to_cfsh: dict[str, list[str]] = cstn_to_cfsh_data
# # #     cfsh_to_engine: dict[str, list[str]] = (
# # #         cfsh_to_engine_data
# # #     )
# # #     engine_to_group: dict[str, list[str]] = (
# # #         engine_to_group_data
# # #     )
# # #     group_to_stack: dict[str, list[str]] = (
# # #         group_to_stack_data
# # #     )
# # #     engine_status: dict[str, str] = engine_status_data
# # #     selected_cstn: str = list(cstn_to_cfsh_data.keys())[0]
# # #     selected_cfsh: str = ""
# # #     selected_engine: str = ""
# # #     selected_group: str = ""
# # #     selected_stack: str = ""
# # #     info_tab_toggle: bool = True
# # #     search_query: str = ""

# # #     @rx.var
# # #     def cstn_options(self) -> list[str]:
# # #         return list(self.cstn_to_cfsh.keys())

# # #     @rx.var
# # #     def current_cfsh_names(self) -> list[str]:
# # #         return self.cstn_to_cfsh.get(self.selected_cstn, [])

# # #     @rx.var
# # #     def current_groups(self) -> list[str]:
# # #         groups = []
# # #         if self.selected_engine:
# # #             groups = self.engine_to_group.get(
# # #                 self.selected_engine, []
# # #             )
# # #         elif self.selected_cfsh:
# # #             engines_on_cfsh = self.cfsh_to_engine.get(
# # #                 self.selected_cfsh, []
# # #             )
# # #             for engine in engines_on_cfsh:
# # #                 groups.extend(
# # #                     self.engine_to_group.get(engine, [])
# # #                 )
# # #             groups = sorted(list(set(groups)))
# # #         else:
# # #             all_groups = []
# # #             for group_list in self.engine_to_group.values():
# # #                 all_groups.extend(group_list)
# # #             groups = sorted(list(set(all_groups)))
# # #         if self.search_query:
# # #             return [
# # #                 g
# # #                 for g in groups
# # #                 if self.search_query.lower() in g.lower()
# # #             ]
# # #         return groups

# # #     @rx.var
# # #     def current_stacks(self) -> list[str]:
# # #         if not self.selected_group:
# # #             return []
# # #         return self.group_to_stack.get(
# # #             self.selected_group, []
# # #         )

# # #     @rx.var
# # #     def sidebar_visible(self) -> bool:
# # #         return bool(
# # #             self.selected_engine or self.selected_stack
# # #         )

# # #     def select_cstn(self, name: str):
# # #         self.selected_cstn = name
# # #         self.selected_cfsh = ""
# # #         self.selected_engine = ""
# # #         self.selected_group = ""
# # #         self.selected_stack = ""

# # #     def select_cfsh(self, name: str):
# # #         self.selected_cfsh = name
# # #         self.selected_engine = ""
# # #         self.selected_group = ""
# # #         self.selected_stack = ""

# # #     def select_engine(
# # #         self, engine_name: str, cfsh_name: str
# # #     ):
# # #         self.selected_engine = engine_name
# # #         self.selected_cfsh = cfsh_name
# # #         self.selected_group = ""
# # #         self.selected_stack = ""

# # #     def _find_parent_engine_and_cfsh(
# # #         self, group_name: str
# # #     ) -> tuple[str, str]:
# # #         for engine, groups in self.engine_to_group.items():
# # #             if group_name in groups:
# # #                 for (
# # #                     cfsh,
# # #                     engines,
# # #                 ) in self.cfsh_to_engine.items():
# # #                     if engine in engines:
# # #                         return (engine, cfsh)
# # #         return ("", "")

# # #     def select_group(self, group_name: str):
# # #         engine, cfsh = self._find_parent_engine_and_cfsh(
# # #             group_name
# # #         )
# # #         self.selected_group = group_name
# # #         self.selected_engine = engine
# # #         self.selected_cfsh = cfsh
# # #         self.selected_stack = ""

# # #     def select_stack(self, stack_name: str):
# # #         self.selected_stack = stack_name

# # #     def toggle_info_tab(self):
# # #         self.info_tab_toggle = not self.info_tab_toggle

# # #     def set_search_query(self, query: str):
# # #         self.search_query = query


# # # def sidebar() -> rx.Component:
# # #     return rx.el.aside(
# # #         rx.el.div(
# # #             rx.el.h3(
# # #                 "Details",
# # #                 class_name="text-lg font-semibold text-white mb-4",
# # #             ),
# # #             rx.el.div(
# # #                 rx.el.details(
# # #                     rx.el.summary(
# # #                         f"CSTN: {AppState.selected_cstn}",
# # #                         class_name="font-semibold text-white cursor-pointer",
# # #                     ),
# # #                     rx.el.p(
# # #                         "Details about the cstn...",
# # #                         class_name="text-gray-300 mt-2 text-sm",
# # #                     ),
# # #                     class_name="mb-4",
# # #                 ),
# # #                 rx.el.details(
# # #                     rx.el.summary(
# # #                         f"CFSH: {AppState.selected_cfsh}",
# # #                         class_name="font-semibold text-white cursor-pointer",
# # #                     ),
# # #                     rx.el.p(
# # #                         "Details about the cfsh...",
# # #                         class_name="text-gray-300 mt-2 text-sm",
# # #                     ),
# # #                     class_name="mb-4",
# # #                 ),
# # #                 rx.el.details(
# # #                     rx.el.summary(
# # #                         f"Engine: {AppState.selected_engine}",
# # #                         class_name="font-semibold text-white cursor-pointer",
# # #                     ),
# # #                     rx.el.p(
# # #                         "Details about the engine...",
# # #                         class_name="text-gray-300 mt-2 text-sm",
# # #                     ),
# # #                 ),
# # #                 class_name="space-y-2",
# # #             ),
# # #             class_name="p-4",
# # #         ),
# # #         class_name=rx.cond(
# # #             AppState.sidebar_visible,
# # #             "w-64 bg-gray-800 text-white transition-all duration-300",
# # #             "w-0 transition-all duration-300 overflow-hidden",
# # #         ),
# # #     )


# # # def engine_icon(
# # #     engine_name: str, cfsh_name: str
# # # ) -> rx.Component:
# # #     is_selected = AppState.selected_engine == engine_name
# # #     return rx.el.label(
# # #         rx.el.input(
# # #             type="radio",
# # #             name="engine_selection",
# # #             class_name="hidden",
# # #             on_change=lambda: AppState.select_engine(
# # #                 engine_name, cfsh_name
# # #             ),
# # #             checked=is_selected,
# # #             default_value=engine_name,
# # #         ),
# # #         rx.el.div(
# # #             rx.tooltip(
# # #                 rx.icon(
# # #                     "heart",
# # #                     class_name=rx.cond(
# # #                         AppState.engine_status[engine_name]
# # #                         == "working",
# # #                         "text-green-500",
# # #                         "text-red-500",
# # #                     ),
# # #                 ),
# # #                 content=engine_name,
# # #             ),
# # #             class_name=rx.cond(
# # #                 is_selected,
# # #                 "p-1 rounded-full bg-blue-200 cursor-pointer",
# # #                 "p-1 rounded-full hover:bg-gray-200 cursor-pointer",
# # #             ),
# # #         ),
# # #         class_name="flex items-center",
# # #     )


# # # def top_row() -> rx.Component:
# # #     return rx.el.div(
# # #         rx.el.div(
# # #             rx.el.p(
# # #                 "CSTN:", class_name="font-semibold mr-2"
# # #             ),
# # #             rx.el.p(
# # #                 AppState.selected_cstn,
# # #                 class_name="font-bold text-indigo-600",
# # #             ),
# # #             class_name="flex items-center",
# # #         ),
# # #         rx.el.select(
# # #             rx.foreach(
# # #                 AppState.cstn_options,
# # #                 lambda name: rx.el.option(name, value=name),
# # #             ),
# # #             value=AppState.selected_cstn,
# # #             on_change=AppState.select_cstn,
# # #             class_name="p-2 border rounded-md shadow-sm",
# # #         ),
# # #         class_name="flex justify-between items-center p-4 bg-white rounded-lg shadow",
# # #     )


# # # def cfsh_row() -> rx.Component:
# # #     return rx.el.div(
# # #         rx.foreach(
# # #             AppState.current_cfsh_names,
# # #             lambda cfsh: rx.el.div(
# # #                 rx.el.label(
# # #                     rx.el.input(
# # #                         type="radio",
# # #                         name="cfsh_selection",
# # #                         class_name="mr-2",
# # #                         on_change=lambda: AppState.select_cfsh(
# # #                             cfsh
# # #                         ),
# # #                         checked=AppState.selected_cfsh
# # #                         == cfsh,
# # #                         default_value=cfsh,
# # #                     ),
# # #                     cfsh,
# # #                     class_name="flex items-center font-medium cursor-pointer",
# # #                 ),
# # #                 rx.el.div(
# # #                     rx.foreach(
# # #                         AppState.cfsh_to_engine[cfsh],
# # #                         lambda engine: engine_icon(
# # #                             engine, cfsh
# # #                         ),
# # #                     ),
# # #                     class_name="flex items-center space-x-2 ml-4",
# # #                 ),
# # #                 class_name="flex items-center p-3 bg-gray-50 rounded-md",
# # #             ),
# # #         ),
# # #         class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 p-4",
# # #     )


# # # def groups_column() -> rx.Component:
# # #     return rx.el.div(
# # #         rx.el.h3(
# # #             "Groups",
# # #             class_name="text-lg font-semibold mb-2",
# # #         ),
# # #         rx.el.input(
# # #             placeholder="Search groups...",
# # #             on_change=AppState.set_search_query,
# # #             class_name="w-full p-2 border rounded-md mb-4",
# # #         ),
# # #         rx.el.div(
# # #             rx.foreach(
# # #                 AppState.current_groups,
# # #                 lambda group: rx.el.label(
# # #                     rx.el.input(
# # #                         type="radio",
# # #                         name="group_selection",
# # #                         class_name="mr-2",
# # #                         on_change=lambda: AppState.select_group(
# # #                             group
# # #                         ),
# # #                         checked=AppState.selected_group
# # #                         == group,
# # #                         default_value=group,
# # #                     ),
# # #                     group,
# # #                     class_name="flex items-center p-2 hover:bg-gray-100 rounded-md cursor-pointer",
# # #                 ),
# # #             ),
# # #             class_name="space-y-1 overflow-y-auto h-96",
# # #         ),
# # #         class_name="p-4 bg-white rounded-lg shadow",
# # #     )


# # # def stacks_column() -> rx.Component:
# # #     return rx.el.div(
# # #         rx.el.h3(
# # #             "Stacks",
# # #             class_name="text-lg font-semibold mb-2",
# # #         ),
# # #         rx.el.div(
# # #             rx.cond(
# # #                 AppState.selected_group,
# # #                 rx.foreach(
# # #                     AppState.current_stacks,
# # #                     lambda stack: rx.el.label(
# # #                         rx.el.input(
# # #                             type="radio",
# # #                             name="stack_selection",
# # #                             class_name="mr-2",
# # #                             on_change=lambda: AppState.select_stack(
# # #                                 stack
# # #                             ),
# # #                             checked=AppState.selected_stack
# # #                             == stack,
# # #                             default_value=stack,
# # #                         ),
# # #                         stack,
# # #                         class_name="flex items-center p-2 hover:bg-gray-100 rounded-md cursor-pointer",
# # #                     ),
# # #                 ),
# # #                 rx.el.p(
# # #                     "Select a group to see stacks.",
# # #                     class_name="text-gray-500",
# # #                 ),
# # #             ),
# # #             class_name="space-y-1 overflow-y-auto h-96",
# # #         ),
# # #         class_name="p-4 bg-white rounded-lg shadow",
# # #     )


# # # def info_column() -> rx.Component:
# # #     return rx.el.div(
# # #         rx.el.div(
# # #             rx.el.label(
# # #                 "Toggle Info",
# # #                 class_name="font-medium text-gray-700",
# # #             ),
# # #             rx.el.div(
# # #                 rx.el.span("Tab 1", class_name="mr-2"),
# # #                 rx.el.button(
# # #                     rx.el.div(
# # #                         class_name="w-4 h-4 bg-white rounded-full shadow-md transform transition-transform"
# # #                     ),
# # #                     on_click=AppState.toggle_info_tab,
# # #                     class_name=rx.cond(
# # #                         AppState.info_tab_toggle,
# # #                         "w-12 h-6 flex items-center bg-gray-300 rounded-full p-1 duration-300 ease-in-out",
# # #                         "w-12 h-6 flex items-center bg-blue-500 rounded-full p-1 duration-300 ease-in-out justify-end",
# # #                     ),
# # #                 ),
# # #                 rx.el.span("Tab 2", class_name="ml-2"),
# # #                 class_name="flex items-center",
# # #             ),
# # #             class_name="flex items-center justify-between mb-4",
# # #         ),
# # #         rx.cond(
# # #             AppState.info_tab_toggle,
# # #             rx.el.div(
# # #                 "Displaying info for Tab 1.",
# # #                 class_name="p-4 bg-gray-50 rounded h-80",
# # #             ),
# # #             rx.el.div(
# # #                 "Displaying info for Tab 2.",
# # #                 class_name="p-4 bg-gray-50 rounded h-80",
# # #             ),
# # #         ),
# # #         class_name="p-4 bg-white rounded-lg shadow",
# # #     )


# # # def index() -> rx.Component:
# # #     return rx.el.div(
# # #         sidebar(),
# # #         rx.el.main(
# # #             top_row(),
# # #             cfsh_row(),
# # #             rx.el.div(
# # #                 groups_column(),
# # #                 stacks_column(),
# # #                 info_column(),
# # #                 class_name="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4",
# # #             ),
# # #             class_name="flex-1 p-6",
# # #         ),
# # #         class_name="flex min-h-screen bg-gray-100 font-['Inter']",
# # #     )


# # # app = rx.App(
# # #     theme=rx.theme(appearance="dark"),
# # #     # head_components=[
# # #     #     rx.el.link(
# # #     #         rel="preconnect",
# # #     #         href="https://fonts.googleapis.com",
# # #     #     ),
# # #     #     rx.el.link(
# # #     #         rel="preconnect",
# # #     #         href="https://fonts.gstatic.com",
# # #     #         crossorigin="",
# # #     #     ),
# # #     #     rx.el.link(
# # #     #         href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
# # #     #         rel="stylesheet",
# # #     #     ),
# # #     # ],
# # # )
# # # app.add_page(index, title="Deployment Dashboard")

# # import reflex as rx
# # from typing import cast

# # cstn_to_cfsh_data: dict[str, list[str]] = {
# #     "cstn_alpha": ["cfsh_A", "cfsh_B", "cfsh_C"],
# #     "cstn_beta": ["cfsh_D", "cfsh_E"],
# #     "cstn_gamma": ["cfsh_F"],
# # }
# # cfsh_to_engine_data: dict[str, list[str]] = {
# #     "cfsh_A": ["engine_1", "engine_2"],
# #     "cfsh_B": ["engine_3"],
# #     "cfsh_C": ["engine_4", "engine_5"],
# #     "cfsh_D": ["engine_6"],
# #     "cfsh_E": ["engine_7", "engine_8"],
# #     "cfsh_F": ["engine_9"],
# # }
# # engine_to_group_data: dict[str, list[str]] = {
# #     "engine_1": ["group_X1", "group_Y1"],
# #     "engine_2": ["group_Z2"],
# #     "engine_3": ["group_X3", "group_W3"],
# #     "engine_4": ["group_V4"],
# #     "engine_5": ["group_Y5", "group_Z5"],
# #     "engine_6": ["group_U6"],
# #     "engine_7": ["group_T7"],
# #     "engine_8": ["group_S8", "group_X8"],
# #     "engine_9": ["group_R9"],
# # }
# # group_to_stack_data: dict[str, list[str]] = {
# #     "group_X": ["stack_alpha", "stack_beta"],
# #     "group_Y": ["stack_gamma"],
# #     "group_Z": ["stack_delta", "stack_epsilon"],
# #     "group_W": ["stack_zeta"],
# #     "group_V": ["stack_eta"],
# #     "group_U": ["stack_theta"],
# #     "group_T": ["stack_iota"],
# #     "group_S": ["stack_kappa"],
# #     "group_R": ["stack_lambda"],
# # }
# # engine_status_data: dict[str, str] = {
# #     "engine_1": "working",
# #     "engine_2": "stopped",
# #     "engine_3": "working",
# #     "engine_4": "working",
# #     "engine_5": "stopped",
# #     "engine_6": "working",
# #     "engine_7": "stopped",
# #     "engine_8": "working",
# #     "engine_9": "working",
# # }


# # class AppState(rx.State):
# #     cstn_to_cfsh: dict[str, list[str]] = cstn_to_cfsh_data
# #     cfsh_to_engine: dict[str, list[str]] = (
# #         cfsh_to_engine_data
# #     )
# #     engine_to_group: dict[str, list[str]] = (
# #         engine_to_group_data
# #     )
# #     group_to_stack: dict[str, list[str]] = (
# #         group_to_stack_data
# #     )
# #     engine_status: dict[str, str] = engine_status_data
# #     selected_cstn: str = list(cstn_to_cfsh_data.keys())[0]
# #     selected_cfsh: str = ""
# #     selected_engine: str = ""
# #     selected_group: str = ""
# #     selected_stack: str = ""
# #     info_tab_toggle: bool = True
# #     search_query: str = ""

# #     @rx.var
# #     def cstn_options(self) -> list[str]:
# #         return list(self.cstn_to_cfsh.keys())

# #     @rx.var
# #     def current_cfsh_names(self) -> list[str]:
# #         return self.cstn_to_cfsh.get(self.selected_cstn, [])

# #     @rx.var
# #     def current_groups(self) -> list[str]:
# #         groups = []
# #         if self.selected_engine:
# #             groups = self.engine_to_group.get(
# #                 self.selected_engine, []
# #             )
# #         elif self.selected_cfsh:
# #             engines_on_cfsh = self.cfsh_to_engine.get(
# #                 self.selected_cfsh, []
# #             )
# #             for engine in engines_on_cfsh:
# #                 groups.extend(
# #                     self.engine_to_group.get(engine, [])
# #                 )
# #             groups = sorted(list(set(groups)))
# #         else:
# #             all_groups = []
# #             for group_list in self.engine_to_group.values():
# #                 all_groups.extend(group_list)
# #             groups = sorted(list(set(all_groups)))
# #         if self.search_query:
# #             return [
# #                 g
# #                 for g in groups
# #                 if self.search_query.lower() in g.lower()
# #             ]
# #         return groups

# #     @rx.var
# #     def current_stacks(self) -> list[str]:
# #         if not self.selected_group:
# #             return []
# #         return self.group_to_stack.get(
# #             self.selected_group, []
# #         )

# #     @rx.var
# #     def sidebar_visible(self) -> bool:
# #         return bool(
# #             self.selected_engine or self.selected_stack
# #         )

# #     def select_cstn(self, name: str):
# #         self.selected_cstn = name
# #         self.selected_cfsh = ""
# #         self.selected_engine = ""
# #         self.selected_group = ""
# #         self.selected_stack = ""

# #     def select_cfsh(self, name: str):
# #         if self.selected_cfsh == name:
# #             self.selected_cfsh = ""
# #         else:
# #             self.selected_cfsh = name
# #         self.selected_engine = ""
# #         self.selected_group = ""
# #         self.selected_stack = ""

# #     def select_engine(
# #         self, engine_name: str, cfsh_name: str
# #     ):
# #         if self.selected_engine == engine_name:
# #             self.selected_engine = ""
# #         else:
# #             self.selected_engine = engine_name
# #             self.selected_cfsh = cfsh_name
# #         self.selected_group = ""
# #         self.selected_stack = ""

# #     def _find_parent_engine_and_cfsh(
# #         self, group_name: str
# #     ) -> tuple[str, str]:
# #         for engine, groups in self.engine_to_group.items():
# #             if group_name in groups:
# #                 for (
# #                     cfsh,
# #                     engines,
# #                 ) in self.cfsh_to_engine.items():
# #                     if engine in engines:
# #                         return (engine, cfsh)
# #         return ("", "")

# #     def select_group(self, group_name: str):
# #         if self.selected_group == group_name:
# #             self.selected_group = ""
# #             self.selected_engine = ""
# #             self.selected_cfsh = ""
# #         else:
# #             engine, cfsh = (
# #                 self._find_parent_engine_and_cfsh(
# #                     group_name
# #                 )
# #             )
# #             self.selected_group = group_name
# #             self.selected_engine = engine
# #             self.selected_cfsh = cfsh
# #         self.selected_stack = ""

# #     def select_stack(self, stack_name: str):
# #         if self.selected_stack == stack_name:
# #             self.selected_stack = ""
# #         else:
# #             self.selected_stack = stack_name

# #     def toggle_info_tab(self):
# #         self.info_tab_toggle = not self.info_tab_toggle

# #     def set_search_query(self, query: str):
# #         self.search_query = query


# # def sidebar() -> rx.Component:
# #     return rx.el.aside(
# #         rx.el.div(
# #             rx.el.h3(
# #                 "Details",
# #                 class_name="text-lg font-semibold text-white mb-4",
# #             ),
# #             rx.el.div(
# #                 rx.el.details(
# #                     rx.el.summary(
# #                         f"CSTN: {AppState.selected_cstn}",
# #                         class_name="font-semibold text-white cursor-pointer",
# #                     ),
# #                     rx.el.p(
# #                         "Details about the cstn...",
# #                         class_name="text-gray-300 mt-2 text-sm",
# #                     ),
# #                     class_name="mb-4",
# #                 ),
# #                 rx.el.details(
# #                     rx.el.summary(
# #                         f"CFSH: {AppState.selected_cfsh}",
# #                         class_name="font-semibold text-white cursor-pointer",
# #                     ),
# #                     rx.el.p(
# #                         "Details about the cfsh...",
# #                         class_name="text-gray-300 mt-2 text-sm",
# #                     ),
# #                     class_name="mb-4",
# #                 ),
# #                 rx.el.details(
# #                     rx.el.summary(
# #                         f"Engine: {AppState.selected_engine}",
# #                         class_name="font-semibold text-white cursor-pointer",
# #                     ),
# #                     rx.el.p(
# #                         "Details about the engine...",
# #                         class_name="text-gray-300 mt-2 text-sm",
# #                     ),
# #                 ),
# #                 class_name="space-y-2",
# #             ),
# #             class_name="p-4",
# #         ),
# #         class_name=rx.cond(
# #             AppState.sidebar_visible,
# #             "w-64 bg-gray-800 text-white transition-all duration-300",
# #             "w-0 transition-all duration-300 overflow-hidden",
# #         ),
# #     )


# # def engine_icon(
# #     engine_name: str, cfsh_name: str
# # ) -> rx.Component:
# #     is_selected = AppState.selected_engine == engine_name
# #     return rx.el.label(
# #         rx.el.input(
# #             type="radio",
# #             name="engine_selection",
# #             class_name="hidden",
# #             on_click=lambda: AppState.select_engine(
# #                 engine_name, cfsh_name
# #             ),
# #             checked=is_selected,
# #             default_value=engine_name,
# #         ),
# #         rx.el.div(
# #             rx.tooltip(
# #                 rx.icon(
# #                     "heart",
# #                     class_name=rx.cond(
# #                         AppState.engine_status[engine_name]
# #                         == "working",
# #                         "text-green-500",
# #                         "text-red-500",
# #                     ),
# #                 ),
# #                 content=engine_name,
# #             ),
# #             class_name=rx.cond(
# #                 is_selected,
# #                 "p-1 rounded-full bg-blue-200 cursor-pointer",
# #                 "p-1 rounded-full hover:bg-gray-200 cursor-pointer",
# #             ),
# #         ),
# #         class_name="flex items-center",
# #     )


# # def top_row() -> rx.Component:
# #     return rx.el.div(
# #         rx.el.div(
# #             rx.el.p(
# #                 "CSTN:", class_name="font-semibold mr-2"
# #             ),
# #             rx.el.p(
# #                 AppState.selected_cstn,
# #                 class_name="font-bold text-indigo-600",
# #             ),
# #             class_name="flex items-center",
# #         ),
# #         rx.el.select(
# #             rx.foreach(
# #                 AppState.cstn_options,
# #                 lambda name: rx.el.option(name, value=name),
# #             ),
# #             value=AppState.selected_cstn,
# #             on_change=AppState.select_cstn,
# #             class_name="p-2 border rounded-md shadow-sm",
# #         ),
# #         class_name="flex justify-between items-center p-4 bg-white rounded-lg shadow",
# #     )


# # def cfsh_row() -> rx.Component:
# #     return rx.el.div(
# #         rx.foreach(
# #             AppState.current_cfsh_names,
# #             lambda cfsh: rx.el.div(
# #                 rx.el.label(
# #                     rx.el.input(
# #                         type="radio",
# #                         name="cfsh_selection",
# #                         class_name="mr-2",
# #                         on_click=lambda: AppState.select_cfsh(
# #                             cfsh
# #                         ),
# #                         checked=AppState.selected_cfsh
# #                         == cfsh,
# #                         default_value=cfsh,
# #                     ),
# #                     cfsh,
# #                     class_name="flex items-center font-medium cursor-pointer",
# #                 ),
# #                 rx.el.div(
# #                     rx.foreach(
# #                         AppState.cfsh_to_engine[cfsh],
# #                         lambda engine: engine_icon(
# #                             engine, cfsh
# #                         ),
# #                     ),
# #                     class_name="flex items-center space-x-2 ml-4",
# #                 ),
# #                 class_name="flex items-center p-3 bg-gray-50 rounded-md",
# #             ),
# #         ),
# #         class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 p-4",
# #     )


# # def groups_column() -> rx.Component:
# #     return rx.el.div(
# #         rx.el.h3(
# #             "Groups",
# #             class_name="text-lg font-semibold mb-2",
# #         ),
# #         rx.el.input(
# #             placeholder="Search groups...",
# #             on_change=AppState.set_search_query,
# #             class_name="w-full p-2 border rounded-md mb-4",
# #         ),
# #         rx.el.div(
# #             rx.foreach(
# #                 AppState.current_groups,
# #                 lambda group: rx.el.label(
# #                     rx.el.input(
# #                         type="radio",
# #                         name="group_selection",
# #                         class_name="mr-2",
# #                         on_click=lambda: AppState.select_group(
# #                             group
# #                         ),
# #                         checked=AppState.selected_group
# #                         == group,
# #                         default_value=group,
# #                     ),
# #                     group,
# #                     class_name="flex items-center p-2 hover:bg-gray-100 rounded-md cursor-pointer",
# #                 ),
# #             ),
# #             class_name="space-y-1 overflow-y-auto h-96",
# #         ),
# #         class_name="p-4 bg-white rounded-lg shadow",
# #     )


# # def stacks_column() -> rx.Component:
# #     return rx.el.div(
# #         rx.el.h3(
# #             "Stacks",
# #             class_name="text-lg font-semibold mb-2",
# #         ),
# #         rx.el.div(
# #             rx.cond(
# #                 AppState.selected_group,
# #                 rx.foreach(
# #                     AppState.current_stacks,
# #                     lambda stack: rx.el.label(
# #                         rx.el.input(
# #                             type="radio",
# #                             name="stack_selection",
# #                             class_name="mr-2",
# #                             on_click=lambda: AppState.select_stack(
# #                                 stack
# #                             ),
# #                             checked=AppState.selected_stack
# #                             == stack,
# #                             default_value=stack,
# #                         ),
# #                         stack,
# #                         class_name="flex items-center p-2 hover:bg-gray-100 rounded-md cursor-pointer",
# #                     ),
# #                 ),
# #                 rx.el.p(
# #                     "Select a group to see stacks.",
# #                     class_name="text-gray-500",
# #                 ),
# #             ),
# #             class_name="space-y-1 overflow-y-auto h-96",
# #         ),
# #         class_name="p-4 bg-white rounded-lg shadow",
# #     )


# # def info_column() -> rx.Component:
# #     return rx.el.div(
# #         rx.el.div(
# #             rx.el.label(
# #                 "Toggle Info",
# #                 class_name="font-medium text-gray-700",
# #             ),
# #             rx.el.div(
# #                 rx.el.span("Tab 1", class_name="mr-2"),
# #                 rx.el.button(
# #                     rx.el.div(
# #                         class_name="w-4 h-4 bg-white rounded-full shadow-md transform transition-transform"
# #                     ),
# #                     on_click=AppState.toggle_info_tab,
# #                     class_name=rx.cond(
# #                         AppState.info_tab_toggle,
# #                         "w-12 h-6 flex items-center bg-gray-300 rounded-full p-1 duration-300 ease-in-out",
# #                         "w-12 h-6 flex items-center bg-blue-500 rounded-full p-1 duration-300 ease-in-out justify-end",
# #                     ),
# #                 ),
# #                 rx.el.span("Tab 2", class_name="ml-2"),
# #                 class_name="flex items-center",
# #             ),
# #             class_name="flex items-center justify-between mb-4",
# #         ),
# #         rx.cond(
# #             AppState.info_tab_toggle,
# #             rx.el.div(
# #                 "Displaying info for Tab 1.",
# #                 class_name="p-4 bg-gray-50 rounded h-80",
# #             ),
# #             rx.el.div(
# #                 "Displaying info for Tab 2.",
# #                 class_name="p-4 bg-gray-50 rounded h-80",
# #             ),
# #         ),
# #         class_name="p-4 bg-white rounded-lg shadow",
# #     )


# # def index() -> rx.Component:
# #     return rx.el.div(
# #         sidebar(),
# #         rx.el.main(
# #             top_row(),
# #             cfsh_row(),
# #             rx.el.div(
# #                 groups_column(),
# #                 stacks_column(),
# #                 info_column(),
# #                 class_name="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4",
# #             ),
# #             class_name="flex-1 p-6",
# #         ),
# #         class_name="flex min-h-screen bg-gray-100 font-['Inter']",
# #     )


# # app = rx.App(
# #     theme=rx.theme(appearance="light"),
# #     head_components=[
# #         rx.el.link(
# #             rel="preconnect",
# #             href="https://fonts.googleapis.com",
# #         ),
# #         rx.el.link(
# #             rel="preconnect",
# #             href="https://fonts.gstatic.com",
# #             crossorigin="",
# #         ),
# #         rx.el.link(
# #             href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
# #             rel="stylesheet",
# #         ),
# #     ],
# # )
# # app.add_page(index, title="Deployment Dashboard")

# # ------------------------------------------------------------------------------------------------------------------------------------------

# import reflex as rx
# from typing import cast

# cstn_to_cfsh_data: dict[str, list[str]] = {
#     "cstn_alpha": ["cfsh_A", "cfsh_B", "cfsh_C"],
#     "cstn_beta": ["cfsh_D", "cfsh_E"],
#     "cstn_gamma": ["cfsh_F"],
# }
# cfsh_to_engine_data: dict[str, list[str]] = {
#     "cfsh_A": ["engine_1", "engine_2"],
#     "cfsh_B": ["engine_3"],
#     "cfsh_C": ["engine_4", "engine_5"],
#     "cfsh_D": ["engine_6"],
#     "cfsh_E": ["engine_7", "engine_8"],
#     "cfsh_F": ["engine_9"],
# }
# engine_to_group_data: dict[str, list[str]] = {
#     "engine_1": ["group_X1", "group_Y1"],
#     "engine_2": ["group_Z2"],
#     "engine_3": ["group_X3", "group_W3"],
#     "engine_4": ["group_V4"],
#     "engine_5": ["group_Y5", "group_Z5"],
#     "engine_6": ["group_U6"],
#     "engine_7": ["group_T7"],
#     "engine_8": ["group_S8", "group_X8"],
#     "engine_9": ["group_R9"],
# }
# group_to_stack_data: dict[str, list[str]] = {
#     "group_X1": ["stack_alpha_X", "stack_beta_X"],
#     "group_Y1": ["stack_gamma_Y"],
#     "group_Z2": ["stack_delta_Z", "stack_epsilon_Z"],
#     "group_W": ["stack_zeta_W"],
#     "group_V4": ["stack_eta_V"],
#     "group_U": ["stack_theta_U"],
#     "group_T": ["stack_iota_T"],
#     "group_S": ["stack_kappa_S"],
#     "group_R": ["stack_lambda_R"],
# }
# engine_status_data: dict[str, str] = {
#     "engine_1": "working",
#     "engine_2": "stopped",
#     "engine_3": "working",
#     "engine_4": "working",
#     "engine_5": "stopped",
#     "engine_6": "working",
#     "engine_7": "stopped",
#     "engine_8": "working",
#     "engine_9": "working",
# }


# class AppState(rx.State):
#     cstn_to_cfsh: dict[str, list[str]] = cstn_to_cfsh_data
#     cfsh_to_engine: dict[str, list[str]] = (
#         cfsh_to_engine_data
#     )
#     engine_to_group: dict[str, list[str]] = (
#         engine_to_group_data
#     )
#     group_to_stack: dict[str, list[str]] = (
#         group_to_stack_data
#     )
#     engine_status: dict[str, str] = engine_status_data
#     selected_cstn: str = list(cstn_to_cfsh_data.keys())[0]
#     selected_cfsh: str = ""
#     selected_engine: str = ""
#     selected_group: str = ""
#     selected_stack: str = ""
#     info_tab_toggle: bool = True
#     search_query: str = ""
#     sidebar_open: bool = False

#     @rx.var
#     def cstn_options(self) -> list[str]:
#         return list(self.cstn_to_cfsh.keys())

#     @rx.var
#     def current_cfsh_names(self) -> list[str]:
#         return self.cstn_to_cfsh.get(self.selected_cstn, [])

#     @rx.var
#     def current_groups(self) -> list[str]:
#         groups = set()
#         if self.selected_engine:
#             groups.update(
#                 self.engine_to_group.get(
#                     self.selected_engine, []
#                 )
#             )
#         elif self.selected_cfsh:
#             engines_on_cfsh = self.cfsh_to_engine.get(
#                 self.selected_cfsh, []
#             )
#             for engine in engines_on_cfsh:
#                 groups.update(
#                     self.engine_to_group.get(engine, [])
#                 )
#         else:
#             cfsh_names = self.cstn_to_cfsh.get(
#                 self.selected_cstn, []
#             )
#             for cfsh in cfsh_names:
#                 engines_on_cfsh = self.cfsh_to_engine.get(
#                     cfsh, []
#                 )
#                 for engine in engines_on_cfsh:
#                     groups.update(
#                         self.engine_to_group.get(engine, [])
#                     )
#         sorted_groups = sorted(list(groups))
#         if self.search_query:
#             return [
#                 g
#                 for g in sorted_groups
#                 if self.search_query.lower() in g.lower()
#             ]
#         return sorted_groups

#     @rx.var
#     def current_stacks(self) -> list[str]:
#         if not self.selected_group:
#             return []
#         return self.group_to_stack.get(
#             self.selected_group, []
#         )

#     def open_sidebar(self):
#         self.sidebar_open = True

#     def close_sidebar(self):
#         self.sidebar_open = False

#     def select_cstn(self, name: str):
#         self.selected_cstn = name
#         self.selected_cfsh = ""
#         self.selected_engine = ""
#         self.selected_group = ""
#         self.selected_stack = ""
#         self.sidebar_open = False

#     def select_cfsh(self, name: str):
#         if self.selected_cfsh == name:
#             self.selected_cfsh = ""
#         else:
#             self.selected_cfsh = name
#         self.selected_engine = ""
#         self.selected_group = ""
#         self.selected_stack = ""
#         self.sidebar_open = False

#     def select_engine(
#         self, engine_name: str, cfsh_name: str
#     ):
#         if self.selected_engine == engine_name:
#             self.selected_engine = ""
#         else:
#             self.selected_engine = engine_name
#             self.selected_cfsh = cfsh_name
#             self.sidebar_open = True
#         self.selected_group = ""
#         self.selected_stack = ""

#     def _find_parent_engine_and_cfsh(
#         self, group_name: str
#     ) -> tuple[str, str]:
#         for engine, groups in self.engine_to_group.items():
#             if group_name in groups:
#                 for (
#                     cfsh,
#                     engines,
#                 ) in self.cfsh_to_engine.items():
#                     if engine in engines:
#                         return (engine, cfsh)
#         return ("", "")

#     def select_group(self, group_name: str):
#         if self.selected_group == group_name:
#             self.selected_group = ""
#             self.selected_engine = ""
#             self.selected_cfsh = ""
#         else:
#             engine, cfsh = (
#                 self._find_parent_engine_and_cfsh(
#                     group_name
#                 )
#             )
#             self.selected_group = group_name
#             self.selected_engine = engine
#             self.selected_cfsh = cfsh
#         self.selected_stack = ""
#         self.sidebar_open = False

#     def select_stack(self, stack_name: str):
#         if self.selected_stack == stack_name:
#             self.selected_stack = ""
#         else:
#             self.selected_stack = stack_name
#             self.sidebar_open = True

#     def toggle_info_tab(self):
#         self.info_tab_toggle = not self.info_tab_toggle

#     def set_search_query(self, query: str):
#         self.search_query = query


# def sidebar() -> rx.Component:
#     return rx.el.div(
#         rx.el.aside(
#             rx.el.div(
#                 rx.el.div(
#                     rx.el.h3(
#                         "Details",
#                         class_name="text-lg font-semibold text-white",
#                     ),
#                     rx.el.button(
#                         rx.icon(
#                             tag="x", class_name="text-white"
#                         ),
#                         on_click=AppState.close_sidebar,
#                         class_name="p-1 rounded-full hover:bg-gray-700",
#                     ),
#                     class_name="flex justify-between items-center mb-4",
#                 ),
#                 rx.el.div(
#                     rx.el.details(
#                         rx.el.summary(
#                             f"CSTN: {AppState.selected_cstn}",
#                             class_name="font-semibold text-white cursor-pointer",
#                         ),
#                         rx.el.p(
#                             "Details about the cstn...",
#                             class_name="text-gray-300 mt-2 text-sm",
#                         ),
#                         class_name="mb-4",
#                     ),
#                     rx.el.details(
#                         rx.el.summary(
#                             f"CFSH: {AppState.selected_cfsh}",
#                             class_name="font-semibold text-white cursor-pointer",
#                         ),
#                         rx.el.p(
#                             "Details about the cfsh...",
#                             class_name="text-gray-300 mt-2 text-sm",
#                         ),
#                         class_name="mb-4",
#                     ),
#                     rx.el.details(
#                         rx.el.summary(
#                             f"Engine: {AppState.selected_engine}",
#                             class_name="font-semibold text-white cursor-pointer",
#                         ),
#                         rx.el.p(
#                             "Details about the engine...",
#                             class_name="text-gray-300 mt-2 text-sm",
#                         ),
#                     ),
#                     class_name="space-y-2",
#                 ),
#                 class_name="p-4",
#             ),
#             class_name="w-64 bg-gray-800 text-white h-full",
#         ),
#         class_name=rx.cond(
#             AppState.sidebar_open,
#             "fixed top-0 right-0 h-full bg-gray-800 text-white transition-transform transform translate-x-0 duration-300 z-50",
#             "fixed top-0 right-0 h-full bg-gray-800 text-white transition-transform transform translate-x-full duration-300 z-50",
#         ),
#     )


# def engine_icon(
#     engine_name: str, cfsh_name: str
# ) -> rx.Component:
#     is_selected = AppState.selected_engine == engine_name
#     return rx.el.label(
#         rx.el.input(
#             type="radio",
#             name="engine_selection",
#             class_name="hidden",
#             on_click=lambda: AppState.select_engine(
#                 engine_name, cfsh_name
#             ),
#             checked=is_selected,
#             default_value=engine_name,
#         ),
#         rx.el.div(
#             rx.tooltip(
#                 rx.icon(
#                     "heart",
#                     class_name=rx.cond(
#                         AppState.engine_status[engine_name]
#                         == "working",
#                         "text-green-500",
#                         "text-red-500",
#                     ),
#                 ),
#                 content=engine_name,
#             ),
#             class_name=rx.cond(
#                 is_selected,
#                 "p-1 rounded-full bg-blue-200 cursor-pointer",
#                 "p-1 rounded-full hover:bg-gray-200 cursor-pointer",
#             ),
#         ),
#         class_name="flex items-center",
#     )


# def top_row() -> rx.Component:
#     return rx.el.div(
#         rx.el.div(
#             rx.el.p(
#                 "CSTN:", class_name="font-semibold mr-2"
#             ),
#             rx.el.p(
#                 AppState.selected_cstn,
#                 class_name="font-bold text-indigo-600",
#             ),
#             class_name="flex items-center",
#         ),
#         rx.el.select(
#             rx.foreach(
#                 AppState.cstn_options,
#                 lambda name: rx.el.option(name, value=name),
#             ),
#             value=AppState.selected_cstn,
#             on_change=AppState.select_cstn,
#             class_name="p-2 border rounded-md shadow-sm",
#         ),
#         class_name="flex justify-between items-center p-4 bg-white rounded-lg shadow",
#     )


# def cfsh_row() -> rx.Component:
#     return rx.el.div(
#         rx.foreach(
#             AppState.current_cfsh_names,
#             lambda cfsh: rx.el.div(
#                 rx.el.label(
#                     rx.el.input(
#                         type="radio",
#                         name="cfsh_selection",
#                         class_name="mr-2",
#                         on_click=lambda: AppState.select_cfsh(
#                             cfsh
#                         ),
#                         checked=AppState.selected_cfsh
#                         == cfsh,
#                         default_value=cfsh,
#                     ),
#                     cfsh,
#                     class_name="flex items-center font-medium cursor-pointer",
#                 ),
#                 rx.el.div(
#                     rx.foreach(
#                         AppState.cfsh_to_engine[cfsh],
#                         lambda engine: engine_icon(
#                             engine, cfsh
#                         ),
#                     ),
#                     class_name="flex items-center space-x-2 ml-4",
#                 ),
#                 class_name="flex items-center p-3 bg-gray-50 rounded-md",
#             ),
#         ),
#         class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 p-4",
#     )


# def groups_column() -> rx.Component:
#     return rx.el.div(
#         rx.el.h3(
#             "Groups",
#             class_name="text-lg font-semibold mb-2",
#         ),
#         rx.el.input(
#             placeholder="Search groups...",
#             on_change=AppState.set_search_query,
#             class_name="w-full p-2 border rounded-md mb-4",
#         ),
#         rx.el.div(
#             rx.foreach(
#                 AppState.current_groups,
#                 lambda group: rx.el.label(
#                     rx.el.input(
#                         type="radio",
#                         name="group_selection",
#                         class_name="mr-2",
#                         on_click=lambda: AppState.select_group(
#                             group
#                         ),
#                         checked=AppState.selected_group
#                         == group,
#                         default_value=group,
#                     ),
#                     group,
#                     class_name="flex items-center p-2 hover:bg-gray-100 rounded-md cursor-pointer",
#                 ),
#             ),
#             class_name="space-y-1 overflow-y-auto h-96",
#         ),
#         class_name="p-4 bg-white rounded-lg shadow",
#     )


# def stacks_column() -> rx.Component:
#     return rx.el.div(
#         rx.el.h3(
#             "Stacks",
#             class_name="text-lg font-semibold mb-2",
#         ),
#         rx.el.div(
#             rx.cond(
#                 AppState.selected_group,
#                 rx.foreach(
#                     AppState.current_stacks,
#                     lambda stack: rx.el.label(
#                         rx.el.input(
#                             type="radio",
#                             name="stack_selection",
#                             class_name="mr-2",
#                             on_click=lambda: AppState.select_stack(
#                                 stack
#                             ),
#                             checked=AppState.selected_stack
#                             == stack,
#                             default_value=stack,
#                         ),
#                         stack,
#                         class_name="flex items-center p-2 hover:bg-gray-100 rounded-md cursor-pointer",
#                     ),
#                 ),
#                 rx.el.p(
#                     "Select a group to see stacks.",
#                     class_name="text-gray-500",
#                 ),
#             ),
#             class_name="space-y-1 overflow-y-auto h-96",
#         ),
#         class_name="p-4 bg-white rounded-lg shadow",
#     )


# def info_column() -> rx.Component:
#     return rx.el.div(
#         rx.el.div(
#             rx.el.label(
#                 "Toggle Info",
#                 class_name="font-medium text-gray-700",
#             ),
#             rx.el.div(
#                 rx.el.span("Tab 1", class_name="mr-2"),
#                 rx.el.button(
#                     rx.el.div(
#                         class_name="w-4 h-4 bg-white rounded-full shadow-md transform transition-transform"
#                     ),
#                     on_click=AppState.toggle_info_tab,
#                     class_name=rx.cond(
#                         AppState.info_tab_toggle,
#                         "w-12 h-6 flex items-center bg-gray-300 rounded-full p-1 duration-300 ease-in-out",
#                         "w-12 h-6 flex items-center bg-blue-500 rounded-full p-1 duration-300 ease-in-out justify-end",
#                     ),
#                 ),
#                 rx.el.span("Tab 2", class_name="ml-2"),
#                 class_name="flex items-center",
#             ),
#             class_name="flex items-center justify-between mb-4",
#         ),
#         rx.cond(
#             AppState.info_tab_toggle,
#             rx.el.div(
#                 "Displaying info for Tab 1.",
#                 class_name="p-4 bg-gray-50 rounded h-80",
#             ),
#             rx.el.div(
#                 "Displaying info for Tab 2.",
#                 class_name="p-4 bg-gray-50 rounded h-80",
#             ),
#         ),
#         class_name="p-4 bg-white rounded-lg shadow",
#     )


# def index() -> rx.Component:
#     return rx.el.div(
#         rx.el.div(
#             sidebar(),
#             rx.el.main(
#                 top_row(),
#                 cfsh_row(),
#                 rx.el.div(
#                     groups_column(),
#                     stacks_column(),
#                     info_column(),
#                     class_name="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4",
#                 ),
#                 class_name="flex-1 p-6",
#             ),
#             class_name="flex flex-1",
#         ),
#         class_name="min-h-screen bg-gray-100 font-['Inter']",
#     )


# app = rx.App(
#     theme=rx.theme(appearance="light"),
#     # head_components=[
#     #     rx.el.link(
#     #         rel="preconnect",
#     #         href="https://fonts.googleapis.com",
#     #     ),
#     #     rx.el.link(
#     #         rel="preconnect",
#     #         href="https://fonts.gstatic.com",
#     #         crossorigin="",
#     #     ),
#     #     rx.el.link(
#     #         href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
#     #         rel="stylesheet",
#     #     ),
#     # ],
# )
# app.add_page(index, title="Deployment Dashboard")

# # # # ------------------------------------------------------------------------------------------------------------------------------------------
  


import reflex as rx
from typing import cast

cstn_to_cfsh_data: dict[str, list[str]] = {
    "cstn_alpha": ["cfsh_A", "cfsh_B", "cfsh_C"],
    "cstn_beta": ["cfsh_D", "cfsh_E"],
    "cstn_gamma": ["cfsh_F"],
}
cfsh_to_engine_data: dict[str, list[str]] = {
    "cfsh_A": ["engine_1", "engine_2"],
    "cfsh_B": ["engine_3"],
    "cfsh_C": ["engine_4", "engine_5"],
    "cfsh_D": ["engine_6"],
    "cfsh_E": ["engine_7", "engine_8"],
    "cfsh_F": ["engine_9"],
}
engine_to_group_data: dict[str, list[str]] = {
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
group_to_stack_data: dict[str, list[str]] = {
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
engine_status_data: dict[str, str] = {
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
    cstn_to_cfsh: dict[str, list[str]] = cstn_to_cfsh_data
    cfsh_to_engine: dict[str, list[str]] = (
        cfsh_to_engine_data
    )
    engine_to_group: dict[str, list[str]] = (
        engine_to_group_data
    )
    group_to_stack: dict[str, list[str]] = (
        group_to_stack_data
    )
    engine_status: dict[str, str] = engine_status_data
    selected_cstn: str = list(cstn_to_cfsh_data.keys())[0]
    selected_cfsh: str = ""
    selected_engine: str = ""
    selected_group: str = ""
    selected_stack: str = ""
    info_tab_toggle: bool = True
    search_query: str = ""
    sidebar_open: bool = False

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
                rx.el.div(
                    rx.icon(
                        "heart",
                        class_name=rx.cond(
                            AppState.engine_status[engine_name]
                            == "working",
                            "text-green-500",
                            "text-red-500",
                        ),
                    ),
                    rx.el.sub(
                        AppState.engine_to_group[engine_name].length(),
                        class_name="font-bold text-xs",
                    ),
                    class_name="flex items-baseline space-x-0.5",
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
        rx.el.select(
            rx.foreach(
                AppState.cstn_options,
                lambda name: rx.el.option(name, value=name),
            ),
            value=AppState.selected_cstn,
            on_change=AppState.select_cstn,
            class_name="p-2 border rounded-md shadow-sm",
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
                    class_name="flex items-center font-medium cursor-pointer",
                ),
                rx.el.div(
                    rx.foreach(
                        AppState.cfsh_to_engine[cfsh],
                        lambda engine: engine_icon(
                            engine, cfsh
                        ),
                    ),
                    class_name="flex items-center space-x-2 ml-4",
                ),
                class_name="flex items-center p-3 bg-gray-50 rounded-md",
            ),
        ),
        class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 p-4",
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


def index() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            sidebar(),
            rx.el.main(
                top_row(),
                cfsh_row(),
                rx.el.div(
                    groups_column(),
                    stacks_column(),
                    info_column(),
                    class_name="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4",
                ),
                class_name="flex-1 p-6",
            ),
            class_name="flex flex-1",
        ),
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
