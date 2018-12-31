#include "common.h"
#include "base.h"
#include "sla.h"
#include "funk.h"
#include "mesh.h"
#include "edmonds.h"

static int lcal(int, int, int);


double qpmataph(int paar1, int paar2,double v0,double vs)

{
    
            
    int j1, j2, j3, j4;
    int l1, l2, l3, l4; 
    int l1s, l2s, l3s, l4s;
    int st1, st2, st3, st4;
    int t1, t2, t3, t4;    
    int bi1, bi2, bi3, bi4;
    int ih1,ih2,ih3,ih4;
    int ib1,ib2,ib3,ib4;    
    int coul;
    double qpmataph, fac0, fac1, fac2; 
    int jmin,mk;
    double sum3j,rmk;   

    st1 = iph[paar1][1];
    st2 = iph[paar2][2];
    st3 = iph[paar1][2];
    st4 = iph[paar2][1];

    t1 = t3 = iph[paar1][3];
    t2 = t4 = iph[paar2][3];
       
    l1s = nl[st1][t1];
    l2s = nl[st2][t2];
    l3s = nl[st3][t3];
    l4s = nl[st4][t4];

    j1 = nj[st1][t1];
    j2 = nj[st2][t2];
    j3 = nj[st3][t3];
    j4 = nj[st4][t4];


   
    fac0 = 1.0/sqrt(double( (1+deltafunk(st1,st3))*(1+deltafunk(st2,st4)) ) );   

    fac1 = ((uo[st1][t1]*vo[st3][t3]*uo[st4][t4]*vo[st2][t2]) +
		(vo[st1][t1]*uo[st3][t3]*vo[st4][t4]*uo[st2][t2]));
    fac2 = ((uo[st1][t1]*vo[st3][t3]*uo[st2][t2]*vo[st4][t4]) +
		(vo[st1][t1]*uo[st3][t3]*vo[st2][t2]*uo[st4][t4]));
		
    qpmataph = (v0+vs)*fac0*fac1 +(v0*iv[j]+vs*iv[j+1])*fac0*fac2;      	      
    //if (paar1 == paar2) // to include only diagonal term
    {
     //qpmataph += eeqp[st1][t1] + eeqp[st3][t3];
        ih1 = indinbl[st1][t1];
	ib1 = iblock[st1][t1];
        ih2 = indinbl[st3][t3];
        ib2 = iblock[st3][t3];
        ih3 = indinbl[st4][t4];
	ib3 = iblock[st4][t4];
	ih4 = indinbl[st2][t2];
	ib4 = iblock[st2][t2];
			       
	qpmataph+= deltafunk(st3,st2)*deltafunk(ib1,ib3)
			       *(h11[ih1][ih3][ib1])*fac0;
        qpmataph-= deltafunk(st1,st2)*deltafunk(ib2,ib3)
             	        *iv[abs0(j1+j3-1+j)]*h11[ih2][ih3][ib2]*fac0;
        qpmataph-= deltafunk(st3,st4)*deltafunk(ib1,ib4)
             		*iv[abs0(j1+j3-1+j)]*h11[ih1][ih4][ib1]*fac0; 
        qpmataph+= deltafunk(st1,st4)*deltafunk(ib2,ib4)
			       *(h11[ih2][ih4][ib2])*fac0; 			                     
    }	  
    return qpmataph;
    


    
}



static int lcal(int lc, int jc, int bil)
{
    

    if (bil == 1)
      return lc;
    
    else 
    {
	if (lc < jc)
	  return jc;
	else
	  return (lc-1);
    }
}
