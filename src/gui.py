#import and configure versions
import gi
import os
import sys
from modules.vault_manager import *
from hashlib import md5

gi.require_version('Gtk' ,'3.0')
from gi.repository import Gtk, GLib


class FileChooserWindow(Gtk.Window):
    def __init__(self, fileMan):
        super().__init__(title="FileChooser Example")
        self.fileMan = fileMan
        box = Gtk.Box(spacing=6)
        self.add(box)

        button1 = Gtk.Button(label="Choose File")
        button1.connect("clicked", self.on_file_clicked)
        box.add(button1)

        button2 = Gtk.Button(label="Choose Folder")
        button2.connect("clicked", self.on_folder_clicked)
        box.add(button2)

    def on_file_clicked(self, widget):
        dialog = Gtk.FileChooserDialog(
            title="Please choose a file", parent=self, action=Gtk.FileChooserAction.OPEN
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK,
        )

        self.add_filters(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filepath = dialog.get_uris()
            print("Open clicked")
            print("File selected: " + filepath)
            filename = os.path.basename(filepath)
            uploadPath = str(uploadDir + filename)
            shutil.copy(filepath, uploadPath)
            self.fileMan.add(filename)
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

    def on_folder_clicked(self, widget):
        dialog = Gtk.FileChooserDialog(
            title="Please choose a folder",
            parent=self,
            action=Gtk.FileChooserAction.SELECT_FOLDER,
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Select", Gtk.ResponseType.OK
        )
        dialog.set_default_size(800, 400)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Select clicked")
            print("Folder selected: " + dialog.get_filename())
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

class Auth(Gtk.Window):
    def __init__(self):
        super().__init__(title="Login")
        self.set_size_request(200, 100)

        self.timeout_id = None
        # Main box
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        # Label box
        self.label = Gtk.Label(label = "Enter password: ")
        vbox.pack_start(self.label, True, True, 0)
        # Entry box
        self.entry = Gtk.Entry()
        vbox.pack_start(self.entry, True, True, 0)
        # Text box
        hbox = Gtk.Box(spacing=6)
        vbox.pack_start(hbox, True, True, 0)

        self.entry.set_editable(True)
        self.entry.set_visibility(False)

        # Submit box
        button = Gtk.Button.new_with_label("Submit")
        button.connect("clicked", self.submit)
        hbox.pack_start(button, True, True, 0)
    # Utility
    def getMD5(self, plaintext):
        m = md5()
        m.update(plaintext.encode('utf-8'))
        hash = str(m.hexdigest())
        return hash
    def submit(self, button):
        if os.path.isfile('auth'):
            savedpassword = open('auth', 'r').read()
            password = self.entry.get_text()
            pwdhash = self.getMD5(password)
            if pwdhash == savedpassword:
                self.password = password
            else:
                sys.exit('Wrong password')
        else:
            password = str(input("Enter new password: "))
            pwdhash = getMD5(password)
            open('auth', 'w').write(pwdhash)
            self.password = password
        self.destroy()
        print('destroyed')

class Filelist(Gtk.Window):
    """docstring for FileManager."""

    def __init__(self, fileMan):
        super().__init__(title="File Manager")

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        for file in fileMan.ls('/'):
            label = Gtk.Label(label = file)
            vbox.pack_start(label, True, True, 0)

class ActionManager(Gtk.Window):
    """docstring for ActionManager."""

    def __init__(self, fileMan):
        super().__init__(title="Action Manager")
        self.fileMan  = fileMan
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        button = Gtk.Button.new_with_label("File list")
        button.connect("clicked", self.filelist)
        vbox.pack_start(button, True, True, 0)

        button = Gtk.Button.new_with_label("Add file")
        button.connect("clicked", self.addfile)
        vbox.pack_start(button, True, True, 0)

        button = Gtk.Button.new_with_label("Quit")
        button.connect("clicked", sys.exit)
        vbox.pack_start(button, True, True, 0)

    def filelist(self, button):
        fm = Filelist(self.fileMan)
        fm.show_all()
        Gtk.main()
    def addfile(self, button):
        fcw = FileChooserWindow(self.fileMan)
        fcw.connect("destroy", sys.exit)
        fcw.show_all()
        Gtk.main()



class Main():
    def __init__(self):
        super(Main, self).__init__()
    def auth(self):
        auth_window = Auth()
        auth_window.show_all()
        auth_window.connect("destroy", Gtk.main_quit)
        Gtk.main()
        print('Auth done')
        self.password = auth_window.password
        self.fileMan = fileManager(self.password)
    def actionManager(self):
        print('action')
        am = ActionManager(self.fileMan)
        am.show_all()
        am.connect("destroy", sys.exit)
        Gtk.main()

gui = Main()
gui.auth()
gui.actionManager()