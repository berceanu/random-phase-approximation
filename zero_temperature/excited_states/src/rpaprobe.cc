#include "common.h"
#include "base.h"
#include "funk.h"
#include "sla.h"


void rpaprobe(int n, double **aa, double **bb, double **xx,
	    double **yy, double *e) {


    //    macht Check nach Loesen der RPA-Gleichungen


    int i, j, k, l;
    
    double colsum;
    double col_err;
    double col_err_max;    
    double uperrormax, downerrormax;
    double uperror, downerror;
    double xysum;
    double xyerrormax = zero;
    double xyerror_cor;
    

    double2(rpa_full);
    double1(rpa_res);
    int istart;
    

    ndim_o_r = n;
    
    ndim_o_c = 2*n;
    
    istart = 1;

          
    double2init(rpa_full,2*ndim_o_r,2*ndim_o_r);
    double1init(rpa_res,2*ndim_o_r);
  

    // normalization of xy-eigenvectors 

    xyerrormax = zero;

    
    for (i = istart; i <= ndim_o_c; i++) 
    {    
	xysum = zero;
	
	for (k = 1; k <= ndim_o_r; k++)
	  xysum += xx[k][i]*xx[k][i] - yy[k][i]*yy[k][i];
	    
	xyerror_cor = sqrt(1./abs0(xysum)); 		    

	for (k = 1; k <= ndim_o_r; k++)
	{
	    xx[k][i] *= xyerror_cor;
	    yy[k][i] *= xyerror_cor;
	}
    }
    

    for (i = 1; i <= ndim_o_r; i++) 
    {
	for (j = 1; j <= ndim_o_r; j++)
	{
	    rpa_full[i][j] = aa[i][j];
	    rpa_full[i+ndim_o_r][j] = -bb[i][j];
	    rpa_full[i][j+ndim_o_r] = bb[i][j];
	    rpa_full[i+ndim_o_r][j+ndim_o_r] = -aa[i][j];
	}
    }
    


    col_err_max = zero;

    for (i = istart; i <= ndim_o_c; i++)
    {

	if (c_erpa[i] == zero)
	{
	    

	    for (j = 1; j <= 2*ndim_o_r; j++)
	    {
		colsum = zero;
	    
		for (k = 1; k <= ndim_o_r; k++) 
		{			
		    colsum += rpa_full[j][k]*xx[k][i]
		      +rpa_full[j][k+ndim_o_r]*yy[k][i];
		}
	    
	   
		if (j <= ndim_o_r)
		  colsum -= e[i]*xx[j][i];
		else
		  colsum -= e[i]*yy[j-ndim_o_r][i];
	    
		rpa_res[j] = colsum; 
	    

	    }
	
	    col_err = zero;

	    for (l = 1; l <= ndim_o_c; l++)
	      col_err += rpa_res[l]*rpa_res[l];
	    col_err = sqrt(col_err);

	    if (col_err > col_err_max)
	      col_err_max = col_err;
	}
	
    }
        
    

    cout << "maximal RPA-error: " << col_err_max << endl;

    

    //check for normalization

    xyerrormax = zero;
  
    for (i = istart; i <= ndim_o_c; i++) 
    {
	if (c_erpa[i] == zero)
	{ 

	
	    for (j = istart; j <= ndim_o_c; j++)
	    {
		if (c_erpa[j] == zero)
		{
		    
	    
		    xysum = zero;
	    
		    for (k = 1; k <= ndim_o_r; k++)
		      xysum += xx[k][i]*xx[k][j] - yy[k][i]*yy[k][j];
	    
		    if (i == j) 
		    {
		
			if (abs0(1-abs0(xysum)) > xyerrormax)     
			  xyerrormax = abs0(1-abs0(xysum)) ;
			
		    }
		    else 
		    {		
			if (abs0(xysum) > xyerrormax)	    
			  xyerrormax = abs0(xysum);
			   
		
		    }
		}
		
	    }
	}
	
    }
    

    cout << "maximal XY-norm-error with correction: " << xyerrormax << endl;


  
    return;
}


