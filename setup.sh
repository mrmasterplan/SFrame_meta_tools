
#This needs to be sourced.


previous_PWD=$PWD
previous_OLDPWD=$OLDPWD

cd $(dirname $BASH_SOURCE)
SFrame_meta_tool_dir="$(pwd)"
cd $previous_PWD
OLDPWD=$previous_OLDPWD

unset previous_PWD
unset previous_OLDPWD

#Set up so that I can use the tools:

export PATH="${SFrame_meta_tool_dir}/bin:${PATH}"
export PYTHONPATH="${SFrame_meta_tool_dir}/python:${PYTHONPATH}"

unset SFrame_meta_tool_dir