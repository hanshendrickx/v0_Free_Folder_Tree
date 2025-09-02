@echo off
echo ================================================================================
echo FREE PROFESSIONAL FOLDER TREE GENERATOR - INSTALLATION
echo AI Development Carousel: v0 Enhanced
echo ================================================================================
echo.

REM Create Free_Folder_Tree directory structure
set INSTALL_DIR=%USERPROFILE%\tools\Free_Folder_Tree
if not exist "%INSTALL_DIR%" (
    mkdir "%INSTALL_DIR%"
    echo Created Free_Folder_Tree directory
)

if not exist "%INSTALL_DIR%\Output" (
    mkdir "%INSTALL_DIR%\Output"
    echo Created Output directory
)

REM Copy main script
copy Free_Folder_Tree.py "%INSTALL_DIR%\"
if errorlevel 1 (
    echo Error: Could not copy Free_Folder_Tree.py
    pause
    exit /b 1
)

echo.
echo Installing Python dependencies...
pip install Pillow svgwrite reportlab
if errorlevel 1 (
    echo Warning: Some dependencies may not have installed correctly
    echo You can install them manually with: pip install Pillow svgwrite reportlab
)

echo.
echo ================================================================================
echo INSTALLATION COMPLETE!
echo ================================================================================
echo.
echo Installation Directory: %INSTALL_DIR%
echo Output Directory: %INSTALL_DIR%\Output
echo.
echo USAGE EXAMPLES:
echo   Simple:     python "%INSTALL_DIR%\Free_Folder_Tree.py" C:\Users
echo   Beautiful:  python "%INSTALL_DIR%\Free_Folder_Tree.py" . --style artisanal --icons
echo   Perfect:    python "%INSTALL_DIR%\Free_Folder_Tree.py" . --style artisanal --icons --formats txt png svg --depth 3
echo.
echo For help:     python "%INSTALL_DIR%\Free_Folder_Tree.py" --help
echo.
echo ================================================================================
echo (c) 2024-2025 Hans Hendrickx MD PhD and Karl Hendrickx MSc
echo AI Development Carousel: v0 Enhanced
echo ================================================================================
pause
