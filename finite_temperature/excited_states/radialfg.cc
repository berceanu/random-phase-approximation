#include "common.h"
#include "sla.h"
#include "base.h"
#include "funk.h"
#include "mesh.h"


static double gaussrfgunten(double *, int);

static double gaussrfgoben(double *, int);


double radialfg(int st1, int l1, int t1, int st2, int l2, int t2, 
		int st3, int l3, int t3, int st4, int l4, int t4, int ll, 
		int bi1, int bi2, int bi3, int bi4, int mpar, int rpar)


{

    double radialfgret = zero;
    double part2 = zero;
    int k1, k2;
    double xmesh;
    double radint1,radint2;
    double rad1,rad2;
    int iso1,iso2;
    
    if (t1==1)
       iso1=-1;
    else
       iso1=1;
    if (t2==1)
       iso2=-1;
    else
       iso2=1; 

    radf1i[0] = zero;
    radf1e[0] = zero;
    radf2i[0] = zero;
    radf2e[0] = zero;

    if (mpar == 4) 
    {
	for (k1 = 1; k1 <= nmixmesh; k1++) {

	    radf1i[k1] = wfgauss[st1][k1+(bi1-1)*nmixmesh][t1]
	      *wfgauss[st3][k1+(bi3-1)*nmixmesh][t3]*
		pow(rmesh[k1],double(ll+2));
	    radf1e[k1] = wfgauss[st1][k1+(bi1-1)*nmixmesh][t1]
	      *wfgauss[st3][k1+(bi3-1)*nmixmesh][t3]*
		pow(rmesh[k1],double(-ll+1));
	    radf2i[k1] = wfgauss[st2][k1+(bi2-1)*nmixmesh][t2]
	      *wfgauss[st4][k1+(bi4-1)*nmixmesh][t4]*
		pow(rmesh[k1],double(ll+2))/(2*ll+1);
	    radf2e[k1] = wfgauss[st2][k1+(bi2-1)*nmixmesh][t2]
	      *wfgauss[st4][k1+(bi4-1)*nmixmesh][t4]*
		pow(rmesh[k1],double(-ll+1))/(2*ll+1);
	}
    }
    
    else 
    {
	    

	for (k1 = 1; k1 <= nmixmesh; k1++)
	{
        switch(rpar)
	{
	    case 1:
	       rad1 = -coupl[mpar][k1]-dcoupl[mpar][k1]*dens[mpar][k1];
	       rad2 = coupl[mpar][k1]+dcoupl[mpar][k1]*dens[mpar][k1];
	       break;
	    case 2:  
	       rad1 = coupl[mpar][k1]+dcoupl[mpar][k1]*dens[mpar][k1];
	       rad2 =  coupl[mpar][k1]-dcoupl[mpar][k1]*dens[mpar][k1];
	       break;  
	    case 3:  
	       rad1 = coupl[mpar][k1]-dcoupl[mpar][k1]*dens[mpar][k1];
	       rad2 = coupl[mpar][k1]+dcoupl[mpar][k1]*dens[mpar][k1];
	       break;
	    case 4:  
	       rad1 = -coupl[mpar][k1]+dcoupl[mpar][k1]*dens[mpar][k1];
	       rad2 = coupl[mpar][k1]-dcoupl[mpar][k1]*dens[mpar][k1];
	       break;
	    case 5:  
	       rad1 = coupl[mpar][k1]+dcoupl[mpar][k1]*dens[mpar][k1];
	       rad2 = coupl[mpar][k1]+dcoupl[mpar][k1]*dens[mpar][k1];
	       break;
	    case 6:  
	       rad1 = iso1*coupl[mpar][k1]+dcoupl[mpar][k1]*dens[mpar][k1];
	       rad2 = iso2*coupl[mpar][k1]+dcoupl[mpar][k1]*dens[mpar][k1];
	       break;
	    case 7:  
	       rad1 = coupl[mpar][k1];
	       rad2 = coupl[mpar][k1];
	       break;
	    case 8:  
	       rad1 = iso1*coupl[mpar][k1];
	       rad2 = iso2*coupl[mpar][k1];
	       break;	       	       	       	       	       	       
	    default:
	    cout << "Error in rpar\n";
	    exit(1);
	}	       
	    radf1i[k1] = wfgauss[st1][k1+(bi1-1)*nmixmesh][t1]
	      *wfgauss[st3][k1+(bi3-1)*nmixmesh][t3]*
		fxi[k1][ll][mpar]*rmesh[k1]*rad1;
	    radf1e[k1] = wfgauss[st1][k1+(bi1-1)*nmixmesh][t1]
	      *wfgauss[st3][k1+(bi3-1)*nmixmesh][t3]*
		fxe[k1][ll][mpar]*rmesh[k1]*rad1;
	    radf2i[k1] = wfgauss[st2][k1+(bi2-1)*nmixmesh][t2]
	      *wfgauss[st4][k1+(bi4-1)*nmixmesh][t4]*
		fxi[k1][ll][mpar]*rmesh[k1]*rad2/(-wro[ll][mpar]);
	    radf2e[k1] = wfgauss[st2][k1+(bi2-1)*nmixmesh][t2]
	      *wfgauss[st4][k1+(bi4-1)*nmixmesh][t4]*
		fxe[k1][ll][mpar]*rmesh[k1]*rad2/(-wro[ll][mpar]);
	}
    }
    
    radint1 = zero; 
    radint2 = zero;    

    for (k1 = 1; k1 < nfe; k1++) 
    {	

	
	radint1 += (radf1e[mapex[k1]]*gaussrfgunten(radf2i,k1)
		   +radf1i[mapex[k1]]*gaussrfgoben(radf2e,k1))
	  *wlex[k1]; 


    }	
    if ((mpar != 4) && (rpar != 7) && (rpar != 8))
    {
       for(k1 = 1; k1 <= nmixmesh; k1++)
       {
          switch(rpar)
          {
            case 1:
	       rad1 = -2.0*rmesh[k1]*dcoupl[mpar][k1]
	              -rmesh[k1]*ddcoupl[mpar][k1]*dens[mpar][k1];
	       rad2 = rmesh[k1]*coupl[mpar][k1]*dens[mpar][k1];
	       break;
	    case 2:
	       rad1 = -rmesh[k1]*ddcoupl[mpar][k1]*dens[mpar][k1];
	       rad2 = rmesh[k1]*coupl[mpar][k1]*dens[mpar][k1];
	       break;
	    case 3:
	       rad1 = -rmesh[k1]*ddcoupl[mpar][k1]*dens[mpar][k1];
	       rad2 = rmesh[k1]*coupl[mpar][k1]*dens[mpar][k1];
	       break;
	    case 4:
	       rad1 = 2.0*rmesh[k1]*dcoupl[mpar][k1]
	              -rmesh[k1]*ddcoupl[mpar][k1]*dens[mpar][k1];
	       rad2 = rmesh[k1]*coupl[mpar][k1]*dens[mpar][k1];
	       break;	       	       	       
            case 5:
	       rad1 = 2.0*rmesh[k1]*dcoupl[mpar][k1]+
	              rmesh[k1]*ddcoupl[mpar][k1]*dens[mpar][k1];
	       rad2 = rmesh[k1]*coupl[mpar][k1]*dens[mpar][k1];
	       break;
	    case 6:
	       rad1 = rmesh[k1]*dcoupl[mpar][k1]*(iso1+iso2)+
	              rmesh[k1]*ddcoupl[mpar][k1]*dens[mpar][k1];
	       rad2 = rmesh[k1]*coupl[mpar][k1]*dens[mpar][k1];
	       break;
	    default:
	    cout << "Error in rpar\n";
	    exit(1);	       
	  }
	  radf1i[k1] = wfgauss[st1][k1+(bi1-1)*nmixmesh][t1]
	              *wfgauss[st3][k1+(bi3-1)*nmixmesh][t3]
	              *wfgauss[st2][k1+(bi2-1)*nmixmesh][t2]
		      *wfgauss[st4][k1+(bi4-1)*nmixmesh][t4] 
		      *fxi[k1][0][mpar]*rad1;
	  radf1e[k1] = wfgauss[st1][k1+(bi1-1)*nmixmesh][t1]
	              *wfgauss[st3][k1+(bi3-1)*nmixmesh][t3]
	              *wfgauss[st2][k1+(bi2-1)*nmixmesh][t2]
		      *wfgauss[st4][k1+(bi4-1)*nmixmesh][t4] 
		      *fxe[k1][0][mpar]*rad1;
	  radf2i[k1] = fxi[k1][0][mpar]*rad2/(-wro[0][mpar]);
	  radf2e[k1] = fxe[k1][0][mpar]*rad2/(-wro[0][mpar]);
       }	
       for (k1 = 1; k1 < nfe; k1++) 
       {		
	  radint2 += (radf1e[mapex[k1]]*gaussrfgunten(radf2i,k1)
		   +radf1i[mapex[k1]]*gaussrfgoben(radf2e,k1))
	  *wlex[k1]; 
       }
    }   
    radialfgret = radint1+radint2;	  	                 	    
    return radialfgret;

}


static double gaussrfgunten(double *radfun, int ista) 

{
    int i, l;
    double gausumunten = zero;
    


    for (i = 1; i <= ista; i++) 
    {
	
	for (l = 1; l <= point[i]; l++) 
	{
	    gausumunten += radfun[mapin[i][l]]*wlin[i][l];
	}
	
    }

    
    return gausumunten;
    

}


static double gaussrfgoben(double *radfun, int ista) 


{
    int i, l;
    double gausumoben = zero;
    


    for (i = ista+1; i <= nfe; i++) 
    {
	
	for (l = 1; l <= point[i]; l++) 
	{
	    gausumoben += radfun[mapin[i][l]]*wlin[i][l];
	}
	
    }

    
    return gausumoben;
    

}

   
