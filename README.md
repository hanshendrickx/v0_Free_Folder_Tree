... existing code ...

### Windows (install.bat)
```batch
@echo off
echo Installing Free Professional Folder Tree Generator...
mkdir "%USERPROFILE%\tools\Free_Folder_Tree"
cd "%USERPROFILE%\tools\Free_Folder_Tree"
pip install Pillow svgwrite reportlab
mkdir Output
echo Installation complete!
pause
