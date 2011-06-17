"""
A class to read TTrees from TFiles.
It will try to import pyROOT only once, and tell you if
it failed. After that it will simply shut up and return
empty objects or decent defaults if ROOT was't imported properly.
"""

from BranchObject import Variable
import sys

## @short Class to encapsulate all pyROOT access
#
# This class and its methods represent the only cases where I need
# access to pyROOT. I attempt to import pyROOT only once. It it fails,
# I attempt to give meaningful default values instead.

try:
    import ROOT
except ImportError, e:
    print >>sys.stderr, "ERROR: pyROOT could not be loaded."
    # print "ERROR: You will need to supply the treename and variable list."
    # print "ERROR: use -h or --help to get help."
    ROOT = 0
    
## @short Function to return a python iterator over any TCollection
#
# @param tcoll TCollection to iterate over
def TCollIter( tcoll ):
    """Gives an iterator over anything that the ROOT.TIter can iterate over."""
    if not ROOT:
        return
    it = ROOT.TIter( tcoll )
    it.Reset()
    item = it.Next()
    while item:
        yield item
        item = it.Next()
    return

## @short Function to extract a relavnt tree name froma rootfile
#
# This function looks inside a rootfile and returns the name of 
# the TTree with the largest number of branches. If any problems
# are encountered "TreeName" is returned.
#
# @param rootfile Path of the rootfile to read
def GetTreeName( rootfile, default="TreeName"):
    """
    Get the name of the treename in the file named rootfile.
    Or just return 'TreeName' if any errors show up.
    If several trees are present, get the one with the largest number
    of branches.
    """
    treename = default
    if not ROOT:
        return treename
    
    if not rootfile:
        print >>sys.stderr, "No rootfile given. Using default tree name:", treename
        return treename
    
    f = ROOT.TFile.Open( rootfile )
    if not f:
        print >>sys.stderr, rootfile, "could not be opened. Using default tree name:", treename
        return treename
    # Get a list of all TKeys to TTrees
    trees = [ key for key in TCollIter( f.GetListOfKeys() ) if key.GetClassName() == "TTree" ]
    if len( trees ) == 1:
        # Just 1? Use it
        treename = trees[ 0 ].GetName()
    elif len( trees ) > 1:
        print >>sys.stderr, "Avaliable tree names:", ", ".join( [ key.GetName() for key in trees ] )
        # Find the tree with the largest number of branches.
        nbranch = -1;
        for key in trees:
            tree = key.ReadObj()
            if tree.GetNbranches() > nbranch:
                nbranch = tree.GetNbranches()
                treename = tree.GetName()
    print >>sys.stderr, "Using treename:", treename
    f.Close()
    
    return treename
    
## @short Function to construct a list of Variable instances from a TTree
#
# This function reads a TTree from a rootfile and constructs a list of
# Variable class intances that can be used in the construction of the cycle.
# The returned object has the same structure as that returned by ReadVariableSelection
#
# @param rootfile Path of the rootfile to read
# @param treename Name of the TTree to use
def ReadVars(rootfile, treename ):
    """
    Reads a list of variables from a root-file into a structured 
    format. From there they can be used to create the declarations and connect
    statements necessary to use the variables in a cycle.
    """
    varlist = []
    if not ROOT:
        return varlist
    
    if not rootfile or not treename:
        print >>sys.stderr, "Incomplete arguments. Cannot get tree named \"%s\" from rootfile \"%s\"" % ( treename, rootfile )
        return varlist
    
    f = ROOT.TFile.Open( rootfile )
    if not f:
        print >>sys.stderr, "Could not open root file \"%s\"" % rootfile
        return varlist
    
    tree = f.Get( treename )
    if not tree:
        print >>sys.stderr, "Could not get tree \"%s\"" % treename
        f.Close()
        return varlist
    
    namelength=0
    typelength=0
    for branch in TCollIter( tree.GetListOfBranches() ):
        for leaf in TCollIter( branch.GetListOfLeaves() ):
            pointer = type( leaf ) in (ROOT.TLeafElement, ROOT.TLeafObject)
            var = Variable( name=leaf.GetName(),typename=leaf.GetTypeName(),pointer=pointer,title=leaf.GetTitle())
            varlist.append( var )
            namelength=max(namelength,var.namelength)
            typelength=max(typelength,var.typelength)
    
    for var in varlist:
        var.typelength=typelength
        var.namelength=namelength
    
    f.Close()
    return varlist

