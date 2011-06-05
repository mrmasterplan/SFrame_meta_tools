#!/usr/bin/env python

import sys
import ROOT
from RootList import TCollToList

class EvCounter(object):
	"""docstring for EvCounter"""
	def __init__(self, treename=""):
		super(EvCounter, self).__init__()
		self.treename = treename
	
	def __call__(self, filename):
		"""docstring for __call__"""
		inf=ROOT.TFile.Open(filename)
		if not inf:
			return 0
		if not self.treename:
			objs=[key.ReadObj() for key in TCollToList(inf.GetListOfKeys())]
			trees=[obj for obj in objs if obj.IsA().InheritsFrom("TTree")]
			if not trees:
				print "No TTrees found in",filename
				return 0
			
			tree=trees[0]
			self.treename=tree.GetName()			
			#print "Using tree name",self.treename
		else:
			tree=inf.Get(self.treename)
		nentries=tree.GetEntries()
		inf.Close()
		return nentries

def main(argv=sys.argv):
	"""docstring for main"""
	evc=EvCounter()
	sumn=0
	for name in argv[1:]:
		n=evc(name)
		sumn+=n
		print name,n,"Total:",sumn
	print "used treename",'\"'+evc.treename+'\"'
	
	
if __name__ == '__main__':
	main()
