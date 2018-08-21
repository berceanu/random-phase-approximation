#include "common.h"
#include "base.h"
#include "sla.h"
#include "funk.h"
#include "edmonds.h"
#include "mesh.h"


static double Yred(int, int , int, int, int);

double elred(int st1, int l1, int j1, int t1, int b1,
	     int st2, int l2, int j2, int t2, int b2, int l) 
{
    
    double elredret = zero;
    double testrad = zero;
    

    



    elredret = (1.+iv[abs0(l1+l2+l)])/2.*sinrad(st1,l1,t1,b1,
						st2,l2,t2,b2,l)*
      sqrt((2*l+1)*(2*j1)*(2*j2)/(4*pi))*iv[j1-1]
	*wigner((j1-half),double(l),j2-half,-half,0.,half);

 
   

    return elredret;
    

}



double magred(int st1, int l1, int j1, int t1, int b1,
	      int st2, int l2, int j2, int t2, int b2, int l) 
{ 

    
    const double gprot = 5.586;
    const double gneut = -3.826;
    
    int k;    
    double gs, gl;        
    double magredret = zero;
    
    
    switch(t1) 
    {
      case 1:
	
	gs = gneut;
	gl = zero;
	

	break;
	

      case 2:
	
	gs = gprot;
	gl = 1.;
	
	break;
	

      default:
	
	cout << "wrong value for isospin in magred()!" << endl;
	cout << "Execution will be terminated!" << endl;
	exit(1);
    }
    

    k = j2*iv[l2+j2]+j1*iv[l1+j1];
    


    magredret = (1.-iv[abs0(l1+l2+l)])/2.*sinrad(st1,l1,t1,b1,
						 st2,l2,t2,b2,(l-1))
      *sqrt((2*l+1)*(2*j1)*(2*j2)/(4*pi))*iv[j1-1]
	*wigner((j1-half),double(l),(j2-half),-half,0.,half)
	  *(l-k)*(half*gs-gl*(1+k/(l+1)));
    

    
    return magredret;
    


}


double monred(int st1, int l1, int j1, int t1, int b1,
	      int st2, int l2, int j2, int t2, int b2) 
{
    
    double monredret = zero;
    
      monredret = sqrt(2.*j1)*
      deltafunk(l1,l2)*deltafunk(j1,j2)
	*sinrad(st1,l1,t1,b1,st2,l2,t2,b2,2);
    return monredret;
}


double dipskalred1(int st1, int l1, int j1, int t1, int b1,
	       int st2, int l2, int j2, int t2, int b2) 
{
    
    double dipskalred_ret = zero;

    double r3_part;
    double r1_part;

  /*  
    r3_part = (1.+iv[abs0(l1+l2+1)])/2.*sinrad(st1,l1,t1,b1,
						st2,l2,t2,b2,3)
      *sqrt((2*1.+1)*(2*j1)*(2*j2)/(4*pi))*iv[j1-1]
	*wigner((j1-half),double(1),j2-half,-half,0.,half);

    r1_part = (1.+iv[abs0(l1+l2+1)])/2.*sinrad(st1,l1,t1,b1,
						st2,l2,t2,b2,1)
      *sqrt((2*1.+1)*(2*j1)*(2*j2)/(4*pi))*iv[j1-1]
	*wigner((j1-half),double(1),j2-half,-half,0.,half);
   */
     
    r3_part = sinrad(st1,l1,t1,b1,st2,l2,t2,b2,3)*
              Yred(l1,j1,l2,j2,j);

    r1_part = sinrad(st1,l1,t1,b1,st2,l2,t2,b2,1)*
              Yred(l1,j1,l2,j2,j);



    //  dipskalred_ret = r3_part;
      dipskalred_ret = r3_part - (5./3.)*rms_2*r1_part;
      

    return dipskalred_ret;
    
}

// EXCITATION WITH THE TOROIDAL OPERATOR

double diptoroidred(int st1, int l1, int j1, int t1, int b1,
	       int st2, int l2, int j2, int t2, int b2) 
{
     
    double diptoroidred_ret = zero;

    double red_fac; 
    double red_Y_lamda_0,red_Y_lamda_2;
    double red_9j_lamda_0,red_9j_lamda_2;
    double part_lamda_0, part_lamda_2, part_cm;
            
    red_fac = -1.0*sqrt(pi)*sqrt(6.0);
    
    red_Y_lamda_0 = (1.0/sqrt(4*pi))*iv[abs0(l1)]*sqrt(2*l1+1)
                    *sqrt(2*l2+1)*wigner(l1,0,l2,0,0,0);
     
    red_9j_lamda_0 = sqrt(2*j1)*sqrt(2*j2)*sqrt(3.0)
                     *s9jslj(1,l1,l2,0,j1,j2,1);

    red_Y_lamda_2 = (1.0/sqrt(4*pi))*iv[abs0(l1)]*sqrt(2*l1+1)
                    *sqrt(2*2+1)*sqrt(2*l2+1)*wigner(l1,2,l2,0,0,0);
    
    red_9j_lamda_2 = sqrt(2*j1)*sqrt(2*j2)*sqrt(3.0)
                     *s9jslj(1,l1,l2,2,j1,j2,1);
    
    part_lamda_0 = red_fac*red_Y_lamda_0*red_9j_lamda_0
                   *sinrad(st1,l1,t1,b1,st2,l2,t2,b2,2);
    
    part_cm = 1.0*red_fac*red_Y_lamda_0*red_9j_lamda_0
                   *sinrad(st1,l1,t1,b1,st2,l2,t2,b2,0);

/*      part_cm = (1.+iv[abs0(l1+l2+1)])/2.*sinrad(st1,l1,t1,b1,
						st2,l2,t2,b2,1)
      *sqrt((2*1.+1)*(2*j1)*(2*j2)/(4*pi))*iv[j1-1]
	*wigner((j1-half),double(1),j2-half,-half,0.,half);  */
    
    part_lamda_2 = red_fac*(sqrt(2.0)/5.0)*red_Y_lamda_2*red_9j_lamda_2
                   *sinrad(st1,l1,t1,b1,st2,l2,t2,b2,2);  			 
    diptoroidred_ret = part_lamda_0 + part_lamda_2  - rms_2*part_cm;
           
    return diptoroidred_ret;
    
}

       

double sinrad(int st1, int l1, int t1, int b1,
	      int st2, int l2, int t2, int b2, int l) 

{
    
    double radproint;
    double sinradret = zero;
    double r;

//    if ((l > (l1+l2)) ||(l < abs0(l1-l2))) 
//      return sinradret;
    

    
    int i, k, index;
    
    radproint = zero;
    
    for (i = 1; i <= nfe; i++)
    {
	for (k = 1; k <= point[i]; k++)
	{	
	    index = mapin[i][k];
		    	    
	    radproint += wfgauss[st1][index+(b1-1)*nmixmesh][t1]
	      *wfgauss[st2][index+(b2-1)*nmixmesh][t2]
		*pow(rmeshin[i][k],double(l))
		  *rmeshin[i][k]*rmeshin[i][k]*wlin[i][k];
	}
	
    }

    
    
    sinradret = radproint;
    
    return sinradret;
    

}
static double Yred(int l1, int j1, int l2, int j2, int j) 
{

    double yred_ret=0.0;
    
    if ((j > (l1+l2)) ||(j < abs0(l1-l2))) 
      return yred_ret;
          
    yred_ret = (1.+iv[abs0(l1+l2+j)])/2.*
      sqrt((2*j+1)*(2*j1)*(2*j2)/(4*pi))*iv[j1-1]
	*wigner((j1-half),double(j),j2-half,-half,0.,half);
    return yred_ret;
}    



    










