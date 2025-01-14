"""The DevEnv Settings Screen for the TUI."""
# dem/cli/tui/window/dev_env_settings_screen.py

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Button, Header, Label, SelectionList
from textual.binding import Binding
from textual import events
from textual.screen import Screen
from rich.table import Table

from dem.cli.tui.printable_tool_image import PrintableToolImage

class DevEnvSettingsScreen(Screen):
    TITLE = "Development Environment Settings"

    def __init__(self, printable_tool_images: list[PrintableToolImage], 
                 already_selected_tool_images: list[str] = []) -> None:
        super().__init__()
        self.printable_tool_images = printable_tool_images
        self.already_selected_tool_images = already_selected_tool_images
        self.dev_env_status_height = len(printable_tool_images)
        self.dev_env_status_width = max(len(tool_image.name) for tool_image in printable_tool_images)
        dev_env_selection = [(tool_image.name, tool_image.name) for tool_image in printable_tool_images]
        self.tool_image_selector_widget = SelectionList(*dev_env_selection, 
                                                        id="tool_image_selector_widget", 
                                                        classes="tool_image_selector")
        self.dev_env_status_widget = Label("", id="dev_env_status_widget", classes="dev_env_status")
        self.cancel_button = Button("Cancel", id=self.app.cancel_button_id, classes="cancel_button")
        self.save_button = Button("Save", id=self.app.save_button_id, classes="save_button")

    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="dev_env_settings_screen", classes="dev_env_settings_screen"):
            yield self.tool_image_selector_widget
            yield self.dev_env_status_widget
            with Container(id="cancel_container", classes="cancel_container"):
                yield self.cancel_button
            with Container(id="save_container", classes="save_container"):
                yield self.save_button

    def on_mount(self) -> None:
        self.set_focus(self.tool_image_selector_widget)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.app.button_pressed = event.button.id
        self.app.exit()

    @on(events.Mount)
    @on(SelectionList.SelectedChanged)
    def update_dev_env_status(self) -> None:
        selected_tool_images_table = Table()
        selected_tool_images_table.add_column("Selected Tool Images")
        for tool_image in self.tool_image_selector_widget.selected:
            selected_tool_images_table.add_row(tool_image)
        self.dev_env_status_widget.update(selected_tool_images_table)
        
        self.app.selected_tool_images = self.tool_image_selector_widget.selected

class DevEnvSettingsWindow(App):
    CSS_PATH = "dev_env_settings_window.tcss"
    save_button_id = "save_button"
    cancel_button_id = "cancel_button"

    def __init__(self, printable_tool_images: list[PrintableToolImage], 
                 already_selected_tool_images: list[str] = []) -> None:
        super().__init__()
        self.printable_tool_images = printable_tool_images
        self.already_selected_tool_images = already_selected_tool_images
        self.button_pressed = None
        self.selected_tool_images = []

    def on_mount(self) -> None:
        self.push_screen(DevEnvSettingsScreen(self.printable_tool_images, 
                                              self.already_selected_tool_images))

def main(printable_tool_images: list[PrintableToolImage], 
         already_selected_tool_images: list[str] = []) -> None:
    app = DevEnvSettingsWindow(printable_tool_images, already_selected_tool_images)
    app.wait_for_user()