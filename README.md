# Find all needed Qt libraries for your app
This script should find all linked Qt libraries for you executable to deploy a dynamically linked Qt app.

**Currently only QtWidgets applications are supported. QML support is experimental.**

# Requirements
- Python 3
- ldd (shell command to print shared library dependencies)
    
# How does it work?
Just set the `QT_LIBRARY_DIR` to your locally installed Qt library and the `QT_EXECUTABLE` to your application path.
You should update the `COPY_SETTINGS` in order to get all plugins or qml files you need.

Then run the script!

It will copy all required library files to your app directory.

# Run your app
To run your app in a Qt-free environment it needs to know where to look for the library files. Therefore you have to set the `LD_LIBRARY_PATH` to `.`.
The script can also create a starter which does this for you. Just set `CREATE_STARTER` to `True` and make it executable afterwards.
