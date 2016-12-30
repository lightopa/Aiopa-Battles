#!/usr/bin/env python3
import sys
from cx_Freeze import setup, Executable
from variables import version


# Dependencies are automatically detected, but it might need fine tuning.
includefiles = ["assets/", "lib/extraDLLs/libogg.dll", "lib/extraDLLs/libvorbis.dll", "lib/extraDlls/libvorbisfile.dll"]
packages = []
build_exe_options = {'include_files': includefiles, 'packages': packages}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

target = Executable(
           # what to build
           script = "run.py",
           initScript = None,
           base = base,
           targetName = "Aiopa Battles.exe",
           compress = True,
           copyDependentFiles = True,
           appendScriptToExe = False,
           appendScriptToLibrary = False,
           icon = "assets/images/icons/icon4.ico"
  )



setup(  name = "Aiopa Battles",
        version = version.split("-")[0],
        description = "Aiopa Battles",
        author = "Lightopa Games",
        options = {"build_exe": build_exe_options},
        executables = [target])
