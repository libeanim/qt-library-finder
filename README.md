# Deploy a Qt application with dynamically linked Qt libraries

If you don't have a Qt commercial license but want to distribute your Qt app commercially or in a Qt free environment (as all in one package) you have to dynamically link the Qt libraries. This is due to the [LGPL](https://www.qt.io/qt-licensing-terms/) license Qt uses.

**Last update: March 2015**, be aware that things might have changed.

On **Windows** you can use a [deployment tool](http://doc.qt.io/qt-5/windows-deployment.html) to find all required files and make a dynamic linkage.

On **Linux** however, as there is no no standard package management (Mar. 15), you need to use the `ldd` shell command to find the required library files ([Deployment on Linux](http://doc.qt.io/qt-5/linux-deployment.html)). If you want to do that manually, you just have to run `ldd /path/to/your/app` and look which libraries lie in the Qt installation directory. Additionally you have to check if those libraries depend on other Qt libraries, and so on, until you got all dependencies. This is exactly what this script does:

# Find all needed Qt libraries for your app
The script finds all linked Qt libraries needed by your executable to deploy a dynamically linked Qt app.

**Currently only QtWidgets applications are supported. QML support is experimental.**

## Requirements
- Python 3
- ldd (shell command to print shared library dependencies)

## How does it work?
There is a `QT_LIBRARY_DIR`, `QT_EXECUTABLE` and `COPY_SETTINGS` variable in the python script (qt-library-finder.py):

* Set the `QT_LIBRARY_DIR` to your locally installed Qt library and the
* `QT_EXECUTABLE` to your application path.
* Update the `COPY_SETTINGS` in order to get all plugins or qml files you need.

* Run the script.

It will copy all required library files to your app directory.

## Run your app
To run your app in a Qt-free environment it needs to know where to look for the library files. Therefore you have to set the `LD_LIBRARY_PATH` to `.`.
The script can also create a starter which does this for you. Just set `CREATE_STARTER` to `True` and make it executable afterwards.
