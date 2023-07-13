import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name='MITAS CIVATA STOK KONTROL',
    version='4.0',
    description='Stock Control App',
    executables=[Executable('Stock Control App.py', base=base, icon='Capture.ico')],
    options={
        'build_exe': {
            'include_files': [
                ('Capture.ico'),
                ('config.json'),
                ('parameters.json')
            ]
        }
    }
)
