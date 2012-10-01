#ifndef SCALEOBJ_H_ESBV4CA0
#define SCALEOBJ_H_ESBV4CA0

/*

    The Scale objects can be used to set ROOT histogram scales.
    They can be implicitly cast to int and double*, giving
    the number of bins and a bin-edge array respectively.

    Examples of use might be:
    LogScale ptscale(100,10,1000); //make 100 logarithmic bins spanning the range [10,1000)
    h=TH1D("h","h",ptscale,ptscale);

    The possible ScaleObjects are:
    LogScale(nbins, from, to):   makes logarithmic bins over the range.
    LinScale(nbins, from, to):   makes linear bins over the range (somewhat unnecessary since it duplicates ROOT's funcionality.)
    CountScale(N): makes integer sized bins centered on the integer values from 0 up to and including N.
    CountScale(N1,N2): makes integer sized bins centered on the integer values on the range N1 to N2, both included.


*/

#include <vector>
// #include <set>

class ScaleObj
{
public:
    ScaleObj (size_t size):nbins(size),binedges(size+1,0) {};
    virtual ~ScaleObj () {};

    virtual operator const int() {
        return nbins;
    }
    virtual operator const double*() {
        return &binedges[0];
    }
    int nbins;
    std::vector<double> binedges;
};

class LogScale: public ScaleObj
{
public:
    LogScale (int nbins, double from, double to);
    // ~LogScale() {}
};

class LinScale: public ScaleObj
{
public:
    LinScale (int nbins, double from, double to);
    // ~LinScale() {}
};

class CountScale: public ScaleObj
{
public:
    CountScale (int from, int to);
    // ~CountScale() {}
};


#endif /* end of include guard: SCALEOBJ_H_ESBV4CA0 */
