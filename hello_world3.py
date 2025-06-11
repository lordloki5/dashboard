import reflex as rx

# Mock data dictionaries (mappings as described in the prompt)
cstn_to_cfsh = {
    "customer1": ["cfsh1", "cfsh2", "cfsh3"],
    "customer2": ["cfsh4", "cfsh5"],
    # ... add more as needed
}
cfsh_to_engines = {
    "cfsh1": ["engineA", "engineB"],
    "cfsh2": ["engineC"],
    "cfsh3": ["engineD", "engineE", "engineF"],
    "cfsh4": ["engineG"],
    "cfsh5": ["engineH", "engineI"],
    # ... etc.
}
engine_to_groups = {
    "engineA": ["group1", "group3"],
    "engineB": ["group2"],
    "engineC": ["group4"],
    "engineD": ["group1", "group2"],
    "engineE": ["group3"],
    "engineF": ["group4"],
    "engineG": ["group2"],
    "engineH": ["group1"],
    "engineI": ["group3", "group4"],
    # ... etc.
}
group_to_stacks = {
    "group1": ["stack1", "stack2", "stack3"],
    "group2": ["stack4", "stack5"],
    "group3": ["stack6"],
    "group4": ["stack7", "stack8"],
    # ... etc.
}

class State(rx.State):
    # Selected values for each category
    cstn_name: str = list(cstn_to_cfsh.keys())[0]  # default to first customer
    selected_cfsh: str = ""
    selected_engine: str = ""
    selected_group: str = ""
    selected_stack: str = ""
    search_text: str = ""           # for filtering group list
    details_toggle: bool = False    # False = summary view, True = detailed view
    sidebar_visible: bool = True    # controls sidebar visibility (open/close)

    # Computed list of cfsh for current cstn
    @rx.var
    def cfsh_list(self) -> list[str]:
        return cstn_to_cfsh.get(self.cstn_name, [])

    # Computed filter for group list based on search text
    @rx.var
    def filtered_groups(self) -> list[str]:
        groups = list(group_to_stacks.keys())
        if not self.search_text:
            return groups
        # case-insensitive filtering by substring
        return [g for g in groups if self.search_text.lower() in g.lower()]

    # Computed summary strings for selections
    @rx.var
    def selected_cfsh_str(self) -> str:
        # Combine explicitly selected CFSHs and any CFSH that contains a selected engine
        if not self.selected_cfsh and not self.selected_engines:
            return "None"
        cfsh_set = set(self.selected_cfsh)
        for eng in self.selected_engines:
            for cfsh, engines in cfsh_to_engines.items():
                if eng in engines:
                    cfsh_set.add(cfsh)
        if not cfsh_set:
            return "None"
        return ", ".join(sorted(cfsh_set))

    @rx.var
    def selected_engines_str(self) -> str:
        if not self.selected_engines:
            return "None"
        return ", ".join(sorted(self.selected_engines))

    @rx.var
    def selected_group_str(self) -> str:
        return self.selected_group if self.selected_group else "None"

    @rx.var
    def selected_stack_str(self) -> str:
        return self.selected_stack if self.selected_stack else "None"

    # Event handler to set a new cstn (from dropdown)
    def set_cstn(self, new_cstn: str):
        self.cstn_name = new_cstn
        # Clear dependent selections when customer changes
        self.selected_cfsh.clear()
        self.selected_engines.clear()
        self.selected_group = ""
        self.selected_stack = ""
        # (We keep sidebar open/closed as is, but could close it since context changed)

    # Toggle a CFSH checkbox
    def toggle_cfsh(self, cfsh_name: str, checked: bool):
        self.selected_cfsh = cfsh_name if checked else ""
        # (Optionally, could open sidebar if needed, but requirement triggers on engine or stack only)

    # Toggle an Engine checkbox (with its CFSH context)
    def toggle_engine(self, engine_name: str, cfsh_name: str, checked: bool):
        self.selected_engine = engine_name if checked else ""
        if checked:
            self.sidebar_visible = True
        # Note: we do not auto-add cfsh_name to selected_cfsh here, 
        # because summary and details will derive it anyway for display.

    # Selecting a group (treated as single-select radio behavior)
    def set_selected_group(self, group: str):
        if group: 
            # if choosing a new group, set it and clear previous stack selection
            self.selected_group = group
            self.selected_stack = ""
            # Also clear any engine selections, since now focusing on stack path
            # (Optional: decide if engines should be cleared or can coexist. Here we clear for clarity.)
            self.selected_engines.clear()
            self.selected_cfsh.clear()
            # Ensure sidebar is not closed if group selected (we might wait until stack is picked to open)
        else:
            # If unchecking the group, clear it
            self.selected_group = ""
            self.selected_stack = ""
        # Note: We enforce only one group at a time via the checked property in UI.

    # Selecting a stack from dropdown
    def set_selected_stack(self, stack: str):
        self.selected_stack = stack
        if stack:
            # When a stack is selected, open the sidebar to show details
            self.sidebar_visible = True

    # Toggle the details view (summary <-> detailed)
    def toggle_details_view(self, checked: bool):
        # The switch on_change will pass a boolean 'checked' state
        self.details_toggle = checked

    # Close the sidebar
    def close_sidebar(self):
        self.sidebar_visible = False

# Define the UI structure
@rx.page()
def index():
    # Top row: CSTN label and dropdown
    top_bar = rx.hstack(
        rx.text("CSTN:", font_weight="bold"),
        rx.select(
            items=list(cstn_to_cfsh.keys()),
            value=State.cstn_name,
            on_change=State.set_cstn
        ),
        padding="1em",
        justify="start",
        align_items="center",
    )

    # Second row: CFSH Instances heading and list
    cfsh_list_section = rx.vstack(
        rx.heading("CFSH Instances:", font_size="1.2em", margin_bottom="0.5em"),
        # Dynamically list CFSH and engines
        rx.foreach(
            State.cfsh_list,
            lambda cfsh: rx.hstack(
                rx.checkbox(
                    text=cfsh,
                    checked=State.selected_cfsh == cfsh,  # if cfsh in selected list string (quick way to bind)
                    # Alternatively, we might compare against State.selected_cfsh set via computed, but using string mapping for simplicity.
                    on_change=lambda checked, cf=cfsh: State.toggle_cfsh(cf, checked)
                ),
                # Engine icons with checkboxes for each engine in this cfsh
                *[
                    rx.tooltip(
                        rx.hstack(
                            rx.checkbox(
                                # no text label, just a checkbox for engine
                                checked=State.selected_engine == engine,
                                on_change=lambda checked, e=engine, cf=cfsh: State.toggle_engine(e, cf, checked),
                                # make engine checkbox smaller for aesthetics
                                size="1",
                                margin_right="0.2em"
                            ),
                            rx.icon(tag="heart", color="red")  # heart icon
                        ),
                        content=engine,
                    )
                    for engine in cfsh_to_engines.get(cfsh, [])
                ],
                padding="0.2em",
            )
        ),
        padding="1em",
        border="1px solid #ccc",
        border_radius="8px",
    )

    # Left column: Groups list with search
    group_column = rx.vstack(
        rx.heading("Groups", font_size="1.2em", margin_bottom="0.5em"),
        rx.input(
            placeholder="Search groups...",
            value=State.search_text,
            on_change=State.set_search_text,  # Reflex auto-generates set_search_text for the var
            margin_bottom="0.5em"
        ),
        rx.foreach(
            State.filtered_groups,
            lambda group: rx.checkbox(
                text=group,
                checked=State.selected_group == group,
                on_change=lambda checked: State.set_selected_group(group if checked else "")
            )
        ),
        padding="1em",
        border="1px solid #ccc",
        border_radius="8px",
        width="30%"
    )

    # Middle column: Stacks dropdown (dependent on group selection)
    stacks_dropdown = rx.cond(
        State.selected_group_str.map(lambda s: s != "None" and s != ""),
        # If a group is selected, show the dropdown for stacks
        rx.select(
            items=State.selected_group.map(lambda g: group_to_stacks.get(g, [])),
            placeholder="Select a stack",
            value=State.selected_stack,
            on_change=State.set_selected_stack
        ),
        # If no group selected, show a disabled dropdown or message
        rx.select(
            items=[], 
            placeholder="No group selected",
            is_disabled=True
        )
    )
    stack_column = rx.vstack(
        rx.heading("Stacks", font_size="1.2em", margin_bottom="0.5em"),
        stacks_dropdown,
        padding="1em",
        border="1px solid #ccc",
        border_radius="8px",
        width="30%"
    )

    # Right column: Details sidebar (toggle between summary and detailed info)
    # Header with toggle switch
    details_header = rx.hstack(
        rx.heading("Details", font_size="1.2em"),
        rx.switch(
            checked=State.details_toggle,
            on_change=State.toggle_details_view
        ),
        justify="space-between",
        align_items="center",
        margin_bottom="0.5em"
    )
    # Summary view (if details_toggle is False)
    summary_view = rx.vstack(
        rx.text("Selection Summary", font_weight="bold"),
        rx.text(lambda: f"Selected Customer: {State.cstn_name.get()}" if State.cstn_name else "Selected Customer: None"),
        rx.text(lambda: f"Selected CFSH: {State.selected_cfsh_str.get()}"),
        rx.text(lambda: f"Selected Engines: {State.selected_engines_str.get()}"),
        rx.text(lambda: f"Selected Group: {State.selected_group_str.get()}"),
        rx.text(lambda: f"Selected Stack: {State.selected_stack_str.get()}"),
        align_items="start",
        padding="0.5em"
    )
    # Detailed info view (if details_toggle is True) using accordions
    detailed_view_items = []
    # Customer accordion item
    detailed_view_items.append(
        rx.accordion_item(
            header=f"Customer: {State.cstn_name.get()}",
            content=rx.box(
                rx.text(f"CFSH instances: {', '.join(cstn_to_cfsh.get(State.cstn_name.get(), []))}"),
                padding="0.5em"
            )
        )
    )
    # CFSH accordion item (if any CFSH selected or any engine selected)
    cfsh_summary = State.selected_cfsh_str.get()
    if cfsh_summary != "None":
        # Prepare content listing each selected CFSH and its engines
        cfsh_details = []
        cfsh_list = cfsh_summary.split(", ")
        for cf in cfsh_list:
            if cf and cf != "None":
                eng_list = cfsh_to_engines.get(cf, [])
                cfsh_details.append(rx.text(f"{cf}: Engines -> {', '.join(eng_list) if eng_list else 'None'}"))
        detailed_view_items.append(
            rx.accordion_item(
                header=f"Selected CFSH: {cfsh_summary}",
                content=rx.box(*cfsh_details, padding="0.5em")
            )
        )
    # Engine accordion item (if any engine selected)
    eng_summary = State.selected_engines_str.get()
    if eng_summary != "None":
        # Content: list each engine and groups it belongs to
        engine_details = []
        for eng in sorted(State.selected_engines):
            groups = engine_to_groups.get(eng, [])
            engine_details.append(rx.text(f"{eng}: Groups -> {', '.join(groups) if groups else 'None'}"))
        detailed_view_items.append(
            rx.accordion_item(
                header=f"Selected Engine(s): {eng_summary}",
                content=rx.box(*engine_details, padding="0.5em")
            )
        )
    # Group accordion item (if a group is selected)
    if State.selected_group:
        grp = State.selected_group
        stacks = group_to_stacks.get(grp, [])
        detailed_view_items.append(
            rx.accordion_item(
                header=f"Selected Group: {grp}",
                content=rx.box(
                    rx.text(f"Stacks in group: {', '.join(stacks) if stacks else 'None'}"),
                    padding="0.5em"
                )
            )
        )
    # Stack accordion item (if a stack is selected)
    if State.selected_stack:
        stk = State.selected_stack
        detailed_view_items.append(
            rx.accordion_item(
                header=f"Selected Stack: {stk}",
                content=rx.box(
                    rx.text(f"Stack '{stk}' is selected (Group: {State.selected_group})"),
                    rx.text("<< Additional stack details can go here >>"),
                    padding="0.5em"
                )
            )
        )
    detailed_view = rx.accordion(
        *detailed_view_items,
        allow_multiple=True,
        collapsible=True,
        border="none"   # use no border for accordion to let section borders show cleanly
    )
    # Combine summary and detailed views with a toggle condition
    details_body = rx.cond(
        State.details_toggle,
        detailed_view,
        summary_view
    )
    # Close button at bottom of sidebar
    close_btn = rx.button("Close", on_click=State.close_sidebar, margin_top="1em")

    details_column = rx.vstack(
        details_header,
        details_body,
        close_btn,
        padding="1em",
        border="1px solid #ccc",
        border_radius="8px",
        width="40%",  # give the sidebar a bit larger width
        align_items="stretch"
    )

    # Main content area layout: three columns, conditional rendering of sidebar
    content_area = rx.hstack(
        group_column,
        stack_column,
        rx.cond(
            State.sidebar_visible,
            details_column,
            rx.box()  # empty box if sidebar hidden (could also collapse space)
        ),
        align_items="start",
        spacing="1em",
        padding="1em"
    )

    # Final page layout
    return rx.vstack(
        top_bar,
        cfsh_list_section,
        content_area,
        align_items="stretch",
        width="100%"
    )

# Create and compile the app
app = rx.App()
app.add_page(index, route="/")

