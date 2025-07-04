# Tuxedo RGB FX

A robust `systemd` service that creates a smooth, aesthetically-pleasing "chameleon" RGB effect for the keyboards of Tuxedo, Clevo, and other compatible laptops. Written in Python for performance and stability.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

![Demo GIF](demo.gif)

## Features

-   **Systemd Service:** Installs as a true system service. It's easy to manage, enable on boot, and control using standard Linux commands.
-   **Highly Performant:** Written in Python, using minimal system resources and avoiding the complexities of process management.
-   **Smooth Gradient Transitions:** Colors fade seamlessly into one another, creating a fluid and continuous effect.
-   **Vibrant & Aesthetic Palette:** The script is designed to generate vivid and saturated colors (deep blues, vibrant reds, bright greens) while avoiding muddy or grayish tones.
-   **Auto-Detection:** Automatically finds the correct keyboard control file on your system, increasing compatibility across different models.
-   **Robust & Stable:** Designed to be stable and avoid conflicts with system processes.

## Known Limitation: Hardware Brightness Keys

The `tuxedo-keyboard` driver has two mutually exclusive modes: a "Brightness Mode" (controlled by `Fn` keys) and an "RGB Mode" (controlled by writing color values). When this script is active, it puts the driver into "RGB Mode," which **prevents the hardware `Fn` brightness keys from working**.

**The Workaround:** The recommended way to adjust keyboard brightness is to:
1.  **Stop the effect** using the `systemctl stop` command or your "Stop" shortcut.
2.  **Adjust the brightness** using your `Fn` keys.
3.  **Start the effect again** using the `systemctl start` command or your "Start" shortcut.

This is a fundamental limitation of the driver, and this script is designed to work harmoniously around it.

## Requirements

-   **A Linux distribution using `systemd`** (most modern distros like Arch, EndeavourOS, Ubuntu, Fedora, etc.).
-   **A compatible laptop:** This script is designed for laptops that use the `tuxedo-keyboard` kernel module. This typically includes most models from **Tuxedo, Clevo, Monster, Schenker, XMG,** etc.
-   **Kernel Driver:** The `tuxedo-keyboard` module (or a compatible one) must be installed and loaded for the script to find the control files.
-   **Python 3.6+** (pre-installed on most modern systems).

## Installation

The automated installer handles everything, including setting up the systemd service.

1.  Clone this repository:
    ```bash
    git clone https://github.com/Kanake83/tuxedo-rgb-fx.git
    cd tuxedo-rgb-fx
    ```

2.  Run the installation script with `sudo`:
    ```bash
    sudo ./install.sh
    ```

## Usage

Once installed, you manage the effect using `systemctl`, the standard tool for controlling services on Linux.

### Managing the Service

-   **Start the effect:** `sudo systemctl start tuxedo-rgb-fx.service`
-   **Stop the effect:** `sudo systemctl stop tuxedo-rgb-fx.service`
-   **Check the status:** `sudo systemctl status tuxedo-rgb-fx.service`
-   **Enable on Boot:** To make the effect start automatically every time you turn on your computer:
    ```bash
    sudo systemctl enable tuxedo-rgb-fx.service
    ```
-   **Disable on Boot:**
    ```bash
    sudo systemctl disable tuxedo-rgb-fx.service
    ```

### Creating Keyboard Shortcuts (KDE Plasma Example)

For KDE Plasma, you can create separate shortcuts to start and stop the effect. This is the most reliable method.

1.  **Allow Passwordless Control:**
    First, you need to allow your user to control this specific service without a password. Run `sudo visudo` and add the following line at the very end of the file, replacing `your_username` with your actual username:
    ```
    your_username   ALL=(ALL) NOPASSWD: /usr/bin/systemctl start tuxedo-rgb-fx.service, /usr/bin/systemctl stop tuxedo-rgb-fx.service
    ```

2.  **Set up the Shortcuts in KDE:**
    -   Go to `System Settings` > `Shortcuts` > `Custom Shortcuts`.
    -   **Create the "Start" shortcut:**
        -   Click `Edit` > `New` > `Global Shortcut` > `Command/URL`.
        -   Name it **"Start Keyboard FX"**.
        -   In the `Trigger` tab, set your desired shortcut (e.g., `Meta + L`).
        -   In the `Action` tab, enter the command: `sudo systemctl start tuxedo-rgb-fx.service`
    -   **Create the "Stop" shortcut:**
        -   Create another new global shortcut.
        -   Name it **"Stop Keyboard FX"**.
        -   In the `Trigger` tab, set a different shortcut (e.g., `Meta + Shift + L`).
        -   In the `Action` tab, enter the command: `sudo systemctl stop tuxedo-rgb-fx.service`
    -   Click `Apply`.

Now you have separate, reliable shortcuts to turn the effect on and off.

## How to Contribute

This project provides a solid foundation. If you have ideas for improvements, pull requests are welcome! Some potential areas for future work include:
-   **Adding more effects:** "Wave", "Breathe", or "Reactive Typing" could be implemented.
-   **Configuration File:** A user-friendly config file to change settings like speed and color palette without editing the script.
-   **GUI/Tray Applet:** A graphical interface for easier control.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
