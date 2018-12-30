#include "common.h"
#include "base.h"
#include "sla.h"
#include "funk.h"
#include "mesh.h"

static int lcal(int, int, int);


double matcons(int paar1, int paar2)

{
            
    int j1, j2, j3, j4;
    int l1, l2, l3, l4; 
    int l1s, l2s, l3s, l4s;
    int st1, st2, st3, st4;
    int t1, t2, t3, t4;    
    int bi1, bi2, bi3, bi4;
    double matsum;   
    double matasum_ome_spat, matasum_rho_spat, matasum_coul_spat;    
    int coul;
    
    
    matsum = zero;

    matasum_ome_spat = matasum_rho_spat = matasum_coul_spat = zero;
    
    
    

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


    // Coulomb-Force ?
    if ((t1 == 2) && (t1 == t2))
      coul = 1;
    else
      coul = 0;

    // pions and
    // current-parts of matrixelements
      
    //F1F2G3G4

    bi1 = 1;
    bi2 = 1;
    bi3 = 2;
    bi4 = 2;


    l1 = lcal(l1s,j1,bi1);
    l2 = lcal(l2s,j2,bi2);
    l3 = lcal(l3s,j3,bi3);
    l4 = lcal(l4s,j4,bi4);


    // s = 1, t = 0

    matasum_ome_spat += +one/(4*pi)*
      vphcomp(j,1,0,st1,l1,j1,t1,st2,l2,j2,t2,
	      st3,l3,j3,t3,st4,l4,j4,t4,
	      bi1,bi2,bi3,bi4,2,7);

    if (coul == 1)
      matasum_coul_spat += +gcoul*
	vphcomp(j,1,0,st1,l1,j1,t1,st2,l2,j2,t2,
		st3,l3,j3,t3,st4,l4,j4,t4,
		bi1,bi2,bi3,bi4,4,1);
    

    // s = 1, t = 1

    matasum_rho_spat += +one/(4*pi)*
      vphcomp(j,1,1,st1,l1,j1,t1,st2,l2,j2,t2,
	      st3,l3,j3,t3,st4,l4,j4,t4,
	      bi1,bi2,bi3,bi4,3,8);



		
			
    // F1G2G3F4
    
    bi1 = 1;
    bi2 = 2;
    bi3 = 2;
    bi4 = 1;


    l1 = lcal(l1s,j1,bi1);
    l2 = lcal(l2s,j2,bi2);
    l3 = lcal(l3s,j3,bi3);
    l4 = lcal(l4s,j4,bi4);

 
    // s = 1, t = 0

    matasum_ome_spat += -one/(4*pi)*
      vphcomp(j,1,0,st1,l1,j1,t1,st2,l2,j2,t2,
	      st3,l3,j3,t3,st4,l4,j4,t4,
	      bi1,bi2,bi3,bi4,2,7);

    if (coul == 1)
      matasum_coul_spat += -gcoul*
	vphcomp(j,1,0,st1,l1,j1,t1,st2,l2,j2,t2,
		st3,l3,j3,t3,st4,l4,j4,t4,
		bi1,bi2,bi3,bi4,4,1);


    // s = 1, t = 1

    matasum_rho_spat += -one/(4*pi)*
      vphcomp(j,1,1,st1,l1,j1,t1,st2,l2,j2,t2,
	      st3,l3,j3,t3,st4,l4,j4,t4,
	      bi1,bi2,bi3,bi4,3,8);


  

			    
    // G1F2F3G4

    bi1 = 2;
    bi2 = 1;
    bi3 = 1;
    bi4 = 2;
	
    l1 = lcal(l1s,j1,bi1);
    l2 = lcal(l2s,j2,bi2);
    l3 = lcal(l3s,j3,bi3);
    l4 = lcal(l4s,j4,bi4);


    // s = 1, t = 0

    matasum_ome_spat += -one/(4*pi)*
      vphcomp(j,1,0,st1,l1,j1,t1,st2,l2,j2,t2,
	      st3,l3,j3,t3,st4,l4,j4,t4,
	      bi1,bi2,bi3,bi4,2,7);

    if (coul == 1)
      matasum_coul_spat += -gcoul*
	vphcomp(j,1,0,st1,l1,j1,t1,st2,l2,j2,t2,
		st3,l3,j3,t3,st4,l4,j4,t4,
		bi1,bi2,bi3,bi4,4,1);


    
    // s = 1, t = 1

    matasum_rho_spat += -one/(4*pi)*
      vphcomp(j,1,1,st1,l1,j1,t1,st2,l2,j2,t2,
	      st3,l3,j3,t3,st4,l4,j4,t4,
	      bi1,bi2,bi3,bi4,3,8);


    
    // G1G2F3G4

    
    bi1 = 2;
    bi2 = 2;
    bi3 = 1;
    bi4 = 1;

    l1 = lcal(l1s,j1,bi1);
    l2 = lcal(l2s,j2,bi2);
    l3 = lcal(l3s,j3,bi3);
    l4 = lcal(l4s,j4,bi4);

	
    // s = 1, t = 0

    matasum_ome_spat += +one/(4*pi)*
      vphcomp(j,1,0,st1,l1,j1,t1,st2,l2,j2,t2,
	      st3,l3,j3,t3,st4,l4,j4,t4,
	      bi1,bi2,bi3,bi4,2,7);

    if (coul == 1)
      matasum_coul_spat += +gcoul*
	vphcomp(j,1,0,st1,l1,j1,t1,st2,l2,j2,t2,
		st3,l3,j3,t3,st4,l4,j4,t4,
		bi1,bi2,bi3,bi4,4,1);


    // s = 1, t = 1

    matasum_rho_spat += +one/(4*pi)*
      vphcomp(j,1,1,st1,l1,j1,t1,st2,l2,j2,t2,
	      st3,l3,j3,t3,st4,l4,j4,t4,
	      bi1,bi2,bi3,bi4,3,8);

 
    


    matsum = matasum_ome_spat + matasum_rho_spat + matasum_coul_spat;
	


    return matsum;
    


    
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

    	
    
