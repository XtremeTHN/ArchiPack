import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

import threading
from gi.repository import Gtk, Adw, Gio, GLib, GObject

class ArchiveUI(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(show_menubar=True,
                          application=app,)
        
        self.set_default_size(600, 550)
        self.set_size_request(600, 550)
        
        self.set_title("Archive")

        header = Adw.HeaderBar.new()
        self.set_titlebar(header)

        menu_Model = Gio.Menu.new()
        menu_Model.append('Open', 'app.open')

        menu = Gtk.MenuButton.new()
        menu.set_icon_name('open-menu-symbolic')
        menu.set_menu_model(menu_Model)

        header.pack_start(menu)

        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        self.add_placeholder()

        self.set_child(self.main_box)
        self.present()

    def open_file(self, *args) -> None:
        dialog = Gtk.FileDialog.new()
        dialog.set_accept_label("Open")
        dialog.open(self, None, self.add_files)

    def add_files(self, src_obj: Gtk.FileDialog, res: Gio.AsyncResult):
        if (n:=src_obj.open_finish(res)) is not None:
            ...

    def add_placeholder(self):
        placeholder = Gtk.CenterBox(orientation=Gtk.Orientation.VERTICAL, vexpand=True)
        placeholder_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)

        placeholder_title = Gtk.Label.new("<span font_weight='ultrabold' font_size='x-large'>ArchiPack</span>")
        placeholder_title.set_use_markup(True)

        placeholder_subtitle = Gtk.Label.new("<span font_size='smaller'>Select a file to view it's contents!</span>")
        placeholder_subtitle.set_use_markup(True)

        placeholder_button = Gtk.Button()
        placeholder_button_child = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        placeholder_button_child_icon = Gtk.Image.new_from_icon_name("edit-find-symbolic")
        placeholder_button_child_label = Gtk.Label.new("Choose file")

        placeholder_button_child.append(placeholder_button_child_icon)
        placeholder_button_child.append(placeholder_button_child_label)

        placeholder_button.set_child(placeholder_button_child)
        placeholder_button.connect("clicked", self.open_file)

        placeholder_box.append(placeholder_title)
        placeholder_box.append(placeholder_subtitle)
        placeholder_box.append(placeholder_button)

        placeholder.set_center_widget(placeholder_box)

        self.main_box.append(placeholder)

class ArchiveApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id='com.github.XtremeTHN.archive', 
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

    def do_activate(self):
        self.win = self.props.active_window
        if not self.win:
            self.win = ArchiveUI(self)
        
        self.create_action('quit', self.exit_app, ['<primary>q'])
        self.create_action('open', self.win.open_file)
    
    def do_startup(self) -> None:
        Gtk.Application.do_startup(self)
    
    def do_shutdown(self) -> None:
        Gtk.Application.do_shutdown(self)

    
    def exit_app(self, action, param):
        self.quit()
    
    def create_action(self, name, callback, shortcuts=None):
        action = Gio.SimpleAction.new(name, None)
        action.connect('activate', callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f'app.{name}', shortcuts)