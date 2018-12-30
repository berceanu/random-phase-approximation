#include "common.h"
#include "base.h"
#include "sla.h"
#include "funk.h"
#include "mesh.h"


#define NRANSI
#define float double
#include "nr.h"
#include "nrutil.h"



float dxsav,*xp,**yp;  /* defining declarations */
int kmax,kount;

int nrhs;   /* counts function evaluations */

static int l;

int gloma;




// ODE-System
void derivs(float x,float y[],float dydx[])
{
    nrhs++;
    dydx[1] = y[2];
    dydx[2] = (l*(l+1)/(x*x)+meffsqx(x,gloma))*y[1];
       
}





void intdif()
{
    

//
//     This subroutine solves the Schr"odinger equation for 
//     Potential V(r) = meff(r)*meff(r) 
// 
//
//     ( - d/dx d/dx +  L(L+1)/ x*x + V(x)) F(x) = 0
//
//         d/dx F(x) = D(x) 
//         d/dx D(x) = F(x) * ( L(L+1)/x*x + VV(x))  
//
//    
//     analytic solutions are used to start the inward and 
//     a fourth-order Runge-Kutta algorithm is used to integrate 
//     the coupled differential equations.
//
//


  double halfmesh, anorm;
  long double fx1, dx1, fk1, dk1, fk2, dk2, fk3, dk3, fk4, dk4;
  double wr1;
  int i;
  int n;
  double meff;
  double xstart, xend;
  double coeffp, coeffn;
  double coeffpd, coeffnd;
  double xmesh, xmeshe;
  double coeff2;
  double wroerrmax;
  double wrodiff;
  double wrocomp;

  
  // variables from Numerical Recipes Routines
  int nbad,nok;
  float eps=1.0e-16, h1=0.001,hmin=0.0, *ystart;
  
  ystart=vector(1,2);
  nrhs=0;

// no steps are stored: kmax = 0 is required!!
  kmax=0;
  dxsav=h1;


  anorm = one;



    
  for (gloma = 1; gloma <= nmass; gloma++)
  {
      


      for (l = 0; l <= lmax; l++)
      {
      
	  	  

	  // Integrate fxi from istart to nmixmesh-1
	  for (i = istart; i <= iende-1; i++)
	  {
	      xmesh = rmesh[i];
	      xmeshe = rmesh[i+1];
	  
	      
	      ystart[1] = fxi[i][l][gloma];
	      ystart[2] = dxi[i][l][gloma];
	  
	      odeint(ystart,2,xmesh,xmeshe,eps,h1,hmin,&nok,&nbad,derivs,rkqs);
	  
	  	  

	      fxi[i+1][l][gloma] = ystart[1];
	      dxi[i+1][l][gloma] = ystart[2];

	      

	  }

	 
	      
  
	  // Integrate inward from iende to istart
      
	  for (i = iende; i >= istart+1; i--)
	  {
	    
	      

	      xmesh = rmesh[i];
	      xmeshe = rmesh[i-1];
	  
	      
	      ystart[1] = fxe[i][l][gloma];
	      ystart[2] = dxe[i][l][gloma];


	      odeint(ystart,2,xmesh,xmeshe,eps,h1,hmin,&nok,&nbad,derivs,rkqs);
	  

	      fxe[i-1][l][gloma] = ystart[1];
	      dxe[i-1][l][gloma] = ystart[2];

	  }
      
	  
// Wronskian


	  wroerrmax = zero;
      
      

	  for (i = istart; i <= iende; i++)
	  {      
	      wro[l][gloma] = (dxe[i][l][gloma]*fxi[i][l][gloma]
			       -dxi[i][l][gloma]*fxe[i][l][gloma]);

	    
	      
	      if (i == istart)
		wrocomp = wro[l][gloma];
	  
	      wrodiff = abs0(wro[l][gloma]-wrocomp);
	      if (wrodiff > wroerrmax) {	      
		  wroerrmax = wrodiff;	
//		  cout << "groesser Fehler bei i = " << i << endl;
//		  cout << "wrodiff = " << wrodiff << endl;
	      }
	      
	      
    	  

	  }
      
	  wroerr[l][gloma] = wroerrmax;
	  cout << "maximaler Fehler in Wronskian fuer l = " << l << 
	    " und Masse " << gloma << " ist "
	      << wroerr[l][gloma] << endl;
      



      }
  
      
  }
  
  


  // free memory

  double3del(dxi);
  double3del(dxe);
  double2del(wroerr);

}







