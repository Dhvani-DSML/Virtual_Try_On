@echo off
echo Setting up Virtual Try-On Application...

echo Removing existing virtual environment...
if exist venv rmdir /s /q venv

echo Creating virtual environment...
py -3.10 -m venv venv

echo Activating virtual environment and installing dependencies...
call venv\Scripts\activate.bat

python -m pip install --upgrade pip

:: Install packages in order with specific versions using wheels
pip install numpy==1.23.5
pip install mediapipe==0.10.5
pip install opencv-python==4.7.0.72
pip install flask==2.3.3
pip install pillow==9.5.0

echo Setup complete! You can now run the application using run.bat
pause 