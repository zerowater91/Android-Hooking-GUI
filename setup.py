import sys,os
from cx_Freeze import setup, Executable

os.environ['TCL_LIBRARY'] = r'C:\Python36\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Python36\tcl\tk8.6'
# Note: I'm using cx_freeze on python 2.7,
#       change tkinter module names when using python3

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
        "packages":[r"tkinter",r"frida",r"pygubu",r"threading"],
	'include_files': [r'zerowater.ui',r'C:\Python36\DLLs\tcl86t.dll',r'C:\Python36\DLLs\tk86t.dll'],
	}
bdist_msi_options = {
    'add_to_path': False,
    'initial_target_dir': r'[ProgramFilesFolder]\%s' % ('zerowater'),
    }

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "zerowater hooking",
        version = "1.0",
        description = "Android Hooking Application",
        options = {"build_exe": build_exe_options,'bdist_msi': bdist_msi_options},
        executables = [Executable("zer0water.py", base=base)])
