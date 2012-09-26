
#include "SFrameMetaTools/include/SFrameMetaTools.h"

#include "TSystem.h"
#include <vector>
#include <map>

#include <iostream>

using namespace std;

typedef std::map<std::string,std::string> strmap;

static strmap GetAllLibraryVersionInfoStrings();

namespace SFrameMetaTools {
    std::string GetLibVersionString(){
        strmap infos = GetAllLibraryVersionInfoStrings();

        string output;
        strmap::iterator it = infos.begin();
        for ( ; it!=infos.end(); ++it ) {
            output+=it->second;
        }

        return output;
        return "<<place-holder>>";
    }
}

// #include <iostream>
#include <dlfcn.h>
#include <stdio.h>

// Utility function.
// static linkage prevents the symbol from being exported
static strmap GetAllLibraryVersionInfoStrings()
{
    TString all_libs(gSystem->GetLibraries());
    TString sframe_lib_path = gSystem->Getenv("SFRAME_LIB_PATH");
    vector<TString> lib_names(0);
    // std::cout<<"now printing "<<lib_names.size()<<" libraries"<<std::endl;
    unsigned int curr_index=0;
    int next_index=0;
    unsigned int size = all_libs.Sizeof();
    
    for ( size_t lib_i = 0; lib_i <size; ++lib_i ) {
        next_index = all_libs.Index(" ",1,curr_index,TString::kExact);
        
        if(next_index<0){
            next_index = size;
        }
        // std::cout<<"size "<<size<<" curr "<<curr_index<<" next "<<next_index<<std::endl;
        TString lib = all_libs(curr_index,next_index-curr_index);
        if(lib.BeginsWith(sframe_lib_path)){
            lib_names.push_back(lib);
        }
        
        curr_index = next_index+1;
    }
    
    strmap versions;
    
    for ( size_t i = 0; i < lib_names.size(); ++i ) {
        // std::cout<<lib_names[i]<<std::endl;
        string path = lib_names[i].Data();
        int index_start=path.rfind("/lib")+4;
    
        string lib_name = path.substr(index_start-3,path.size()-index_start+3);
    
        string symbol = path.substr(index_start,path.size()-index_start-3);
        symbol = "_"+symbol+"_version_info";
    
        // std::cout<<"Looking for symbol "<<symbol<<" in "<<path<<std::endl;
        
        void* handle =0;
        handle = dlopen(path.c_str(), RTLD_LAZY | RTLD_NOLOAD);
        if ( not handle) {
            // std::cerr << "Cannot open library: \n" << dlerror() << '\n';
            continue;
        }
        // std::cout<<"Library opened, loading symbol."<<std::endl;
    
        char *info=0;
        dlerror();
        info = (char*) dlsym(handle, symbol.c_str());
        
        if (dlerror()) {
            // std::cout << "Cannot load symbol '"<<symbol<<"'"<< '\n';
            dlclose(handle);
            continue;
        }

        // std::cout<<"Text is: "<<info<<std::endl;
        // std::cout<<info[0]<<info[1]<<info[2]<<info[3]<<info[4]<<info[5]<<info[6]<<std::endl;
        
        versions[lib_name] = info;
        dlclose(handle);
        // 
        // std::cout<<"Version info from "<<path<<":"<<std::endl;
        // std::cout<<versions[lib_name]<<std::endl;
    }
    return versions;
}
