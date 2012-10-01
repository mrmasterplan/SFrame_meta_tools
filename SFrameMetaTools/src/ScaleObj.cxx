#include "include/ScaleObj.h"

/*

    The Scale objects can be used to set ROOT histogram scales.
    They can be implicitly cast to integrs and double*, giving
    the number of bins and bin-edge array respectively.

    Examples of use might be:
    LogScale ptscale(100,10,1000); //make 100 logarithmic bins spanning the range [10,1000)
    h=TH1D("h","h",ptscale,ptscale);

    The possible ScaleObjects are:
    LogScale:   makes logarithmic bins over the range.
    LinScale:   makes linear bins over the range (somewhat unnecessary since it duplicates ROOT's funcionality.)
    CountScale: makes integer sized bins centered on the integer values.

*/

#include <iostream>
#include <TMath.h>

LogScale::LogScale(int m_nbins, double from, double to):ScaleObj(m_nbins)
{
    if(from<=0) {
        std::cerr<<"A logscale cannot start from a negative value"<<std::endl;
        return;
    }
    if(to<=from) {
        std::cerr<<"A logscale must go over a positive interval"<<std::endl;
        return;
    }
    if(nbins<1) {
        std::cerr<<"A logscale must have at least one bin"<<std::endl;
        return;
    }

    double interval = to/from;

    double step=TMath::Power(interval,1./nbins);

    binedges[0]=from;
    for(int i=1; i< nbins+1 ; i++) {
        binedges[i]=from*TMath::Power(step,i);
    }
}

LinScale::LinScale(int m_nbins, double from, double to):ScaleObj(m_nbins)
{
    if(to<=from) {
        std::cerr<<"A scale must go over a positive interval"<<std::endl;
    }
    if(nbins<1) {
        std::cerr<<"A scale must have at least one bin"<<std::endl;
    }

    double interval = to-from;

    double step=interval/nbins;

    binedges[0]=from;
    for(int i=1; i< nbins+1 ; i++) {
        binedges[i]=from + step*i;
    }
}

CountScale::CountScale(int m_from, int m_to = 0):ScaleObj(TMath::Abs(m_to-m_from) + 1)
{
    // This function does what it should, trust me. /Simon
    int from = TMath::Min(m_from, m_to);

    binedges[0]= from - 0.5;
    for(int i=1; i< nbins+1 ; i++) {
        binedges[i] = from + i - 0.5;
    }
}
