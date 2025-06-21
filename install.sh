#!/bin/bash

# Tuxedo RGB FX - Final Universal Installer with systemd support

# --- CONFIGURATION ---
SCRIPT_NAME="tuxedo-rgb-fx"
INSTALL_PATH="/usr/local/bin"
SYSTEMD_PATH="/etc/systemd/system"

SOURCE_PY_FILE="./${SCRIPT_NAME}.py"
SOURCE_SERVICE_FILE="./${SCRIPT_NAME}.service"
# ---------------------

print_info() { echo -e "\033[1;34m[INFO]\033[0m $1"; }
print_success() { echo -e "\033[1;32m[SUCCESS]\033[0m $1"; }
print_error() { echo -e "\033[1;31m[ERROR]\033[0m $1" >&2; }

# --- START OF INSTALLATION ---
print_info "Starting Tuxedo RGB FX installation..."

if [ "$EUID" -ne 0 ]; then
  print_error "This installer must be run as root. Please use 'sudo ./install.sh'."
  exit 1
fi

if [ ! -f "$SOURCE_PY_FILE" ] || [ ! -f "$SOURCE_SERVICE_FILE" ]; then
    print_error "Source files not found. Run this from the project directory."
    exit 1
fi

print_info "Checking for Python 3..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install it and try again."
    exit 1
fi
print_info "Python 3 is installed. ✓"

print_info "Installing Python script to $INSTALL_PATH..."
cp "$SOURCE_PY_FILE" "$INSTALL_PATH/$SCRIPT_NAME.py"
chmod +x "$INSTALL_PATH/$SCRIPT_NAME.py"

print_info "Installing systemd service file..."
cp "$SOURCE_SERVICE_FILE" "$SYSTEMD_PATH/$SCRIPT_NAME.service"
chmod 644 "$SYSTEMD_PATH/$SCRIPT_NAME.service"

print_info "Reloading systemd daemon..."
systemctl daemon-reload

echo ""
print_success "Installation complete!"
echo ""
print_info "To enable the effect on boot, run:"
echo "  sudo systemctl enable $SCRIPT_NAME.service"
echo ""
print_info "To start the effect now, run:"
echo "  sudo systemctl start $SCRIPT_NAME.service"
echo ""
print_info "For instructions on creating keyboard shortcuts, please see the README.md file."
echo ""
