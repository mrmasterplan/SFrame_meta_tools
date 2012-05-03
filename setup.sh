#This needs to be sourced.


# find out where this script is located.
# this line is what allows you to source this script from anywhere

export SFRAME_META_TOOL_DIR=$(python -c "from os.path import *; print abspath(expanduser(dirname('$BASH_SOURCE')))")

#Set up so that I can use the tools:

export PATH="${SFRAME_META_TOOL_DIR}/bin:${PATH}"
export PYTHONPATH="${SFRAME_META_TOOL_DIR}/python:${PYTHONPATH}"

