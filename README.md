# wsdist
GUI interface for wsdist.py, currently in "beta" form.

The code for finding and comparing gearsets works well, but the UI scaling is not great yet.
You will likely need to resize the window or increase font size (see Edit menubar at the top) to make things useable.




You should be able to run the code with just the following files:

    gui_wsdist.exe
    item_list.txt
    icons32/*
    icons64/*

The gui_wsdist.exe was created with the commands within a Python3.8.8 virtual environment (see https://virtualenv.pypa.io/en/stable/user_guide.html):

    pip install numpy
    pip install matplotlib
    pip install numba
    pip install PySimpleGUI
    pip install pillow
    pip install pyinstaller

    pyinstaller --clean --onefile .\gui_wsdist.py

(see also: https://stackoverflow.com/a/70419705 for dealing with Windows10 PowerShell errors when trying to use virtual environments)