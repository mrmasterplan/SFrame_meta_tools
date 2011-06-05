#!/usr/bin/env python
# encoding: utf-8
"""
create.py

Created by Simon Heisterkamp on 2011-03-31.
"""

# TODO: Mark with a comment when variables only appear in some files

help_message="""This is MakeVarList.py. 
Usage:
	./MakeVarList.py [-i Varlist.C] [-o Varlist.C] [-n treename] file1.root [file2.root ... ]

Effects:
	-i Varlist.C : A previous list of variables. The result will be the union
	               of this list and the variables in the root-files
	-o Varlist.C : The output. If this is omitted, stdout will be used.
	-n treename  : The name of the TTree in the input files that is to be used.
	               If no name is provided, the first TTree in the first file will be used.
	file.root    : The files from which to read the list of variables.
"""

import sys, os, getopt, ROOT, re

def main():
	opt=UserOptions()
	global gerr
	global gout
	try:
		try:
			gout=open(opt.outfile,"w")
			gerr=sys.stdout
		except IOError,e:
			print >>sys.stderr, "Unable to open",opt.outfile
			return 0
	except AttributeError,e:
		gout=sys.stdout
		gerr=sys.stderr
	
	tan=TreeAnalyzer(opt.treename)
	
	try:
		vlist=DeclarationReader(opt.prevfile)
		vset=set([leaf.name for leaf in vlist])
	except AttributeError,e:
		vlist=[]
		vset=set()
	
	for name in opt.infiles:
		if tan.GetTree(name):
			leaves=tan.GetLeaves()
			for leaf in leaves:
				if not leaf.name in vset:
					vset.add(leaf.name)
					vlist.append(leaf)
	
	for leaf in vlist:
		print >>gout, "\t%s %s%s;"%(leaf.typename,leaf.point,leaf.name)

class TreeAnalyzer(object):
	def __init__(self, treename=None):
		super(TreeAnalyzer, self).__init__()
		self.treename=treename
	
	
	def GetTree(self, filename,treename=None):
		if treename:
			self.treename=treename
		self.infile=ROOT.TFile.Open(filename)
		
		if not self.infile:
			print >>gerr, "Unable to open",filename
			return None
		if not self.treename:
			print >>gerr,"No treename set, searching the file."
			objs=[key.ReadObj() for key in TCollToList(self.infile.GetListOfKeys())]
			trees=[obj for obj in objs if obj.IsA().InheritsFrom("TTree")]
			if not trees:
				print >>gerr,"No TTrees found in",filename
				return None
			
			self.tree=trees[0]
			self.treename=self.tree.GetName()			
			print >>gerr,"Using tree name","\""+self.treename+"\""
			
		else:
			self.tree=self.infile.Get(self.treename)
		
		if not self.tree:
			print >>gerr, "Tree",self.treename,"not found in",filename
			return None
		return self.treename
	
	
	def GetLeaves(self):
		import ROOT
		
		self.leaves=[]
		for branch in TCollToList(self.tree.GetListOfBranches()):
			for leaf in TCollToList(branch.GetListOfLeaves()):
				point=""
				if type(leaf) in [ROOT.TLeafElement,ROOT.TLeafObject]:
					point="*"
				self.leaves.append(Variable(leaf.GetTypeName(),point,leaf.GetName()))
		#print >>gerr, "Found",len(self.leaves),"leaves."
		return self.leaves


#Takes any TCollection and returns a python list
def TCollToList(tcoll):
	import ROOT
	
	it=ROOT.TIter(tcoll)
	it.Reset()
	pos=[]
	while 1:
		po = it.Next()
		if not po:
			break
		pos.append(po)
	return pos #Stupid ROOT

class Variable:
	"""Simple Dummy class to contain a variable type, a name and whether it is pointery."""
	def __init__(self, typename,point,name):
		self.typename = typename
		self.point = point
		self.name = name



def DeclarationReader(selfile):
	pat=re.compile(	"""^\s*(?P<type>\w+(?:\s*<.+>)?)\s+(?P<point>\*?)\s*(?P<name>[a-zA-Z_][a-zA-Z_0-9]*)[\s;]*$""",flags=re.MULTILINE)
	
	leaves=[]
	#print "Selecting leaves:"
	for match in pat.finditer(remCcomments(open(selfile).read())):
		#print match.group("name")
		leaves.append(Variable(match.group("type"),match.group("point"),match.group("name")))
	
	return leaves

def remCcomments(instring):
	import re
	"""Removes every C/C++ style comment in a string."""
	#first remove /* */ style comments
	#needs to go via re.compile since re.sub only supposrts the flag argument since 2.7
	pat=re.compile("""/\*.*?\*/""",flags=re.DOTALL)
	outstring=pat.sub("""\n""",instring)
	#then remove // style comments
	return re.sub("""//.*\n""","""\n""",outstring)


#################################################################
#
#    Handle user options:
#
#################################################################

class UserOptions(object):	
	class Usage(Exception):
		def __init__(self,msg):
			self.msg = msg
		def Print(self):
			if self.msg:
				print >>sys.stderr, self.msg
			print >>sys.stderr, help_message
			
	
	"""docstring for UserOptions"""
	def __init__(self, argv=sys.argv):
		super(UserOptions, self).__init__()
		self.treename=None
		self.infiles=[]
		try:
			try:
				opts, args = getopt.getopt(argv[1:], "i:o:n:h",[])
			except getopt.error, msg:
				raise UserOptions.Usage(msg)
			
			# option processing
			for option, value in opts:
				if option =="-i":
					self.prevfile=value
				if option == "-h":
					raise UserOptions.Usage("")
				if option == "-n":
					self.treename=value
				if option == "-o":
					self.outfile=value
			
			if not args:
				raise self.Usage("Please provide some input files")
			self.infiles=args
		
		
		except UserOptions.Usage, err:
			err.Print()
			sys.exit(-1)
	



#################################################################
#
#    IfMain
#
#################################################################


if __name__ == "__main__":
	sys.exit(main())

