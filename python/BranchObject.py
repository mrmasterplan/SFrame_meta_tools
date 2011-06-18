
## @short Class the contain the information related to one variable.tree-branch
#
# This is a simple container class that holds, aomngst other things the 
# type-name and name of a variable. A list of instances of this class is created
# either by parsing a list of variable declarations or from a TTree inside a 
# root-file in the course of the cycle-creation.
class Variable( object ):
    """
    One of the variables that will be used in the cycle.
    A variable has a name and a typename.
    A variable can be and stl-container where the input declaration must be a pointer etc.
    A variable can be commented out, in which case it will be included in the cycle, 
    but as being commented out.
    
    A list of variables is assembled either by the TreeReader directly from a root-file, 
    or by the VariableSelectionReader from a C-like file with variable declarations.
    """
    
    @classmethod
    def ReadFromString(cls,line):
        import re
        # Definitions may start with a //.
        # After that I expect there to be a typename of the form UInt_t or int or std::vector<double> etc.
        # then a name, 
        # and finally a semicolon
        query="""^[ \t]*(?P<comment>(?://)?)[ \t]*""" # First find out if the line is commented
        # next is the typename which starts with a word chracter [a-zA-Z_]
        query+="""(?P<type>[a-zA-Z_][a-zA-Z0-9_:]*(?:[ \t]*<.*>)?)""" 
        # but can from there on also contain numbers [a-zA-Z_0-9:]*
        # finally it may contain a template structure (?:[ \t]*<.*>)?
        # next comes the issue of pointers. 
        query+="""(?:(?:[ \t]*(?P<point>\*)[ \t]*)|(?:(?<!\*)[ \t]+(?!\*)))"""
        # if there is a star, it can have whitespaces before or after.
        # if there is no star, there must be some whitespace which is neiter preceded nor succede by a star.
        # and now for the name
        query+="""(?P<name>[a-zA-Z_][a-zA-Z_0-9]*)[ \t]*;[ \t]*"""
        # finally there may be a comment with the variable.
        # in a TTree this is usually saved in the title.
        query+="""(?P<title>//.*)?$"""
        match = re.match(query,line)
        # print "line:",line
        # print "query:",repr(query)
        # print "match was",match
        if not match:
            return None
        commented = match.group( "comment" ) # whether the variable was commented out. Will be '//' if it was, or "" if it wasn't
        typename = match.group( "type" )
        name = match.group( "name" )
        pointer = match.group( "point" )
        title = match.group( "title" )
        return cls(name=name, typename=typename,pointer=pointer, commented=commented,title=title)
        
    
    ## @short Constructor of the Variable class
    #
    # This function takes the arguments and saves them as member variables.
    # on top of that, it sanitizes the name to create a member called cname
    # that is suitable as a c++ variable name.
    #
    # @param name The name of the variable.
    # @param typename The type of the variable, such as int or vector<float> etc.
    # @param name The name of the variable.
    # @param commeneted Should be eiter "" or "//" to indicate wheter to use this variable or not
    # @param pointer Should be eiter "" or "*" to indicate whether this variable needs to be accessed as an object.
    def __init__( self, name, typename="", pointer="", commented="", title="" ):
        super( Variable, self ).__init__()
        self.SetName(name)
        self.SetTypeName(typename)
        self.SetPointer(pointer)
        self.SetCommented(commented)
        self.SetTitle(title)
        self._typelength=0
        self._namelength=0
        self.mc=0
    
    def SetName(self,name):
        self._name = name
        # Sanitize the name. Root names can be anything.
        # We must be careful to have a valid C++ variable name in front of us
        import re
        cname = re.sub( """[^_0-9a-zA-Z]""", "_", name )  # These are the only valid characters in C++ variable names
        if not re.match( "[a-zA-Z_]", cname ):  # furthermore, the name must start with a letter, not a number
            cname = "_" + cname
        
        if cname != name:
            print >>sys.stderr, "WARNING: Illegal characters in variable name \"%s\", using \"%s\" instead. " % (self.name, self.cname)
        self._cname = cname
    
    def GetName(self):
        return self._name
    
    name = property(GetName,SetName)
    
    def GetTypeName(self):
        return self._typename
    
    def SetTypeName(self,typename):
        self._typename=typename
    
    typename = property(GetTypeName,SetTypeName)
    
    @property
    def cname(self):
        return self._cname
    
    def SetPointer(self,pointer):
        if pointer not in ("","*"):
            if pointer:
                pointer="*"
            else:
                pointer=""
        self._pointer = pointer
    
    def GetPointer(self):
        return self._pointer
    
    pointer = property(GetPointer,SetPointer)
    
    def SetCommented(self,commented):
        if commented not in ("","// "):
            if commented:
                commented="// "
            else:
                commented=""
        self._commented = commented
    
    def GetCommented(self):
        return self._commented
    
    commented = property(GetCommented,SetCommented)
    
    def SetTitle(self,title):
        if not title or title==self._name:
            self._title=""
            return
        #make it commented so that it is easy to print
        title = title.strip()
        if title[:2]!="//":
            title="// "+title
        if self.name != self.cname:
            title=title+" (real name: %s)"%self.name
        self._title = title
        
    def GetTitle(self):
        return self._title
    
    title = property(GetTitle,SetTitle)
    
    def SetTypeLength(self,i):
        self._typelength=i
    
    def GetTypeLength(self):
        if not self._typelength:
            self._typelength = len("%s%s "% (self.commented, self._typename) )
        return self._typelength
    
    typelength=property(GetTypeLength,SetTypeLength)
    
    def SetNameLength(self,i):
        self._namelength = i
    
    def GetNameLength(self):
        if not self._namelength:
            self._namelength = len("%s%s; " % (self.pointer, self.name))
        return self._namelength
    
    namelength = property(GetNameLength,SetNameLength)
    
    def StdPointName(self):
        return ("%-"+str(self.namelength)+"s")%("%s%s; " % (self.pointer, self.cname))
    
    def StdTypeName(self):
        return ("%-"+str(self.typelength)+"s") % (self.commented+ self._typename)
    
    def StdCName(self):
        return ("%-"+str(self.namelength)+"s")%(self.cname)
    
    def Declaration(self):
        return self.StdTypeName()+self.StdPointName()+self.title
    
    def __repr__(self):
        return "Variable(%s, %s, %s, %s, %s )"%(repr(self.name),repr(self.typename),repr(self.pointer),repr(self.commented),repr(self.title))
        
    def __str__(self):
        return self.Declaration()
    
    def __hash__(self):
        return hash("%s%s"%(self.typename,self.name))
    
    def __eq__(self,other):
        return hash(self)==hash(other)
    
    def __ne__(self,other):
        return not self==other
    # End of Class Variable

## @short Function to read the variable declarations from a file
#
# The function uses regular expressions to read a list of c++ 
# variable declarations from a file and assembles a list of 
# "Variable" instances.
# 
# The file should contain at most one variable declaration per line.
# Commented out variable declarations are used and flagged as commented.
# Other comments are ignored as long as they do not resemble declarations.
# Objects that need to be accessed as pointers, such as stl vectors, should
# be declared as pointers, as done by the ROOT MakeClass, for example.
#
# The returned object has the same structure as that returned by ROOT_Access.ReadVars
#
# @param fileName Path of the file that contains the list of variables.
def ReadVariableSelection( filename ):
    """
    Reads a list of variable declarations from file into a structured format.
    From there they can be used to create the declarations and 
    connect-statements necessary to use the variables in a cycle.
    """
    varlist = []
    try:
        text = open( filename ).read()
    except:
        print "Unable to open variable selection file", "\"%s\"" % filename
        return varlist
    
    import re
    # Use some regexp magic to change all /*...*/ style comments to // style comments
    text = re.sub( """\*/(?!\n)""", "*/\n", text ) # append newline to every */ that isn't already followed by one
    text = re.sub( """(?<!\n)/\*""", "\n/*", text ) # prepend newline to every /* that isn't already preceded by one
    while re.search( """/\*""", text ):  # While ther still are /* comments
        text = re.sub( """/\*(?P<line>.*?)(?=\n|\*/)""", """// \g<line>/*""", text ) # move the /* to the next newline or */
        text = re.sub( """/\*\*/""", "", text )  # remove zero content comments
        text = re.sub( """/\*\n""", "\n/*", text ) # move the /* past the newline
    
    # text = re.sub("""(?<!\n)//""","\n//", text ) # Make sure // always starts a new line
    text = re.sub("""(?<=\n)(\s)+""","", text ) # clean up any sequence of successive whitespaces starting with a newline
    text = re.sub("""^(\s)+""","", text ) # clean up any sequence of successive whitespaces at the start of the file
    text = re.sub("""(\s)+(?=\n)""","", text ) # clean up any sequence of successive whitespaces at line endings
    
    # the text should now be quite tidy and ready for parsing.
    
    # Find every variable definition.
    namelength=0
    typelength=0
    for line in text.splitlines():
        var = Variable.ReadFromString(line)
        if var:
            varlist.append(var)
            namelength=max(namelength,var.namelength)
            typelength=max(typelength,var.typelength)
    for var in varlist:
        var.typelength=typelength
        var.namelength=namelength
    return varlist

if __name__ == '__main__':
    import sys
    for var in ReadVariableSelection(sys.argv[-1]):
        print var