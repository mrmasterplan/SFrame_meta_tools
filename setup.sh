#This needs to be sourced.


# find out where this script is located.
# this line is what allows you to source this script from anywhere

SFrame_meta_tool_dir=$(python -c "from os.path import *; print abspath(expanduser(dirname('$BASH_SOURCE')))")

#Set up so that I can use the tools:

export PATH="${SFrame_meta_tool_dir}/bin:${PATH}"
export PYTHONPATH="${SFrame_meta_tool_dir}/python:${PYTHONPATH}"

#we don't want this to hand around:
unset SFrame_meta_tool_dir
