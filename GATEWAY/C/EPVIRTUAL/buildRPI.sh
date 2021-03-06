#!/bin/sh
#
#  Copyright 2014-2016 CyberVision, Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
COMPRPI="/rpi_root/tools/arm-bcm2708/gcc-linaro-arm-linux-gnueabihf-raspbian-x64/bin/arm-linux-gnueabihf-gcc"
PROJECT_HOME=$(pwd)
KAA_LIB_PATH="libs/kaa"
KAA_C_LIB_HEADER_PATH="$KAA_LIB_PATH/src"
KAA_CPP_LIB_HEADER_PATH="$KAA_LIB_PATH/kaa"
KAA_SDK_TAR="kaa-c*.tar.gz"

help_message() {
    echo "Choose one of the following: {build|run|deploy|clean}"
    exit 1
}

if [ ! -d "$KAA_C_LIB_HEADER_PATH"  -a ! -d "$KAA_CPP_LIB_HEADER_PATH" ]
then
    KAA_SDK_TAR_NAME=$(find $PROJECT_HOME -iname $KAA_SDK_TAR)

    if [ -z "$KAA_SDK_TAR_NAME" ]
    then
        echo "Please, put the generated C/C++ SDK tarball into the libs/kaa folder and re-run the script."
        exit 1
    fi

    mkdir -p $KAA_LIB_PATH
    tar -zxf $KAA_SDK_TAR_NAME -C $KAA_LIB_PATH
fi

build() {
    mkdir -p "$PROJECT_HOME/build"
    cd "$PROJECT_HOME/build"
    cmake -DKAA_MAX_LOG_LEVEL=5 -DCMAKE_C_COMPILER="$PROJECT_HOME$COMPRPI" -DBUILD_TESTING=OFF ..
    make
}

run() {
    cd "$PROJECT_HOME/build"
    ./epvirtual
}

clean() {
    rm -rf "$PROJECT_HOME/build"
}

case "$1" in
    build)
        build
    ;;

    run)
        run
    ;;

    deploy)
        clean
        build
        run
    ;;

    clean)
        clean
    ;;

    *)
        help_message
    ;;
esac
