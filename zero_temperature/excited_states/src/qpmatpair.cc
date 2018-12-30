#include "common.h" 
#include "base.h"
#include "sla.h"
#include "funk.h"
#include "mesh.h"
#include "edmonds.h"

static int lcal(int, int, int);


double qpmatpair(int paar1, int paar2)
{
 int j1, j2, j3, j4;
 int l1, l2, l3, l4;
 int l1s, l2s, l3s, l4s;
 int st1, st2, st3, st4;
 int t1, t2, t3, t4;
 int lammax,lammin,l,s,lam,ig,n1,n2,ngog;
 double sumpp, sumgog, facgog, fact1,fact2,fact0,fact4,r1,r2;
 double fact1a,fact2a,fact0a,fact4a;
 double weight,wave,fbess,facint;
 double wavea,facinta,sumgoga;

 double matasump = zero;

 st1 = iph[paar1][1];
 st2 = iph[paar1][2];
 st3 = iph[paar2][1];
 st4 = iph[paar2][2];

 t1 = t2 = iph[paar1][3];
 t3 = t4 = iph[paar2][3];

 l1 = nl[st1][t1];
 l2 = nl[st2][t2];
 l3 = nl[st3][t3];
 l4 = nl[st4][t4];
 lammax = min0(2,l1+l3,l2+l4);
 lammin = max0(2,abs0(l1-l3),abs0(l2-l4));
 j1 = nj[st1][t1];
 j2 = nj[st2][t2];
 j3 = nj[st3][t3];
 j4 = nj[st4][t4];

// CONSTANT MONOPOLE PAIRING
  
 /*sumpp = 0.0;
 if ((j1 == j2) && (l1 ==l2) && (j3 == j4) && (l3 == l4)
     &&(t1==t3) && (st1 == st2) && (st3 == st4)) sumpp = 1.0;

 sumpp *= -10.0*sqrt(2*j1)*sqrt(2*j3);
 //cout << sumpp << endl;
 return sumpp;*/

   sumpp = 0.0;
   if(t1 != t3 ) return sumpp;
   for(s = 0; s <= 1; s++)
   {
    for(l = abs0(j-s); l <= j+s; l++)
    {
     for(lam = lammin; lam <= lammax; lam++)
     {
     fact1 = s9jslj(s,l1,l2,l,j1,j2,j)*s9jslj(s,l3,l4,l,j3,j4,j);
     fact1a = s9jslj(s,l1,l2,l,j1,j2,j)*s9jslj(s,l4,l3,l,j4,j3,j);    
     
     fact2 = wigner(l1,lam,l3,0,0,0)*wigner(l2,lam,l4,0,0,0)
               *racah(l3,l4,l,l2,l1,lam);
     fact2a = wigner(l1,lam,l4,0,0,0)*wigner(l2,lam,l3,0,0,0)
               *racah(l4,l3,l,l2,l1,lam); 
	             
     fact0 =sqd[l1]*sqd[l2]*sqd[l3]*sqd[l4]*4.0
               *sq[j1]*sq[j2]*sq[j3]*sq[j4]*(2*l+1)*(2*s+1);
	       
     fact4 = iv[l+l1+l3];
     fact4a = iv[l+l1+l4];
     
     sumgog = 0.0;
     sumgoga = 0.0;
     for(ig = 1; ig <= 2; ig++)
     {
       ngog = (ig-1)*n_lag;
       facgog = gogw[ig]-gogh[ig]+(gogb[ig]-gogm[ig])*(2*s-1);
       facint = 0.0;
       facinta =0.0;
       if(abs0(fact1*fact2*fact0) > 1.0e-6) 
       {
         for(n1 = 1; n1 <= n_lag; n1++)
	 {
            for(n2 = 1; n2 <= n_lag; n2++)
	    {
	       weight = wlag[n1]*wlag[n2];
	       wave = wflag[st1][n1+ngog][t1]*wflag[st3][n1+ngog][t3]*
	              wflag[st2][n2+ngog][t2]*wflag[st4][n2+ngog][t4];
	       wavea = wflag[st1][n1+ngog][t1]*wflag[st4][n1+ngog][t4]*
	              wflag[st2][n2+ngog][t2]*wflag[st3][n2+ngog][t3];	      
	       fbess = bess[lam+1][n1][n2];
	       facint += weight*wave*fbess;
	       facinta += weight*wavea*fbess;
	     }
	  }        	  
       } // if fact1*fact2
       sumgog += facgog*facint*sqrt(pi)*pow(gogr[ig],6.0)*0.25;
       sumgoga += facgog*facinta*sqrt(pi)*pow(gogr[ig],6.0)*0.25;
       //cout << ig << "sumgog=" << sumgog << endl; 
      } // ig
      sumpp += fact1 * fact2 * fact0 * fact4 * sumgog*(2*lam+1)
        -iv[j3+j4-1-j]*(fact1a * fact2a * fact0 * fact4a * sumgoga*(2*lam+1));
     }
    }
   }
 sumpp = sumpp*vfac*0.5;
 return sumpp;
 
 
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

