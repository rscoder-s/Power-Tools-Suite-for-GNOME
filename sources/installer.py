#!/usr/bin/env python3
import sys
import os
import shutil
import subprocess
import threading
import datetime
# --- PRE-FLIGHT DEPENDENCY CHECK ---
# If Libadwaita is missing, we must warn the user before crashing.
try:
    import gi
    gi.require_version('Gtk', '4.0')
    gi.require_version('Adw', '1')
    from gi.repository import Gtk, Adw, GLib, Gio
except ValueError:
    # If we are here, the system is missing the GUI libraries.
    # We try to use Zenity to show an error since GTK failed.
    subprocess.run([
        "zenity", "--error", 
        "--text=<b>Critical Error:</b>\n\nMissing 'python3-libadwaita'.\nThe installer cannot run without it.\n\nPlease run:\n<tt>sudo dnf install python3-libadwaita</tt>", 
        "--width=400"
    ])
    sys.exit(1)
except ImportError:
    # Fallback for non-GTK systems
    print("Error: Python GObject/GTK not found.")
    sys.exit(1)

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GLib, Gio

# --- CONFIGURATION ---
BEAM_FILENAME = "Send over Local Network (QR)"
APP_ID = "com.secure.beam.installer"

class InstallerApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id=APP_ID)
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.source_dir = os.path.join(self.script_dir, "scripts")
        
        # Paths
        home = os.path.expanduser("~")
        self.nautilus_dir = os.path.join(home, ".local/share/nautilus/scripts")
        self.app_dir = os.path.join(home, ".local/share/applications")
        self.bin_dir = os.path.join(home, ".local/bin")
        self.backup_dir = os.path.join(self.nautilus_dir, f"Backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}")

    def do_activate(self):
        win = Adw.ApplicationWindow(application=self)
        win.set_title("Tool Suite Installer")
        win.set_default_size(500, 650)
        
        # Main Layout (Toast Overlay -> Toolbar View)
        self.toast_overlay = Adw.ToastOverlay()
        win.set_content(self.toast_overlay)
        
        toolbar_view = Adw.ToolbarView()
        self.toast_overlay.set_child(toolbar_view)
        
        header = Adw.HeaderBar()
        toolbar_view.add_top_bar(header)
        
        # Scrollable Content
        page = Adw.PreferencesPage()
        toolbar_view.set_content(page)
        
        # --- HERO SECTION ---
        group_hero = Adw.PreferencesGroup()
        page.add(group_hero)
        
        hero_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        hero_box.set_margin_top(20)
        hero_box.set_margin_bottom(10)
        
        icon = Gtk.Image.new_from_icon_name("system-software-install")
        icon.set_pixel_size(96)
        icon.add_css_class("accent") 
        hero_box.append(icon)
        
        title = Gtk.Label(label="Install Tool Suite", css_classes=["title-1"])
        hero_box.append(title)
        
        desc = Gtk.Label(label="Select the components you wish to install.", css_classes=["body"])
        hero_box.append(desc)
        
        # Wrap hero in a row just for layout
        row_hero = Adw.ActionRow()
        row_hero.set_child(hero_box)
        group_hero.add(row_hero)

        # --- SCRIPTS LIST ---
        self.group_scripts = Adw.PreferencesGroup(title="Nautilus Context Menu Scripts")
        page.add(self.group_scripts)
        
        # Scan for scripts
        self.script_switches = {}
        if os.path.exists(self.source_dir):
            for f in sorted(os.listdir(self.source_dir)):
                full_path = os.path.join(self.source_dir, f)
                # Check for Shebang to ensure it's a script
                if os.path.isfile(full_path):
                    with open(full_path, 'rb') as script_file:
                        try:
                            if script_file.read(2) == b'#!':
                                self.add_script_row(f)
                        except: pass
        else:
            self.show_toast(f"Error: 'scripts' folder not found in {self.script_dir}")

        # --- APP SECTION ---
        group_app = Adw.PreferencesGroup(title="System Applications")
        page.add(group_app)
        
        # Secure Beam App Toggle
        self.beam_switch = Gtk.Switch()
        self.beam_switch.set_active(False)
        self.beam_switch.set_valign(Gtk.Align.CENTER)
        
        row_beam = Adw.ActionRow(title="Secure Beam App")
        row_beam.set_subtitle("Add 'Send over Local Network' to App Grid and Dock")
        row_beam.add_suffix(self.beam_switch)
        
        # FIX 1: set_icon_name is deprecated. Use add_prefix with GtkImage.
        beam_icon = Gtk.Image.new_from_icon_name("network-wireless-hotspot")
        row_beam.add_prefix(beam_icon)
        
        group_app.add(row_beam)
        
        # If secure beam script exists in source, default to checked
        if BEAM_FILENAME in self.script_switches:
            self.beam_switch.set_active(True)

        # --- INSTALL BUTTON ---
        self.btn_install = Gtk.Button(label="Install Selected")
        self.btn_install.add_css_class("suggested-action")
        self.btn_install.add_css_class("pill")
        self.btn_install.set_margin_top(20)
        self.btn_install.set_margin_bottom(20)
        self.btn_install.set_halign(Gtk.Align.CENTER)
        self.btn_install.connect("clicked", self.on_install_clicked)
        
        # Spinner (Hidden by default)
        self.spinner = Gtk.Spinner()
        self.spinner.set_margin_top(20)
        
        # Bottom Box
        bottom_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        bottom_box.append(self.btn_install)
        bottom_box.append(self.spinner)
        
        group_btn = Adw.PreferencesGroup()
        group_btn.add(bottom_box)
        page.add(group_btn)

        win.present()

    def add_script_row(self, filename):
        row = Adw.ActionRow(title=filename)
        
        # Check if update
        installed_path = os.path.join(self.nautilus_dir, filename)
        if os.path.exists(installed_path):
            row.set_subtitle("Update (Already installed)")
        
        switch = Gtk.Switch()
        switch.set_active(True) # Default on
        switch.set_valign(Gtk.Align.CENTER)
        
        row.add_suffix(switch)
        self.group_scripts.add(row)
        self.script_switches[filename] = switch

    def show_toast(self, message):
        toast = Adw.Toast.new(message)
        self.toast_overlay.add_toast(toast)

    def on_install_clicked(self, btn):
        # 1. Disable UI
        self.btn_install.set_sensitive(False)
        for s in self.script_switches.values(): s.set_sensitive(False)
        self.beam_switch.set_sensitive(False)
        
        # 2. Start Spinner
        self.spinner.start()
        
        # 3. Gather Tasks
        to_install_scripts = [name for name, sw in self.script_switches.items() if sw.get_active()]
        install_beam_app = self.beam_switch.get_active()
        
        # 4. Run in Thread
        thread = threading.Thread(target=self.run_installation, args=(to_install_scripts, install_beam_app))
        thread.start()

    def run_installation(self, scripts, beam_app):
        try:
            # Create Dirs
            os.makedirs(self.nautilus_dir, exist_ok=True)
            os.makedirs(self.app_dir, exist_ok=True)
            os.makedirs(self.bin_dir, exist_ok=True)
            
            # Install Scripts
            for script_name in scripts:
                src = os.path.join(self.source_dir, script_name)
                dest = os.path.join(self.nautilus_dir, script_name)
                
                # Backup
                if os.path.exists(dest):
                    os.makedirs(self.backup_dir, exist_ok=True)
                    shutil.move(dest, self.backup_dir)
                
                # Copy
                shutil.copy2(src, dest)
                os.chmod(dest, 0o755)

            # Install Beam App
            if beam_app and BEAM_FILENAME in scripts:
                src = os.path.join(self.source_dir, BEAM_FILENAME)
                dest_bin = os.path.join(self.bin_dir, "secure-beam")
                
                # Copy Binary
                shutil.copy2(src, dest_bin)
                os.chmod(dest_bin, 0o755)
                
                # Create .desktop
                desktop_content = f"""[Desktop Entry]
Type=Application
Name=Send over Local Network
Comment=Secure, Encrypted Local File Transfer
Exec="{dest_bin}" %F
Icon=network-wireless-hotspot
Terminal=false
Categories=Network;Utility;FileTransfer;
StartupNotify=true
MimeType=application/octet-stream;
"""
                desktop_path = os.path.join(self.app_dir, "secure-beam.desktop")
                with open(desktop_path, "w") as f:
                    f.write(desktop_content)
                os.chmod(desktop_path, 0o755)

            # Post-Install
            subprocess.run(["update-desktop-database", self.app_dir], stderr=subprocess.DEVNULL)
            subprocess.run(["nautilus", "-q"], stderr=subprocess.DEVNULL)
            
            GLib.idle_add(self.install_success, len(scripts))

        except Exception as e:
            GLib.idle_add(self.install_error, str(e))

    def install_success(self, count):
        self.spinner.stop()
        self.btn_install.set_sensitive(True)
        
        # FIX 2: Modern Adw.MessageDialog Usage
        dialog = Adw.MessageDialog(
            heading="Installation Complete",
            body=f"Successfully installed {count} scripts.\nNautilus has been restarted.",
        )
        dialog.add_response("ok", "OK")
        dialog.set_response_appearance("ok", Adw.ResponseAppearance.SUGGESTED)
        
        # FIX 3: Attach to window properly to avoid "TypeError"
        dialog.set_transient_for(self.get_active_window())
        dialog.present()

    def install_error(self, message):
        self.spinner.stop()
        self.btn_install.set_sensitive(True)
        
        dialog = Adw.MessageDialog(
            heading="Installation Failed",
            body=message,
        )
        dialog.add_response("close", "Close")
        dialog.set_response_appearance("close", Adw.ResponseAppearance.DESTRUCTIVE)
        
        # FIX 3: Attach to window properly
        dialog.set_transient_for(self.get_active_window())
        dialog.present()

if __name__ == "__main__":
    app = InstallerApp()
    app.run(sys.argv)
