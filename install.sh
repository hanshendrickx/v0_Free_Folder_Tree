#!/bin/bash
# Free_Folder_Tree Installation Script
# AI Development Carousel: v0 Enhanced

echo "🌳 Installing Free Professional Folder Tree Generator..."

# Create tools directory
TOOLS_DIR="$HOME/tools/Free_Folder_Tree"
mkdir -p "$TOOLS_DIR"
cd "$TOOLS_DIR"

echo "📁 Created directory: $TOOLS_DIR"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install --user Pillow svgwrite reportlab

# Create output directory
mkdir -p Output

# Make script executable
chmod +x Free_Folder_Tree.py

# Create desktop shortcut (Linux)
if command -v desktop-file-install &> /dev/null; then
    cat > Free_Folder_Tree.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Free Folder Tree
Comment=Professional folder tree generator
Exec=python3 $TOOLS_DIR/Free_Folder_Tree.py
Icon=folder
Terminal=true
Categories=Development;Utility;
EOF
    
    desktop-file-install --dir="$HOME/.local/share/applications" Free_Folder_Tree.desktop
    echo "🖥️  Desktop shortcut created"
fi

# Add to PATH (optional)
echo "🛣️  To add to PATH, add this line to your ~/.bashrc or ~/.zshrc:"
echo "export PATH=\"\$PATH:$TOOLS_DIR\""

echo "✅ Installation complete!"
echo "📖 Usage: python3 $TOOLS_DIR/Free_Folder_Tree.py --help"
echo "📁 Output directory: $TOOLS_DIR/Output"
