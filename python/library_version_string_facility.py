#!/usr/bin/env python

"""
The idea here is to automatically create a version string for a library.
The string should contain the compile path, the SFrame version, the ROOT version
and a few other things in a machine and human readable format like:

$Item: Some info here in any format.\n

The string will be placed in a file called
_$(LIBRARY)_version_info.cxx in the project source directory.
It will be included in the compilation of the library as a const char * string literal
called _$(LIBRARY)_version_info.

The makefile will be modified to regenerate this file each time the library is reconstructed.

Another program called "sframe_read_version" will be supplied to read the version string from a
specified library and dump it to the screen.

"""

# version_file_path = "$(SRCDIR)/_$(LIBRARY)_version_info.$(SrcSuf)"
SFrame_Makefile_common="$SFRAME_DIR/Makefile.common"

package_makefile_path = "Makefile"

import os, re, sys

def version_info(library):
    output=["_%s_version_info:"%library]
    output+=["Library name: %s"%library]
    try:
        import datetime
        output+=["Date: "+datetime.datetime.now().ctime().strip()]
    except:
        pass
    
    try:
        local_svn_info = command_output("svn info 2>/dev/null")
        if local_svn_info:
            output+=["Library svn url: "+re.search(r"URL: (.*)",local_svn_info).group(1)]
            output+=["Library svn revision: "+re.search(r"Revision: (.*)",local_svn_info).group(1)]
        else:
            output+=["Library is not using svn"]
    except:
        output+=["Library is not using svn"]
    output+=["Library path: "+os.getcwd()]
    
    if command_output("which root-config 2>/dev/null"):
        try:
            output+=["ROOT version: "+command_output("root-config --version")]
        except:
            output+=["ROOT version not available"]
    else:
        output+=["ROOT version not available"]
        
    if "SFRAME_DIR" in os.environ:
        try:
            sframe_svn_info = command_output("cd $SFRAME_DIR; svn info")
            if sframe_svn_info:
                output+=["SFrame svn url: "+re.search(r"URL: (.*)",sframe_svn_info).group(1)]
                output+=["SFrame svn revision: "+re.search(r"Revision: (.*)",sframe_svn_info).group(1)]
            else:
                output+=["SFrame is not using svn"]
        except:
            output+=["SFrame is not using svn"]
    output+=["Compiled by: "+command_output("whoami")]
    maxlen = max([len(s) for s in output])
    pat = "    \"%%-%ds   \\n\"\n"%maxlen
    out_str="\n"
    for s in output:
        out_str+=pat%s
    # out_str+="\""
    return out_str
    # return "\"%s\""%output.replace(r"\\",r"\\\\").replace("\n","    \\n\\\n").replace("\"","\\\"")
    
def recreate_version_file(library,version_file_path):
    # make_vars = parse_local_makefile()
    path = version_file_path
    name = "_%s_version_info" %library
    file = open(path,"w")
    file.write("\n\n//AUTO-GENERATED VERSION INFO.\n//This string is accessible from sframe_read_version in SFrame_meta_tools.\n\n")
    file.write("\nextern const char %(name)s[] = %(info)s;\n\n"%dict(name=name,info=version_info(library)))
    # file.write("\nconst char *%(name)s = %(info)s;\n\n"%dict(name=name,info=version_info(library)))
    file.close()


def modify_sframe_makefile():
    path = os.path.expandvars(SFrame_Makefile_common)
    # make a backup
    if not os.path.exists(path+".backup"):
        backup = open(path+".backup","w")
        backup.write(open(path).read())
        backup.close()
    newfile =""
    for line in open(path+".backup"):
        if line == "DICTLDEF  = $(INCDIR)/$(LIBRARY)_LinkDef.h\n":
            newfile+=line
            newfile+="VERSION_FILE = $(SRCDIR)/_$(LIBRARY)_version_info.$(SrcSuf)\n"
            newfile+="VERSION_OBJ = _$(LIBRARY)_version_info.$(ObjSuf)\n"
            newfile+="ifeq (,$(SFRAME_META_TOOL_DIR))\n"
            newfile+="VERSION_OBJ =\n"
            newfile+="endif\n"
        elif line =='\t@echo "Making shared library: $(SHLIBFILE)"\n':
            newfile+=line
            newfile+="ifneq (,$(SFRAME_META_TOOL_DIR))\n"
            newfile+="\t@sframe_write_version_string_file $(LIBRARY) $(VERSION_FILE)\n"
            newfile+="\t@$(CXX) $(CXXFLAGS) -c $(VERSION_FILE) -o $(OBJDIR)/$(VERSION_OBJ)\n"
            newfile+="endif\n"
        elif "$(addprefix $(OBJDIR)/,$(OLIST))" in line:
            newfile+=line.replace("$(addprefix $(OBJDIR)/,$(OLIST))","$(addprefix $(OBJDIR)/,$(OLIST) $(VERSION_OBJ))")
        elif line == "SKIPCPPLIST = $(DICTFILE)\n":
            newfile+= "SKIPCPPLIST = $(DICTFILE) $(VERSION_FILE)\n"
        elif line.startswith("INCLUDES +="):
            newfile+=line.strip()+" -I$(SFRAME_META_TOOL_DIR)/ \n"
        elif line.startswith("distclean:"):
            newfile+=line
            newfile+="\t@rm -f $(VERSION_FILE)\n"
        else:
            newfile+=line
    print "Writing modified",path
    file = open(path,"w")
    file.write(newfile)
    file.close()

def get_version_info(lib_path):
    name=re.sub(r".*lib(.*).so.*",r"\g<1>",lib_path)
    
    nm_out = command_output("nm %s"%lib_path)
    match = re.search(r"([0-9abcdef]+) .*_%(name)s_version_info"%{"name":name},nm_out)
    if not match:
        return ""
    
    # convert the hex address to an integer
    address = int(match.group(1),16) # use base 16
    file = open(lib_path,"rb")
    file.seek(address,0)
    outstr=""
    while not '\0' in outstr:
        outstr+=file.read(500)
        # print outstr
    return outstr[:outstr.index('\0')].strip()
    
    
def command_output(cmd):
    import subprocess
    return subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True).stdout.read().strip("\n")

def main():
    """This function is where the modifiactions of the exisitng Makefile will be made."""
    if not "SFRAME_DIR" in os.environ:
        print >>sys.stderr, "Please set up SFrame first."
        sys.exit(-1)
    modify_sframe_makefile()

if __name__ == '__main__':
    main()
