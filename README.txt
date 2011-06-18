This is a collection of tools that I have written in order to facilitate as
many repetitive and tedious tasks a possible when working with sframe and
root.

SETUP
=====
To set this up, please just source the setup.sh

Short Decription
================
most tools can provide usage info by calling them with -h.

sframe_create_full_cycle.py:
----------------------------
    can create a full working sframe cycle. See a detailed readme in
    README_sframe_create_full_cycle.txt

root_varlist
------------
    A tool to print the list of variables that are contained in a TTree.
    The variables are printed as C++ declarations that can be used directly.
    Alternatively the list can be modified and used as input to the other
    tools in this collection.

root_varlist_diff
-----------------
    A tool to find the difference in variables between two files. The files
    can be root-files or text files with variable definitions.

rootbrowse
----------
    Start a root TBrowser wihtout a root command line. Any files that are
    supplied on the command line are opened and accessible within the 
    TBrowser. This TBrowser can be backgrounded by supplying '&' on the 
    command line.

root_eventcount
---------------
    Counts the number of events in TTrees.

NEW Sat 18 Jun 2011 17:20:39 CEST:
  sframe_create_full_cycle.py has two new options and some new features.
  
  The option -f or --more-functions will put all the long lists of
  declarations etc. into separate functions. This makes it possible to 
  collapse those functions in an editor.
  
  The option -m or --mc-tags allows you to choose what varibles should be 
  recognized as Monte-Carlo. MC variables are only used within blocks that
  check that they really are dealing with MC input files.
  
