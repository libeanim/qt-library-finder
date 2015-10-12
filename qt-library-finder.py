"""
================================
Qt library finder
================================

Find all Qt dependent libraries of your Qt executable on Linux.

ATTENTION: This is currently experimental especially the QML support.
"""

import fnmatch
import re
import subprocess
import shutil
import os

__version__ = '0.1'

### Enter your Qt Library directory (current path is just an example)
QT_LIBRARY_DIR = '/home/user/.local/share/qt_libs/5.4/gcc_64/'

### Enter the absolut path to your Qt executable
QT_EXECUTABLE = '/home/user/developement/my_app'

### EDIT THE COPY SETTINGS
#
#       plugins/platforms should always be copied!
#               if your project is using additional plugins add them here
#
##      QML/QtQuick applications
#               if your project is a QML/QtQuick application, add all your dependencies to the qml key
COPY_SETTINGS = {
    'plugins':['platforms'],
}
## Example for qml application:
#COPY_SETTINGS = {
#    'plugins':['platforms', 'imageformats', 'bearer', 'iconengines', 'sqldrivers'],
#    'qml':['QtQuick', 'QtQuick.2', 'QtWebKit', 'QtWebChannel', 'QtWebView', 'QtWebEngine']
#}



# Your Qt application needs to find your libraries, therefore you need to export your library path.
# If you set following option to true a shell script will be generated which does this automatically
CREATE_STARTER = False

# Start a dry run to see which libraries were found
DRY_RUN = True

# ------------------------ NO USER EDITABLE SETTINGS BELOW THIS POINT ------------------------ #

QT_EXECUTABLE_DIR = os.path.dirname(QT_EXECUTABLE)

print(__doc__)
print('script version:', __version__)
print('qt library path:', QT_LIBRARY_DIR)
print('your executable:', QT_EXECUTABLE)

# FUNCTION DEFINITION
def get_subfiles(path, suff='*.so*'):
    matches = []
    for root, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, suff):
            matches.append(os.path.join(root, filename))
    return matches


def get_lib_dependencies(path, qt_libs, recursive=True, libraries = []):
    res = str(subprocess.check_output(["ldd", path])).split(r'\n')
    for e in res:
        if qt_libs in e:
            lib = os.path.normpath(re.search(r'.*=> (.*) \(', e).group(1))
            if lib not in libraries:
                libraries.append(lib)
                if recursive:
                    libraries = get_lib_dependencies(lib, qt_libs, True, libraries)
    return libraries

def get_dependencies(path, qt_libs, copy_settings, recursive=True):
    libraries = get_lib_dependencies(path, qt_libs)
    for key in copy_settings.keys():
        for element in copy_settings[key]:
            path = QT_LIBRARY_DIR + key + '/' + element
            if os.path.isfile(path):
                libraries = get_lib_dependencies(path, qt_libs, recursive, libraries)
            else:
                files = get_subfiles(path)
                for f in files:
                    libraries = get_lib_dependencies(f, qt_libs, recursive, libraries)
            if path not in libraries:
                libraries.append(path)
    return libraries

# GATHER INFORMATION AND COPY FILES
print('Getting dependencies...')
deps = get_dependencies(QT_EXECUTABLE, QT_LIBRARY_DIR, COPY_SETTINGS)
print('done.')

if DRY_RUN:
    print('DRY_RUN! -', 'Following dependencies found:')
    for dep in deps:
        print(dep)
else:
    print('copying dependencies...')
    for dep in deps:
        if os.path.isfile(dep):
            shutil.copy(dep, QT_EXECUTABLE_DIR)   
        elif os.path.isdir(dep):
            shutil.copytree(dep, QT_EXECUTABLE_DIR + '/' +  os.path.basename(dep))
        else:
            print('UNKNOWN ERROR!')
        print(dep, 'copied.')
    
    if CREATE_STARTER:
        f = open(QT_EXECUTABLE + '.sh', 'w')
        f.write("""#!/bin/sh
appname=`basename $0 | sed s,\.sh$,,`

dirname=`dirname $0`
tmp="${dirname#?}"

if [ "${dirname%$tmp}" != "/" ]; then
dirname=$PWD/$dirname
fi
LD_LIBRARY_PATH=$dirname
export LD_LIBRARY_PATH
$dirname/$appname "$@"
""")
        f.close()
