#include "common.h"
#include "base.h"
#include "sla.h"
#include "funk.h"
#include "mesh.h"

#define float double
#define NRANSI
#include "nr.h"
#include "nrutil.h"



double3(fxi);
double3(fxe); 
double3(dxi);
double3(dxe);
double2(wro);
double2(wroerr);
int istart;
int iende;


void potdif()
{

    
    int i, l, nm, ix;
    int na1, na2;
    double meff;
    double xmesh;
    double pifakt, pifaktd;
    double fxinumr;
    double dxinumr;
    double fxenumr;
    double dxenumr;
    double wrocomp,wrodiff;
    double wroerrmax = 0;


    // allocation of arrays

    double3init(fxi,nmixmesh,lmax,nmass);
    double3init(fxe,nmixmesh,lmax,nmass); 
    double3init(dxi,nmixmesh,lmax,nmass);
    double3init(dxe,nmixmesh,lmax,nmass);
    double2init(wro,lmax,nmass);
    double2init(wroerr,lmax,nmass);
        


    for (nm = 1; nm <= nmass; nm++)
    {
	
	meff = rmass[nm];	

	for (l = 0; l <= lmax; l++)
	{
            for (ix = 1; ix <= nmixmesh; ix++)
            {
                xmesh = meff*rmesh[ix];
                pifakt = sqrt(pi*xmesh/2.);
	        pifaktd = sqrt(pi/(2.*xmesh))/2.;    	    
	        bessik(xmesh,(l+half),&fxinumr,&fxenumr,
		   &dxinumr,&dxenumr);	
	        fxi[ix][l][nm] = pifakt*fxinumr;
	        dxi[ix][l][nm] = meff*(pifaktd*fxinumr+pifakt*dxinumr);
	        fxe[ix][l][nm] = pifakt*fxenumr;
	        dxe[ix][l][nm] = meff*(pifaktd*fxenumr+pifakt*dxenumr);    
                wro[l][nm] = (dxe[ix][l][nm]*fxi[ix][l][nm]
			      - dxi[ix][l][nm]*fxe[ix][l][nm]);
                if(ix == 1) wrocomp = wro[l][nm];
                wrodiff = abs0(wro[l][nm]-wrocomp);
                if (wrodiff > wroerrmax) wroerrmax = wrodiff;	    
	    }
            wroerr[l][nm] = wroerrmax;
            cout << "Maximal error in wronskian for l = " << l << 
		" and mass = " << nm << " is " << wroerr[l][nm] << endl; 
        }
    }
}









