#include "common.h"
#include "base.h"  
#include "funk.h"


int npair;
int jphmax;
int npair_ph;
int npair_ah;
int lphmax;

int2(iph); 
int2(kpp);
double1(eph);

void qppair(int, int);

void qppair(int j, int parity) {


    int il = 0, laufp;
    int il_ph, il_ah, il_pp;    
    int it, i1, i2;
    int l1, j1, l2, j2, kl;
    int nal;
    double ediff = zero;
    int nst;
    int jphtemp;
    int lpart = 0;
    int lhole = 0;
    int en_ok;
    double uv12;
    double cut_ah;
    int lphtemp;

    for (laufp = 1; laufp <= 2; laufp++) 
    {
	il = 0;
	il_ph = 0;
	il_ah = 0;

	for (it = 1; it <= 2; it++) 
	{
	   for (i1 = 1; i1 <= ntpar[it]; i1++) 
	   {
	      // particle (unoccupied or partially occupied) or antiparticle
	      // final state		 
	      j1 = nj[i1][it];
	      l1 = nl[i1][it];	    

	      for (i2 = 1; i2 <= ntpar[it]; i2++) 
	      {
		 en_ok = 0;
		 uv12 = abs0(uo[i1][it]*vo[i2][it]);
		// fully occupied or partially occupied
		// initial state (h or p state)
 
//                 if(eeqp[i2][it] > -1000.0) // no aa pairs
                   if(ee[i2][it] > -1000.0)
		 {
		     j2 = nj[i2][it];
		     l2 = nl[i2][it]; 
		     cut_ah = 2.0*j2*vv[i2][it];

					     
		     // if final state is antiparticle-state
//		     if ( (eeqp[i1][it] < -1000.0)  && (cut_ah >= 1.0)
//				 && (eeqp[i1][it] > -2.0*amu  ))
             if ( (ee[i1][it] < -1000.0)  && (cut_ah >= 1.0)
				 && (ee[i1][it] > -2.0*amu  ))
		     {
		        ediff = -ee[i2][it]+ee[i1][it];
		        if (fabs(ediff) <= ediffmaxd)
		           en_ok = -1;
			else 
		           en_ok = 0;						       				
		     } 
			    
		     // if final state is partially occupied or empty (qp or p state)

//		    if ((ee[i2][it] <= ee[i1][it]) && (eeqp[i1][it] > -1000.0)
//				&& (uv12 >= qptresh) ) 
//	        if ((ee[i2][it] <= ee[i1][it]) && (ee[i1][it] > -1000.0)
//				&& (vv[i2][it] >= qptresh) && (vv[i1][it] < qptresh))//? or cut_ah>1?
	        if ((ee[i2][it] <= ee[i1][it]) && (ee[i1][it] > -1000.0)
				&& (uv12 >= qptresh))      
	            {			       
			ediff = ee[i1][it]-ee[i2][it];  
			if (fabs(ediff) <= ediffmaxu)
			   en_ok = 1;
		        else
			   en_ok = 0;			        
		    }
			     			    
		 } // if(eeqp[i2][it] > -1000)     
		   // check conditions for ph or pp pairs		    
		 if ((abs0(j1-j2) <= j) && (j <= (j1+j2-1))
		     && (((l1+l2+parity)%2) == 1)
		     && ((en_ok == 1) ||(en_ok == -1)) && i1!= i2 )
		 {    
		     il += 1;
		     switch (en_ok)
		     {
			case 1 : il_ph += 1; break;
			case -1: il_ah += 1; break;
                     }
		     if (laufp == 2) 
		     {
			eph[il] = ediff;
			iph[il][1] = i1;
			iph[il][2] = i2;
			iph[il][3] = it;
			iph[il][4] = en_ok;    
		        kpp[i1][i2] = il;										
		      } // if laufp = 2									
	         } // if triangle rule plus parity    			
	      } // for i2		
	   } // for i1	    
	} // for it	
    	
	if (laufp < 2) 
	{
	   npair = il;
	   npair_ph = il_ph;
	   npair_ah = il_ah;	    	    
	   if (npair == 0) 
	   {
		cout << "there were no pairs found!" << endl
		  << "calculation will be terminated!" << endl;
		exit(-1);
	   }

	    // Allocation of Array-Objects

	    int2init(iph,npair,4); 
	    int2init(kpp,ntmax,ntmax);
	    double1init(eph,npair);
	    	    	    
	} // if laufp < 2
		
    } // for laufp

   cout << "... total number of pairs npair = " << npair << endl;

  // determination of maximal jp+jh and lp + lh


    jphmax = 0;
    lphmax = 0;

    int it1, it2;
    

    for (i1 = 1; i1 <= npair; i1++)
    {
	for (i2 = 1; i2 <= npair; i2++)
	{
	
	    it1 = iph[i1][3];
	    it2 = iph[i2][3];
	    
    
	    jphtemp = min0(2,(nj[iph[i1][1]][it1]+nj[iph[i2][1]][it2]),
			   (nj[iph[i1][2]][it1]+nj[iph[i2][2]][it2]));
	    lphtemp = nl[iph[i1][1]][it1]+nl[iph[i2][1]][it2];
	    if((lphtemp > lphmax) && (iph[i1][4] == 1) && 
	         (iph[i2][4] == 1)) lphmax = lphtemp;
	
	    if (jphtemp > jphmax)
	      jphmax = jphtemp;
	}   
    }  
    cout << "lphmax=" << lphmax << endl;
    return;
} // void pairt












