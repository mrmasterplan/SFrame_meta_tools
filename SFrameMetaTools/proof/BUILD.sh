# $Id$

if [ "$1" = "clean" ]; then
    make distclean
    exit 0
fi

if [ "x" != "x" ]; then
    echo "Running on PROOF-Lite, skipping build"
    exit 0
fi

make default
