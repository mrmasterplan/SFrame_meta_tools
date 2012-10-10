#!/bin/sh

function sframe_svn_setignore {
    local LIBRARY="$(grep LIBRARY Makefile | sed 's/LIBRARY *=* *//g')"
    local NL=$'\n'

    local PREV="$(svn propget svn:ignore .)"
    svn propset svn:ignore "${PREV}${NL}obj${NL}.sframe.\*" .
    local PREV="$(svn propget svn:ignore src)"
    svn propset svn:ignore "${PREV}${NL}${LIBRARY}_Dict.h${NL}${LIBRARY}_Dict.cxx${NL}_${LIBRARY}_version_info.cxx" src

    echo "Now ignoring:"
    echo "   obj/"
    echo "   .sframe.\*"
    echo "   src/${LIBRARY}_Dict.h"
    echo "   src/${LIBRARY}_Dict.cxx"
    echo "   src/_${LIBRARY}_version_info.cxx"
    echo "If you have trouble checking in please run 'svn up' first."
    echo "You can edit the ignores by calling 'svn propedit svn:ignore .' in any directory." 
}

sframe_svn_setignore

unset sframe_svn_setignore