import cx_Freeze

# base = "Win32GUI" allows your application to open without a console window
executables = [cx_Freeze.Executable('main.py', base = "Win32GUI")]

cx_Freeze.setup(
    name = "My Example Exe App",
    options = {"build_exe" : 
        {"packages" : ["pygame"], "include_files" : ['assets/', "start_screen.py","seagull.py", "poop.py", "utils.py","enemy.py","background.py","constants.py"]}},
    executables = executables
)