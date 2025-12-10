    # Power Tools Suite for GNOME
    ![License](https://img.shields.io/badge/License-GPLv3-blue.svg) ![Platform](https://img.shields.io/badge/Platform-Linux%20%28GNOME%29-green.svg) ![Toolkit](https://img.shields.io/badge/Toolkit-GTK4%20%2F%20Libadwaita-orange.svg)
    **Stop memorizing commands. Start getting work done fast.**
    
    The **Power Tools Suite** is a collection of modern utilities designed to fix the biggest complaint about Linux: *"Why do I need the terminal to do basic things?"*
    
    This suite bridges the gap between the raw power of the Linux kernel and the elegance of the GNOME desktop. It transforms your right-click menu of your file manager into a command center, giving you capabilities that often require expensive third-party software on Windows or macOS — secure deletion, forensic analysis, and encrypted file transfer — completely free and open source.
    
    ---
    
    ## 🌟 The Philosophy
    
    Linux shouldn't be difficult. It should be powerful *and* accesible for use.
    
    1.  **Zero Terminal Required:** Every tool launches a modern, graphical window.
    2.  **Native Design:** Built with `Libadwaita`, these tools look and feel like they came pre-installed on your computer.
    3.  **Safety First:**  Safety locks and warnings are included to nudge and/or to prevent you from accidentally performing dangerous actions.
    
    ---
    
    ## 🚀 Feature Spotlight: Send Over Local Network
    
    **The ultimate privacy tool for the modern home.**
    
    Most file transfer tools require the internet, a cloud account, or trusting a third-party app. **Send Over Local Network** is different.
    
    * **⚡️ Standalone Application:** You can launch this tool directly from your app menu to pick files, or simply right-click a file to send it immediately.
    * **🔒 End-to-End Encrypted (E2EE):** Your files are encrypted with **AES-256** *before* they leave your computer. The decryption key is never sent over the network; it is embedded inside the QR code.
    * **📡 Optical Air-Gap:** To receive the file, the recipient scans a QR code from your screen. This creates a physical "optical key exchange" that cannot be intercepted by anyone snooping on your Wi-Fi.
    * **🌐 No Internet Required:** Works perfectly even if your internet is down. The data travels directly from Device A to Device B on the same network.
    
    ---
    
    ## 🛠️ The Full Suite
    
    This repository installs 9 distinct utilities to handle every aspect of your digital life:
    
    
     **File Centre**: A complete forensic dashboard. View technical metadata, check file hashes (MD5/SHA256), see who owns a file, and kill apps that are locking it.
    **Secure Delete**: Permanently destroys files by overwriting them 3 times. Includes a confirmation to prevent accidents. 
    **PDF Merger**:  Combine multiple PDF documents into one. 
    **Quick Print**:  Instantly sends files to your printer without opening them.
    **VirusTotal Scan**: Checks files against 70+ antivirus engines in the cloud. Uses a secure, encrypted vault for your API key.
    **Integrity Verifier**:  Did your download corrupt? This tool instantly compares a file's digital fingerprint against your clipboard.
    **Media Converter**:  Batch convert video and audio to modern formats (HEVC, AAC, FLAC) with smart metadata preservation.
    **Quick Resize**: Shrink images to standard sizes (SD, HD, 4K) in one click. Perfect for email attachments or web uploads.
    **Send Over Local Network**: Securely beam files to _any_ phone, tablet or laptop on your Wi-Fi via QR code.
    
    ---
    
    ## 📦 Installation
    
    The included installer installs selected tools and apps into your user folder (`~/.local/share`), meaning they **do not** clutter your system directories.
    
    However, to draw the windows and perform the magic, your system needs a few standard libraries.
    
    ### Step 1: Prepare Your System
    Copy and paste the command for your specific Linux distribution into a terminal. You only need to do this once.
    
    **🔵 Fedora Workstation**
    ```bashsudo dnf install python3-gobject python3-libadwaita gtk4 \    libgexiv2 python3-mutagen python3-secret \    ffmpeg poppler-utils psmisc attr qrencode ghostscript

**⚛️ Fedora Silverblue / Kinoite** (Atomic)

Bash
    rpm-ostree install python3-gobject python3-libadwaita gtk4 \
        libgexiv2 python3-mutagen python3-secret \
        ffmpeg poppler-utils psmisc attr qrencode ghostscript
    # Reboot required to apply changes

**🟠 Ubuntu / Debian / Linux Mint**

Bash
    sudo apt update && sudo apt install python3-gi python3-adwaita \
        gir1.2-gtk-4.0 gir1.2-adw-1 gir1.2-gexiv2-0.10 \
        python3-mutagen python3-secret \
        ffmpeg poppler-utils psmisc attr qrencode ghostscript

**🟢 Arch Linux / Manjaro**

Bash
    sudo pacman -S python-gobject gtk4 libadwaita \
        libgexiv2 python-mutagen python-secretstorage \
        ffmpeg poppler psmisc attr qrencode ghostscript

### Step 2: Install the Suite

Now, simply download and run the installer. It handles everything else:

Bash
    git clone [https://github.com/rscoder-s/Power-Tools-Suite-for-GNOME.git](https://github.com/rscoder-s/Power-Tools-Suite-for-GNOME.git)
    cd Power-Tools-Suite-for-GNOME
    chmod +x Install
    ./Install

_(The installer will automatically refresh Nautilus, the file manager on GNOME. You can start using the tools immediately!)_

****

## ⌨️ Usage

The power of this suite lies in its seamless integration. Once the installation is complete, these tools are available wherever you need them within your file system.

1. **Open GNOME Files (Nautilus).**
2. **Right-Click** on any file or selection of files to bring up the context menu.
3. Navigate to the **Scripts** submenu.
4. Select the desired tool (e.g., **File Centre** or **Send Over Local Network (QR)**).

* * *

🖼️ Gallery
-----------

The suite utilizes a modern design language to provide a cohesive, polished experience.

| **Utility**                 | **Interface Preview**                                                                                         |
| --------------------------- | ------------------------------------------------------------------------------------------------------------- |
| **File Centre**             | _The ultimate file dashboard, featuring live lock monitoring, forensic timestamps, and metadata editing._<br> |
| **Secure Delete**           | _Visual confirmation screen with safety warnings._<br>                                                        |
| **PDF Merger**              | _Drag-and-drop reordering interface._<br>                                                                     |
| **VirusTotal Scan**         | _Live API progress and detailed threat reporting._<br>                                                        |
| **Send Over Local Network** | _QR code generation for encrypted transfer._<br>                                                              |

* * *

---

## ⚠️ Stability Warning & Contribution Call

**Current Version:** `v0.1.0 (Alpha)`

Please note that these scripts are currently in an **experimental alpha state**. While they have been designed with safety in mind (e.g., adhering to "filestream safety" principles), they have not yet been extensively tested across different hardware configurations or Linux distributions.

* **Use with caution:** It is recommend to test these tools on non-critical files first.
* **Bugs are expected:** If you encounter silent failures or unexpected behavior, please report them via the Issues tab.
* **Contributors needed:** Need for testers and developers to help harden the code, improve error handling for edge cases, and ensure compatibility with immutable systems (Fedora Silverblue, SteamOS, etc.).

**PS: Pull Requests are highly encouraged!**

----------
