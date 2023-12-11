import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

import threading
from gi.repository import Gtk, Adw, Gio, GLib

class ArchiveUI(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(show_menubar=True,
                          application=app,)
        
        self.set_default_size(600, 550)
        self.set_size_request(600, 550)
        
        self.set_title("Archive")

        self.file = ""

        header = Adw.HeaderBar.new()
        self.set_titlebar(header)

        menu_Model = Gio.Menu.new()
        menu_Model.append('Open', 'app.open')

        menu = Gtk.MenuButton.new()
        menu.set_icon_name('open-menu-symbolic')
        menu.set_menu_model(menu_Model)

        header.pack_start(menu)

        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        self.present()

class ArchiveApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id='com.github.XtremeTHN.archive', 
                         flags=Gio.ApplicationFlags.FLAGS_NONE)
        
        self.create_action('quit', self.exit_app, ['<primary>q'])
        self.create_action('open', self.open_file)

    def do_activate(self):
        self.win = self.props.active_window
        if not self.win:
            self.win = ArchiveUI(self)
    
    def do_startup(self) -> None:
        Gtk.Application.do_startup(self)
    
    def do_shutdown(self) -> None:
        Gtk.Application.do_shutdown(self)
    
    def open_file(self, action, param) -> None:
        print("Asd")
        dialog = Gtk.FileChooserNative(accept_label="Open", 
                                       cancel_label="Cancel", 
                                       title="Choose a file to view",
                                       transient_for=self.get_active_window(),
                                       visible=True,
                                       create_folders=False,
                                       select_multiple=False)
        dialog.show()
        dialog.connect("response", self._open_file_cb, dialog)
    
    def _open_file_cb(self, _, response, dialog):
        if response == Gtk.ResponseType.OK:
            self.win.file = dialog.get_filenames()
            print("Showing")
            print(self.win.file, type(self.win.file), dialog.get_filenames())
            dialog.destroy()
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
    
    def exit_app(self, action, param):
        self.quit()
    
    def create_action(self, name, callback, shortcuts=None):
        action = Gio.SimpleAction.new(name, None)
        action.connect('activate', callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f'app.{name}', shortcuts)