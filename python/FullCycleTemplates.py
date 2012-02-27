## @short The Tab character
#
# Define the tab character to be used during code gerneration
# may be, for example, "\t", "  ", "   " or "    "
# Note: If you want to change the indentation of all the genrated code
# you also need to change it in all the following templates.
tab = " " * 4 # four spaces

## @short Template for namespaced code
#
# This string is used to enclose code bodys in a namespace
namespace = "namespace %(namespace)s {\n\n%(body)s\n} // of namespace %(namespace)s\n"

## @short Template for the body of a header file
#
# This string is used by CreateHeader to create the body of a header file
header_Body = """
/**
 *    @short Put short description of class here
 *
 *          Put a longer description over here...
 *
 *  @author Put your name here
 * @version $Revision: 173 $
 */
class %(class)-s : public SCycleBase {

public:
    /// Default constructor
    %(class)-s();
    /// Default destructor
    ~%(class)-s();

    /// Function called at the beginning of the cycle
    virtual void BeginCycle() throw( SError );
    /// Function called at the end of the cycle
    virtual void EndCycle() throw( SError );

    /// Function called at the beginning of a new input data
    virtual void BeginInputData( const SInputData& ) throw( SError );
    
    /// Function called after finishing to process an input data
    virtual void EndInputData  ( const SInputData& ) throw( SError );

    /// Function called once on the master at the beginning of a new input data
    virtual void BeginMasterInputData( const SInputData& ) throw( SError );
    
    /// Function called once on the master after finishing to process an input data
    virtual void EndMasterInputData  ( const SInputData& ) throw( SError );
    
    /// Function called after opening each new input file
    virtual void BeginInputFile( const SInputData& ) throw( SError );
%(functionDeclarations)s
    /// Function called for every event
    virtual void ExecuteEvent( const SInputData&, Double_t ) throw( SError );

private:
    //
    // Put all your private variables here
    //
    string InTreeName;
    
    // Input Variables
%(inputVariableDeclarations)s

    //Output Variables
%(outputVariableDeclarations)s

    // Macro adding the functions for dictionary generation
    ClassDef( %(fullClassName)s, 1 );

}; // class %(class)-s
"""

ConnectInputVariables_declaration="""   
    /// Function to connect the input variables to the input tree
    virtual void ConnectInputVariables( const SInputData& ) throw( SError );
    """
ConnectInputVariables_body="""
void %(class)-s::ConnectInputVariables( const SInputData& id ) throw( SError ){

    bool isdata = id.GetType().Contains("data",TString::kIgnoreCase);

%(inputVariableConnections)s
}
"""
ConnectInputVariables_call="    ConnectInputVariables(id);\n"

DeclareOutputVariables_declaration="""   
    /// Function to connect the input variables to the input tree
    virtual void DeclareOutputVariables( const SInputData& ) throw( SError );
    """
DeclareOutputVariables_body="""
void %(class)-s::DeclareOutputVariables( const SInputData& id ) throw( SError ){

    bool isdata = id.GetType().Contains("data",TString::kIgnoreCase);

%(outputVariableConnections)s
}
"""
DeclareOutputVariables_call="    DeclareOutputVariables(id);\n"

ClearOutputVariables_declaration="""   
    /// Function to connect the input variables to the input tree
    virtual void ClearOutputVariables() throw( SError );
    """
ClearOutputVariables_body="""
void %(class)-s::ClearOutputVariables() throw( SError ){
%(outputVariableClearing)s
}
"""
ClearOutputVariables_call="    ClearOutputVariables();\n"

StartMCBlock="    if(!isdata) {\n"
CloseMCBlock="    }\n"
## @short Template for a header file
#
# This string is used by CreateHeader to create a header file
# once the body has already been generated
header_Frame = """// Dear emacs, this is -*- c++ -*-
#ifndef %(capclass)-s_H
#define %(capclass)-s_H

// SFrame include(s):
#include \"core/include/SCycleBase.h\"
#include <vector>
#include <string>
using namespace std;

%(body)s

#endif // %(capclass)-s_H

"""

## @short Template for the body of a source file
#
# This string is used by CreateSource to create the body of a source file
source_Body = """
%(class)-s::%(class)-s()
    : SCycleBase() {
    
    DeclareProperty("InTreeName", InTreeName );
    SetLogName( GetName() );
}

%(class)-s::~%(class)-s() {

}

void %(class)-s::BeginCycle() throw( SError ) {

    return;

}

void %(class)-s::EndCycle() throw( SError ) {

    return;

}

void %(class)-s::BeginMasterInputData( const SInputData& ) throw( SError ) {

    return;
}

void %(class)-s::EndMasterInputData( const SInputData& ) throw( SError ) {

	  // You can do fitting here.
    return;

}

void %(class)-s::BeginInputData( const SInputData& id ) throw( SError ) {

    bool isdata = id.GetType().Contains("data",TString::kIgnoreCase);

%(outputVariableConnections)s
    return;

}

void %(class)-s::EndInputData( const SInputData& ) throw( SError ) {

    return;

}

void %(class)-s::BeginInputFile( const SInputData& id ) throw( SError ) {

    bool isdata = id.GetType().Contains("data",TString::kIgnoreCase);

%(inputVariableConnections)s
    return;

}

void %(class)-s::ExecuteEvent( const SInputData& id, Double_t /*weight*/ ) throw( SError ) {

    bool isdata = id.GetType().Contains("data",TString::kIgnoreCase);

%(outputVariableClearing)s

    // The main part of your analysis goes here
    
%(outputVariableFilling)s

    return;

}

%(functionBodys)s
"""

## @short Template for the frame of a source file
#
# This string is used by CreateSource to create a source file
# once the main body has already been generated
source_Frame = """
// Local include(s):
#include \"%(header)s\"

ClassImp( %(fullClassName)s );

%(body)s
"""

## @short Template for a new LinkDef file
#
LinkDef = """// Dear emacs, this is -*- c++ -*-

#ifdef __CINT__

#pragma link off all globals;
#pragma link off all classes;
#pragma link off all functions;
#pragma link C++ nestedclass;

%(new_lines)s
#endif // __CINT__
"""
    
## @short Function to indent a text body
# 
# Evenry line in the string that is passed to this function is prepended with the Tab character
# that is defined as a class member of this class.
# 
# @param text The text body to indent
def Indent( text ):
    import re
    return re.sub( """.+""", """%s\g<0>""" % tab, text )
