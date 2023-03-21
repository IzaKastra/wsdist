# wsdist
GUI interface for wsdist.py.

The code for finding and comparing gearsets works well, but the UI scaling is not great yet.
You will likely need to resize the window or increase font size (see Edit menubar at the top) to make things useable.


Run the code using

    python gui_wsdist.py

or download the executable and simply double-click it.

You should be able to run the executable with just the following files:

    gui_wsdist.exe
    item_list.txt
    icons32/*
    icons64/*

The gui_wsdist.exe was created with the following commands within a Python3.8.8 virtual environment using Windows10 PowerShell (see https://virtualenv.pypa.io/en/stable/user_guide.html):

    virtualenv venv
    .\venv\Scripts\activate.ps1

    pip install numpy
    pip install matplotlib
    pip install numba
    pip install PySimpleGUI
    pip install pillow
    pip install pyinstaller

    pyinstaller --clean --onefile .\gui_wsdist.py

(see also: https://stackoverflow.com/a/70419705 for dealing with Windows10 PowerShell ExecutionPolicy errors when trying to use virtual environments).