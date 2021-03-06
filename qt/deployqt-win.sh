#!/bin/sh
#
# deployqt-win.sh --
#  
# Before running this, be sure to:
# 1. Select "Release" build in QtComposer 
# 2. Build Blink1Control
# 3. Do QC Tests
# 4. Type "./deployqt-win.sh" (i.e. must be in this dir)
# 5. Resulting zipped up app will be this directory as "Blink1Control-win.zip"
#
# Wow this is such a hack.  
# Is this really what one must do to make executables on Windows?
# (though MacOSX is not much better)
#
# 2014 Tod E. Kurt, http://thingm.com/
#

# name of resulting directory you want, containing the application
APP_DIR=Blink1Control

# (paths are from the soon-to-be-created APP_DIR
# path to built application executable
EXE_PATH=../../build-blink1control-Desktop_Qt_5_2_1_MinGW_32bit-Release/release/Blink1Control.exe 

# where QML files live
QML_DIR=../../blink1control/qml

# Where "windeployqt.exe" lives (and the mingw libs)
QT_BIN_PATH=/c/qt/Qt5.2.1/5.2.1/mingw48_32/bin

# location of blnik1-lib.dll (do "make lib" in that dir first to get it)
BLINK1_LIB_PATH=../../../commandline/blink1-lib.dll

export PATH=${PATH}:${QT_BIN_PATH}

# make the place where we're going to put the whole app
rm -rf windeploy
mkdir windeploy/${APP_DIR}
pushd windeploy/${APP_DIR}

if [ ! -e $EXE_PATH ] ; then 
    echo "file not found: ${EXE_PATH}"
    popd
    exit
fi

# copy the built executable
cp ${EXE_PATH} .

# copy blink1-lib
cp ${BLINK1_LIB_PATH} .

# copy qml files  (seems like windeployqt should do this, but it doesn't)
cp -r ${QML_DIR} .

# copy mingw libs (seems like windeployqt should do this too)
cp ${QT_BIN_PATH}/lib*dll .

# windeploy to get rest of Qt dependencies
${QT_BIN_PATH}/windeployqt Blink1Control.exe

# fix bug in windeployqt
# see: https://bugreports.qt-project.org/browse/QTBUG-35211
cp ${QT_BIN_PATH}/QtWebProcess.exe .
cp ${QT_BIN_PATH}/Qt5WebKitWidgets.dll .
cp ${QT_BIN_PATH}/Qt5OpenGL.dll .
cp ${QT_BIN_PATH}/Qt5PrintSupport.dll  .
cp ${QT_BIN_PATH}/Qt5MultimediaWidgets.dll  .

# Build a zip bundle
cd ..
zip -r ${APP_DIR}-win.zip ${APP_DIR}

echo "created ${APP_DIR}-win.zip"
mv ${APP_DIR}-win.zip ..

popd


