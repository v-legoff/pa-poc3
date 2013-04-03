from cx_Freeze import setup, Executable

includefiles = ['servers.txt']
includes = ['cherrypy.wsgiserver', 'ws4py', 'win32timezone']
excludes = ['Tkinter']

setup(
    name = 'aboard',
    version = '0.1',
    description = 'PythonAboard',
    author = 'me, who else?',
    author_email = 'findout@domain.ext',
    options = {
        'build_exe': {
            'excludes': excludes,
            'packages': includes,
            'include_files': includefiles
        }
    },
    executables = [
        Executable('aboard.py'),
        Executable('winservice.py'),
    ]
)