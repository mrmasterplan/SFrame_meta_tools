// $Id$

int SETUP() {

   /// Add all the additional libraries here that this package
   /// depends on. (With the same command that loads this package's library...)
   if( gSystem->Load( "libSFrameMetaTools" ) == -1 ) return -1;

   return 0;
}
