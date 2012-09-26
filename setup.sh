#This needs to be sourced.


# find out where this script is located.
# this line is what allows you to source this script from anywhere

export SFRAME_META_TOOL_DIR="$( cd $( dirname "${BASH_SOURCE[0]}" ) && pwd )"

#Set up so that I can use the tools:

export PATH="${SFRAME_META_TOOL_DIR}/bin:${PATH}"
export PYTHONPATH="${SFRAME_META_TOOL_DIR}/python:${PYTHONPATH}"

python $SFRAME_META_TOOL_DIR/python/library_version_string_facility.py
