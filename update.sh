#!/bin/bash

REPO_URL="https://github.com/PietroMarigo/NotSmartTV.git"
INSTALL_DIR="/home/$(whoami)/NotSmartTV"
USERNAME=$(whoami)

echo "=========================================="
echo "   NotSmartTV Installer"
echo "   User: $USERNAME"
echo "   Install Location: $INSTALL_DIR"
echo "=========================================="

echo "Updating system"
sudo apt update && sudo apt upgrade -y

if [ -d "$INSTALL_DIR" ]; then
  echo "Updating existing repository"
  cd "$INSTALL_DIR"
  git pull
else
  echo "Cloning repository from GitHub"
  git clone "$REPO_URL" "$INSTALL_DIR"
  sudo usermod -aG input $USERNAME
  echo 'KERNEL=="uinput", MODE="0660", GROUP="input"' | sudo tee /etc/udev/rules.d/99-uinput.rules
fi

echo "Setting up SERVER environment"
cd "$INSTALL_DIR/server"
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi
./.venv/bin/pip install -r dependencies.txt

echo "Setting up PLATFORM environment"
cd "$INSTALL_DIR/platform"
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi
if [ -f "dependencies.txt" ]; then
  ./.venv/bin/pip install -r dependencies.txt
fi

echo "Fixing Control Permissions"
sudo udevadm control --reload-rules
sudo udevadm trigger

echo "Generating Systemd Service Files"

cat <<EOF | sudo tee /etc/systemd/system/tv-remote.service
[Unit]
Description=NotSmartTV Remote Control Service
After=network.target

[Service]
Type=simple
User=$USERNAME
WorkingDirectory=$INSTALL_DIR/server
# CRITICAL: Points to the SERVER .venv
ExecStart=$INSTALL_DIR/server/.venv/bin/python main.py
Restart=always
RestartSec=5
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOF

cat <<EOF | sudo tee /etc/systemd/system/tv-platform.service
[Unit]
Description=NotSmartTV Platform Dashboard
After=graphical.target

[Service]
Type=simple
User=$USERNAME
WorkingDirectory=$INSTALL_DIR/platform
ExecStart=$INSTALL_DIR/platform/.venv/bin/python main.py
Restart=always
RestartSec=10
Environment=PYTHONUNBUFFERED=1

Environment=DISPLAY=:0
Environment=XDG_RUNTIME_DIR=/run/user/$(id -u)
Environment=WAYLAND_DISPLAY=wayland-0

[Install]
WantedBy=graphical.target
EOF

echo "Enabling Services"
sudo systemctl daemon-reload
sudo systemctl enable tv-remote.service
sudo systemctl enable tv-platform.service

echo "=========================================="
echo "Installation Complete!"
echo "Services enabled. Please REBOOT your Pi now."
echo "=========================================="
