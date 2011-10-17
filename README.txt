This is a collection of tools that I have written in order to facilitate as
many repetitive and tedious tasks a possible when working with sframe and
root. May they be helpful to you.
    Simon Heisterkamp


SETUP
=====
To set up the tools in bash, please just source the setup.sh:

    $ source SFrame_meta_tools/setup.sh

Please note: The above setup script has been written for the bash shell.
The setup is quite simple and can easily be reproduced for other shells.
If you make you own setup scrip for another shell, please send it to me 
so that I can include it in the release. Email: simonhe <AT> nbi.dk

Short Decription
================
All tools are located in the bin/ folder.
Most tools can provide usage info by calling them with -h.

sframe_create_full_cycle.py:
----------------------------
    can create a full working sframe cycle. See a detailed readme in
    README/README_sframe_create_full_cycle.txt

root_varlist
------------
    A tool to print the list of variables that are contained in a TTree.
    The variables are printed as C++ declarations that can be used directly.
    Alternatively the list can be modified and used as input to the other
    tools in this collection.

root_varlist_diff
-----------------
    A tool to find the difference in variables between two files. The files
    can be root-files or text files with variable definitions, or one of each.

rootbrowse
----------
    Start a root TBrowser wihtout a root command line. Any files that are
    supplied on the command line are opened and accessible within the 
    TBrowser. This TBrowser can be run in the background by supplying '&' on 
    the command line.

root_eventcount
---------------
    Counts the number of events in TTrees.

SFrame bugfix for fixed location root installations:
====================================================
    SFrame relies on the root enviroment variables being set up correctly.
    If those are not found it tries to look in a few standard places for the 
    files that it needs. Unfortunately for us (NBI) our installation was 
    non-standard so SFrame doesn't work out of the box. Add the following 
    change to make SFrame work:
    
    In the files 
        - $SFRAME_DIR/Makefile.common
        - $SFRAME_DIR/python/PARHelpers.py
    find the following lines:
"""
ARCH_LOC_1 := $(wildcard $(shell root-config --prefix)/test/Makefile.arch)
ARCH_LOC_2 := $(wildcard $(shell root-config --prefix)/share/root/test/Makefile.arch)
ARCH_LOC_3 := $(wildcard $(shell root-config --prefix)/share/doc/root/test/Makefile.arch)
ifneq ($(strip $(ARCH_LOC_1)),)
  $(info Using $(ARCH_LOC_1))
  include $(ARCH_LOC_1)
else
  ifneq ($(strip $(ARCH_LOC_2)),)
    $(info Using $(ARCH_LOC_2))
    include $(ARCH_LOC_2)
  else
    ifneq ($(strip $(ARCH_LOC_3)),)
      $(info Using $(ARCH_LOC_3))
      include $(ARCH_LOC_3)
    else
      $(error Could not find Makefile.arch!)
    endif
  endif
endif
"""
    
    and replace them with these lines:

"""
ARCH_LOC_1 := $(wildcard $(shell root-config --prefix)/test/Makefile.arch)
ARCH_LOC_2 := $(wildcard $(shell root-config --prefix)/share/root/test/Makefile.arch)
ARCH_LOC_3 := $(wildcard $(shell root-config --prefix)/share/doc/root/test/Makefile.arch)
ARCH_LOC_4 := $(wildcard $(shell root-config --prefix)/share/doc/root-$(shell root-config --version | tr '/' '.')/test/Makefile.arch)
ifneq ($(strip $(ARCH_LOC_1)),)
  $(info Using $(ARCH_LOC_1))
  include $(ARCH_LOC_1)
else
  ifneq ($(strip $(ARCH_LOC_2)),)
    $(info Using $(ARCH_LOC_2))
    include $(ARCH_LOC_2)
  else
    ifneq ($(strip $(ARCH_LOC_3)),)
      $(info Using $(ARCH_LOC_3))
      include $(ARCH_LOC_3)
    else
      ifneq ($(strip $(ARCH_LOC_4)),)
        $(info Using $(ARCH_LOC_4))
        include $(ARCH_LOC_4)
      else
        $(error Could not find Makefile.arch!)
      endif
    endif
  endif
endif
"""

    that's it. Compile and enjoy.