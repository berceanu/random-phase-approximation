#include "common.h"
#include "base.h"
#include "sla.h"
#include "funk.h"
#include "edmonds.h"


static int lcal(int, int, int);
static void write_head(fstream &, int, int);
static char lname (int);


void excstr(double *erpa, double **xrpa,
	    double **yrpa, int npair, int j, char *fileskal,
	    char *filevec, char *filecurv, char *fileneu, 
	    char *filepro, char *filetot, char *filelskal,
	    char *filelvec, char *filepskal, char *filepvec,
	    char *filestrength, double lswid, double lvwid,
	    int hp)
{    

    int pairc;
    int energyc;
    double elstrength, elstrengthsum;
    double protmonsum, neutmonsum;
    double protelsum, neutelsum;
    double protmagsum, neutmagsum;
    double magstrength, magstrengthsum;
    double monstrength, monstrengthsum;
    double strength;
    int st1, l1, j1;
    int st2, l2, j2;
    int l1g, l2g;    
    int iso;
    int i;
    fstream skalfile;
    fstream vecfile;    
    fstream curvfile;
    fstream neudensf;
    fstream prodensf;
    fstream totdensf;   
    fstream lorskalfile;
    fstream lorvecfile;
    fstream purskalfile;
    fstream purvecfile;
    fstream strengthfile;
//add    
    fstream lorskalfile1;
    fstream lorvecfile1;
    
    int nl1, nl2;
    double sum, xwidth, xl;
    double tdens, totdensum, prodensum, neudensum;
    double prodens, neudens;
    int1(energ);
    double monstr, elstr, magstr;
    
    double monsumskal, monsumvec;
    double elsumskal, elsumvec;
    double magsumskal, magsumvec;
    double dipol_skalar, dipol_skalar_sum;
    double dipol_toroidal;
    double1(bmonskal);
    double1(bmonvec);
    double1(belskal); 
    double1(belvec);
    double1(bmagskal);
    double1(bmagvec);
    double1(stre);
    double2(selstrength);

    double1init(bmonskal,ndim_o_c);
    double1init(bmonvec,ndim_o_c);
    double1init(belskal,ndim_o_c);
    double1init(belvec,ndim_o_c);
    double1init(bmagskal,ndim_o_c);
    double1init(bmagvec,ndim_o_c);
    double1init(stre,ndim_o_c);
    double neufact;
    double profact;

    double2init(selstrength,2,npair);

    double xy_norm,xy_norm1;
    double sum_test;
    double sum_out;
    int energy_cal;
    double sum_xx, sum_yy;
    double sum_out_proton, sum_out_neutron;
    double energy_peak;

    
    int1init(energ,ndim_o_c);
    
    int energy_start;
    
    
    energy_start = 1;
    
    int erp_ok;
        
    int erp_ok_1;
     
    xy_norm = 0.0;
    sum_xx=0.0;
    sum_yy=0.0;
    sum_out_proton=0.0;
    sum_out_neutron=0.0;
    // change this value for displaying higher energies
    const double exc_erg_max = 25.0;
    cout << "Maximal RPA energy : " << erpa[ndim_o_c] << endl;
    cout << "exc_erg_max = " << exc_erg_max << endl;
   


    //printf("RPA Eigenvalue for calculating X,Y contributions --->");
    //scanf("%lf",&energy_peak);
    //PEAK FOR ANALYSIS IS WRITTEN IN START.DAT - transerg  
       energy_peak=transerg;       
    
    // for j=1 transition- isovector dipole-operator
    neufact = (double(npro))/(double(npro+nneu));
    profact = (double(nneu))/(double(npro+nneu));

    // searching for RPA-eigenvalue close to the energy_peak from input
  energy_cal = energy_start;
  for (energyc = energy_start; energyc <= ndim_o_c; energyc++)
    {
     if (abs0(erpa[energyc]-energy_peak) < 1.e-2)
     {
      energy_cal = energyc; 
      break;
     }

    } 

    // summing up excitations strengths for valid energies
    for (energyc = energy_start; energyc <= ndim_o_c; energyc++) 
    {	
        // no imaginary states
	if (c_erpa[energyc] == zero)
	  erp_ok_1 = 1;
	else
	  erp_ok_1 = 0;
     	
	if ((erpa[energyc] > 0.0) && (erp_ok_1 == 1))
	{	    
	    elstrengthsum = magstrengthsum = zero;
	    dipol_skalar_sum = zero;
	    
	
	    neutmonsum = neutelsum = neutmagsum = zero;	
	    protmonsum = protelsum = protmagsum = zero;
	
	    monstrengthsum = zero;

	    for (pairc = 1; pairc <= npair; pairc++) 
	    {    
		erp_ok = 1;
		    
		iso = iph[pairc][3];		    
//particle
		st1 = iph[pairc][1];
		l1 = nl[st1][iso];		  
		j1 = nj[st1][iso];
		l1g = lcal(l1,j1,2);
		  
//hole
		st2 = iph[pairc][2];
		l2 = nl[st2][iso];
		j2 = nj[st2][iso];
		l2g = lcal(l2,j2,2);
	
//  NORMALIZATION OF X`s and Y`s
// 
       
       if (energyc == energy_cal)
       {
       xy_norm+=xrpa[pairc][energy_cal]*xrpa[pairc][energy_cal]-
		yrpa[pairc][energy_cal]*yrpa[pairc][energy_cal];
       xy_norm1=xrpa[pairc][energy_cal]*xrpa[pairc][energy_cal]-
		yrpa[pairc][energy_cal]*yrpa[pairc][energy_cal];		
       sum_xx+=xrpa[pairc][energy_cal]*xrpa[pairc][energy_cal];
       sum_yy+=yrpa[pairc][energy_cal]*yrpa[pairc][energy_cal];
        
       if (abs0(xy_norm1) > 0.01)
               cout << pairc << " " << xy_norm1 << endl;
       }



		if (j == 0) 
		{
		    monstrength = (xrpa[pairc][energyc]
				   +yrpa[pairc][energyc])*
				     (monred(st1,l1,j1,iso,1,
					     st2,l2,j2,iso,1)
				      +monred(st1,l1g,j1,iso,2, // sign is changed from original -
					      st2,l2g,j2,iso,2));
	         monstrength *= (uo[st1][iso]*vo[st2][iso]+
		     vo[st1][iso]*uo[st2][iso]);
				
		 monstrengthsum += monstrength;
		}
	    
		else 
		{

		    if (natural_parity == 1) 
		    {
			    
			elstrength = (xrpa[pairc][energyc]
				      +iv[abs0(j)]
				      *yrpa[pairc][energyc])*
					(elred(st1,l1,j1,iso,1,
					       st2,l2,j2,iso,1,j)
					 +elred(st1,l1g,j1,iso,2,
						st2,l2g,j2,iso,2,j));
		        elstrength *= (uo[st1][iso]*vo[st2][iso]
			  +iv[j]*vo[st1][iso]*uo[st2][iso]);		            		      
			elstrengthsum += elstrength;
    if (abs0(elstrength) > 0.001 && energyc == energy_cal)
    {
    printf("%d  %10.5lf  ->  %10.5lf %d%c%d/2  -> %d%c%d/2   %12.8lf  X=%10.5lf Y=%10.5lf\n",
              iso, ee[iph[pairc][2]][iso],
              ee[iph[pairc][1]][iso],
              nr[iph[pairc][2]][iso],lname(l2),
              j2*2-1,
              nr[iph[pairc][1]][iso],lname(l1),
              j1*2-1,
              elstrength, xrpa[pairc][energyc], yrpa[pairc][energyc]);
    // strengthfile << eph[pairc] << " " << abs0(sum_out) << endl;

    }
			
		    }
			
		    else 
		    {
			magstrength =
			  (magred(st1,l1,j1,iso,1,st2,l2,j2,iso,1,j)
			   +magred(st1,l1g,j1,iso,2,st2,l2g,j2,iso,2,j))*
			     xrpa[pairc][energyc]
			       +iv[abs0(j1-j2+j)]*yrpa[pairc][energyc]
				 *(magred(st2,l2,j2,iso,
					  1,st1,l1,j1,iso,1,j)
				   +magred(st2,l2g,j2,iso,
					   2,st1,l1g,j1,iso,2,j));
		      

			magstrengthsum += magstrength;
 		    }
			
		    if (j == 1) 
		    {	
			if (natural_parity == 1) 
			{
		      //DIPOLE ISOSCALAR
                   	
	    	       dipol_skalar = 
			      (xrpa[pairc][energyc]
			        +iv[abs0(j)]
			       *yrpa[pairc][energyc])*
				 (dipskalred1(st1,l1,j1,
					     iso,1,st2,l2,j2,iso,1)
			 	  +dipskalred1(st1,l1g,j1,
					      iso,2,st2,l2g,j2,iso,2));
		       dipol_skalar *= (uo[st1][iso]*vo[st2][iso]
		       +iv[j]*vo[st1][iso]*uo[st2][iso]);
                  /*                                  
                        //TOROIDAL 
                     
                              dipol_toroidal =
                              (xrpa[pairc][energyc]
                               -iv[abs0(j)]
			       *yrpa[pairc][energyc]) // *iv[abs0(j1+j2-j)]
                               *(-diptoroidred(st1,l1g,j1,
                                             iso,2,st2,l2,j2,iso,1)
                               +diptoroidred(st1,l1,j1,
                                           iso,1,st2,l2g,j2,iso,2)); 
			dipol_skalar = dipol_toroidal
                            *(uo[st1][iso]*vo[st2][iso]
                       +iv[j]*vo[st1][iso]*uo[st2][iso]);
                   */
	        		
			}			    			    
		    }			
		}
				    		 
		if (iso == 1)
		{
		   if (j == 0)
		      neutmonsum += monstrength;		
		   else 
		   {
		      if (natural_parity == 1)
                         {
			  neutelsum += elstrength;
                         }
		      else
			 neutmagsum += magstrength;                      
		    }
		
		}		
		else
		{			
		    if (j == 0)
		      protmonsum += monstrength;		
		    else 
		    {		
			if (natural_parity == 1)
                        {
                          // iso = 2
			  protelsum += elstrength;
                        }
			else
			  protmagsum += magstrength;
		    }
			
		}
		    
		// isoscalar dipole-mode
		if (j == 1) 
		{
		    if (natural_parity == 1)
		      dipol_skalar_sum +=
			dipol_skalar;
		}
		    
	    } // end of the loop for all p-h pairs, still remains loop for energy
	    	    
	    if (j == 0)
	    {	    
		monsumskal = abs0((neutmonsum+protmonsum)*
				  (neutmonsum+protmonsum));
		
		monsumvec = abs0((neutmonsum-protmonsum)*
				 (neutmonsum-protmonsum));
	        
		bmonskal[energyc] = monsumskal;	      

		bmonvec[energyc] = monsumvec;	      			  
	    }	    
	    else 
	    {
		if (natural_parity == 1)
		{		    
		    if (j == 1)
		      elsumskal = dipol_skalar_sum*dipol_skalar_sum;
		    else
		      elsumskal = abs0((neutelsum+protelsum)
			      *(neutelsum+protelsum));

		    if (j == 1)
		    {
 		       elsumvec = (-1.0*profact*protelsum + neufact*neutelsum )*
				( -1.0*profact*protelsum +neufact*neutelsum );
                    }
		    else
		      elsumvec =
                              protelsum*protelsum;
                         //   abs0((protelsum-neutelsum)
			 //     *(protelsum-neutelsum));

		    
		    belskal[energyc] = elsumskal;		
		    belvec[energyc] = elsumvec;
		}
		else 
		{		
		    magsumskal = abs0((neutmagsum+protmagsum)
			    *(neutmagsum+protmagsum)); 
  
		    magsumvec = abs0((neutmagsum-protmagsum)
			    *(neutmagsum-protmagsum));
	    	    
	    
		    bmagskal[energyc] = magsumskal;
		    bmagvec[energyc] = magsumvec;
		}	 				    
	    }	    		    
	}							
    }

    cout << "calculation of strengths finished" << endl;
    
    skalfile.open(fileskal, ios::out | ios::trunc);
    skalfile.setf(ios::scientific);
    write_head(skalfile,0,hp);

    vecfile.open(filevec, ios::out | ios::trunc);
    vecfile.setf(ios::scientific);
    write_head(vecfile,1,hp);
    
    curvfile.open(filecurv, ios::out | ios::trunc);
    curvfile.setf(ios::scientific);
    write_head(curvfile,-1,hp);

    neudensf.open(fileneu, ios::out | ios::trunc);
    neudensf.setf(ios::scientific);
    write_head(neudensf,-1,hp);
    
    prodensf.open(filepro, ios::out | ios::trunc);
    prodensf.setf(ios::scientific);
    write_head(prodensf,-1,hp);

    totdensf.open(filetot, ios::out | ios::trunc);
    totdensf.setf(ios::scientific);
    write_head(totdensf,-1,hp);
    
    lorskalfile.open(filelskal, ios::out | ios::trunc);
    lorskalfile.setf(ios::scientific);
    write_head(lorskalfile,0,hp);
    
    lorvecfile.open(filelvec, ios::out | ios::trunc);
    lorvecfile.setf(ios::scientific);
    write_head(lorvecfile,1,hp);
    
    strengthfile.open(filestrength, ios::out | ios::trunc);
    strengthfile.setf(ios::scientific);
    write_head(strengthfile,-1,hp);
    
 //add    
    lorskalfile1.open("ftes_REsca.out", ios::out | ios::trunc);
    lorskalfile1.setf(ios::scientific);
    write_head(lorskalfile1,0,hp);
    
    lorvecfile1.open("ftes_REvec.out", ios::out | ios::trunc);
    lorvecfile1.setf(ios::scientific);
    write_head(lorvecfile1,1,hp);

    strengthfile << "# 2qp contributions " << endl;
    if( energy_cal != energy_start)
    {
    cout << "ERPA = " << erpa[energy_cal] << endl;
    cout << "Sum XX = " << sum_xx << "    Sum YY = " << sum_yy ;
    cout << "     Sum XX-YY =" << xy_norm << "\n" << endl;
    sum_test=0.0;
    cout << " 1=n/2=p       E/hole      E/particle  XX-YY/%" << endl;
    for(pairc=1; pairc <= npair; pairc++)
    {
    iso = iph[pairc][3];

    st2 = iph[pairc][2];

    st1 = iph[pairc][1];

    l1 = nl[st1][iso];

    l2 = nl[st2][iso];

    j1 = nj[st1][iso];

    j2 = nj[st2][iso];

    sum_out =(100.0*(xrpa[pairc][energy_cal]*xrpa[pairc][energy_cal]
             -yrpa[pairc][energy_cal]*yrpa[pairc][energy_cal])/xy_norm);
    if (abs0(sum_out)> 0.01)
    {
    printf("%d  %10.5lf  ->  %10.5lf %d%c%d/2  -> %d%c%d/2   %12.8lf\n",
              iso, ee[iph[pairc][2]][iso],
              ee[iph[pairc][1]][iso],
              nr[iph[pairc][2]][iso],lname(l2),
              j2*2-1,
              nr[iph[pairc][1]][iso],lname(l1),
              j1*2-1,
              sum_out);
    strengthfile << eph[pairc] << " " << abs0(sum_out) << endl;

    }
    sum_test+=sum_out;
   //    if (abs0(sum_out)>0.1)
       {
        if (iso == 1) sum_out_neutron+=abs0(sum_out);
        else sum_out_proton+=abs0(sum_out);
       }
    }
    printf("Sum XX-YY after normalization * 100 = %lf\n", sum_test);
    printf("Sum XX-YY for protons =%lf\n", sum_out_proton);
    printf("Sum XX-YY for neutrons=%lf\n", sum_out_neutron);
    }
    	  
 
    double2(xplot);
    double2init(xplot,5000,2);
    double lskalval;
    double lvecval;
    double1(gamlor);
    const double xxl = 0.01;
    int xi;    
 
    int en_count = 0;
    double1(xplot_skal_max);
    double1(xplot_vec_max);

    double1init(xplot_skal_max,2);
    double1init(xplot_vec_max,2);    
    double orig_skal_max, orig_vec_max; 
    xplot_skal_max[1] = zero;
    xplot_vec_max[1] = zero;
    orig_skal_max = zero;
    orig_vec_max = zero;


    double1init(gamlor,2);
    gamlor[1] = lswid;
    gamlor[2] = lvwid;

  //another formula for R(E) 
    
    double2(xplot1);
    double2init(xplot1,5000,2);

    double1(xplot_skal_max1);
    double1(xplot_vec_max1);

    double1init(xplot_skal_max1,2);
    double1init(xplot_vec_max1,2);  
    
    xplot_skal_max1[1] = zero;
    xplot_vec_max1[1] = zero;
   
    for (energyc = energy_start; energyc <= ndim_o_c; energyc++) 
    {
	if (c_erpa[energyc] == zero)
	  erp_ok = 1;
	else
	  erp_ok = 0;
	
	if ((erpa[energyc] > 0.0) && (erpa[energyc] < exc_erg_max) 
	    && (erp_ok == 1)) 
	{
	    
	    en_count++;
	     	
	    if (j == 0) 
	    {	
	        if(bmonskal[energyc] > orig_skal_max) orig_skal_max=bmonskal[energyc];
		if(bmonvec[energyc] > orig_vec_max) orig_vec_max=bmonvec[energyc];
		skalfile << erpa[energyc] << "\t" << bmonskal[energyc] << endl;
		vecfile << erpa[energyc] << "\t" << bmonvec[energyc] << endl; 
		
		lskalval = bmonskal[energyc];
		lvecval = bmonvec[energyc];

	    }
	
	    else
	    {
		if (natural_parity == 1) 
		{
                    if(belskal[energyc] > orig_skal_max) orig_skal_max=belskal[energyc];
		    if(belvec[energyc] > orig_vec_max) orig_vec_max=belvec[energyc];
		    skalfile << erpa[energyc] << "\t" << belskal[energyc]
		      << endl;
		    vecfile << erpa[energyc] << "\t" << belvec[energyc]
		      << endl;
		    if ((erpa[energyc] > 2.0) || (j != 1))
		    {
		      lskalval = belskal[energyc];
		      lvecval = belvec[energyc];
                    }
		    else
		    {
		     lskalval = zero;
		     lvecval = zero;
                    }
		}
		else 
		{
		    if(bmagskal[energyc] > orig_skal_max) orig_skal_max=bmagskal[energyc];
		    if(bmagvec[energyc] > orig_vec_max) orig_vec_max=bmagvec[energyc];
		    skalfile << erpa[energyc] << "\t" << bmagskal[energyc]
		      << endl;
		    vecfile << erpa[energyc] << "\t" << bmagvec[energyc]
		      << endl;
		    lskalval = bmagskal[energyc];
		    lvecval = bmagvec[energyc];	
		}
		
	    }

 
	    for (xi = 1; xi <= 5000; xi++)
	    {
		xplot[xi][1] += lskalval*1./(pow(xi*xxl-erpa[energyc],2.)
					     + (gamlor[1]*gamlor[1]/4.))
		  *(gamlor[1]*gamlor[1]/4.)*(2.0/(pi*gamlor[1]));		
		
		xplot[xi][2] += lvecval*1./(pow(xi*xxl-erpa[energyc],2.)
					    + (gamlor[2]*gamlor[2]/4.))
		  *(gamlor[2]*gamlor[2]/4.)*(2.0/(pi*gamlor[2]));
	
		if ((xplot[xi][1] > xplot_skal_max[1])&&(xi > 200)) 
		{		    
		    xplot_skal_max[1] = xplot[xi][1];
		    xplot_skal_max[2] = xi*xxl;
		}
		
		if (xplot[xi][2] > xplot_vec_max[1]) 
		{		    
		    xplot_vec_max[1] = xplot[xi][2];
		    xplot_vec_max[2] = xi*xxl;
		}		
	    }	
	    
	    //another formula for R(E)
	    
	  	    for (xi = 1; xi <= 5000; xi++)
	    {
		xplot1[xi][1] += lskalval*1./(pow(xi*xxl-erpa[energyc],2.)
					     + (gamlor[1]*gamlor[1]/4.))
		  *(gamlor[1]*gamlor[1]/4.);		
		
		xplot1[xi][2] += lvecval*1./(pow(xi*xxl-erpa[energyc],2.)
					    + (gamlor[2]*gamlor[2]/4.))
		  *(gamlor[2]*gamlor[2]/4.);
	
		if ((xplot[xi][1] > xplot_skal_max1[1])&&(xi > 200)) 
		{		    
		    xplot_skal_max1[1] = xplot[xi][1];
		    xplot_skal_max1[2] = xi*xxl;
		}
		
		if (xplot[xi][2] > xplot_vec_max1[1]) 
		{		    
		    xplot_vec_max1[1] = xplot[xi][2];
		    xplot_vec_max1[2] = xi*xxl;
		}		
	    }	          
	    
	}		
    }

    
    lorskalfile << "#width: " << gamlor[1] << endl;
    lorskalfile << "#maximum value: " << xplot_skal_max[1] << endl;
    lorskalfile << "#at energy: " << xplot_skal_max[2] << endl;

    lorvecfile << "#width: " << gamlor[2] << endl;
    lorvecfile << "#maximum value: " << xplot_vec_max[1] << endl;
    lorvecfile << "#at energy: " << xplot_vec_max[2] << endl;


	
    for (xi = 0; xi <= 5000; xi++)
    {
	lorskalfile << xi*xxl << "\t" << xplot[xi][1] << endl;
	lorvecfile << xi*xxl << "\t" << xplot[xi][2] << endl;
    }
    
    
//another formula for R(E) 
    lorskalfile1 << "#width: " << gamlor[1] << endl;
    lorskalfile1 << "#maximum value: " << xplot_skal_max1[1] << endl;
    lorskalfile1 << "#at energy: " << xplot_skal_max1[2] << endl;

    lorvecfile1 << "#width: " << gamlor[2] << endl;
    lorvecfile1 << "#maximum value: " << xplot_vec_max1[1] << endl;
    lorvecfile1 << "#at energy: " << xplot_vec_max1[2] << endl;


	
    for (xi = 0; xi <= 5000; xi++)
    {
	lorskalfile1 << xi*xxl << "\t" << xplot1[xi][1] << endl;
	lorvecfile1 << xi*xxl << "\t" << xplot1[xi][2] << endl;
    }    
    



    // writing "pure" data-files

    purskalfile.open(filepskal, ios::out | ios::trunc);
    purskalfile.setf(ios::scientific);

    purvecfile.open(filepvec, ios::out | ios::trunc);
    purvecfile.setf(ios::scientific);
    

    purskalfile << en_count << endl;
    purvecfile << en_count << endl;
      


    for (energyc = energy_start; energyc <= ndim_o_c; energyc++) 
    {
	if (c_erpa[energyc] == zero)
	  erp_ok = 1;
	else
	  erp_ok = 0;
	
	
	
	if ((erpa[energyc] > 0.0)  && (erpa[energyc] < exc_erg_max) 
	    && (erp_ok == 1)) 
	{

	    if (j == 0)
	    {		
		purskalfile << erpa[energyc] << "\t" << bmonskal[energyc]
		  << endl;
		purvecfile << erpa[energyc] << "\t" << bmonvec[energyc]
		  << endl;
		
	    }
	    else 
	    {

		if (natural_parity == 1) 
		{		    
		    purskalfile << erpa[energyc] << "\t" << belskal[energyc]
		      << endl;
		    purvecfile << erpa[energyc] << "\t" << belvec[energyc]
		      << endl;
		}
		else 
		{
		    purskalfile << erpa[energyc] << "\t" << bmagskal[energyc]
		      << endl;
		    purvecfile << erpa[energyc] << "\t" << bmagvec[energyc]
		      << endl;
		}


	    }
	}
    }

    // calculating sum-rules

    
    double m_minus1_skal_sum = zero;
    double m_minus1_vec_sum = zero;
    double m_0_skal_sum = zero;
    double m_0_vec_sum = zero;
    double m_1_skal_sum = zero;
    double m_1_vec_sum = zero;
    double m_3_skal_sum = zero;

    double m_0_vec_sum_low = zero;
    double m_1_vec_sum_low = zero;
    double m_2_vec_sum_low = zero;
    double m_0_vec_sum_high = zero;
    double m_1_vec_sum_high = zero;
    
    double m_0_skal_sum_low = zero;
    double m_1_skal_sum_low = zero;
    double m_0_skal_sum_high = zero;
    double m_1_skal_sum_high =zero;
    

    double1(m_minus1_skal);
    double1(m_minus1_vec);
    double1(m_0_skal);
    double1(m_0_vec);
    double1(m_1_skal);
    double1(m_1_vec);
    double1(m_2_vec);
    double1(m_3_skal);

    double1init(m_minus1_skal,ndim_o_c);
    double1init(m_minus1_vec,ndim_o_c);
    double1init(m_0_skal,ndim_o_c);
    double1init(m_3_skal,ndim_o_c);
    double1init(m_0_vec,ndim_o_c);
    double1init(m_1_skal,ndim_o_c);
    double1init(m_1_vec,ndim_o_c);
    double1init(m_2_vec,ndim_o_c);
    
    double ewsr_max;
    int en_lauf;
    
//    ewsr_max = 13.0;

    for(ewsr_max = 10.0; ewsr_max <= 11.0; ewsr_max+=1.0)
    {

    m_minus1_skal_sum = zero;
    m_minus1_vec_sum = zero;
    m_0_skal_sum = zero;
    m_0_vec_sum = zero;
    m_1_skal_sum = zero;
    m_1_vec_sum = zero;
    m_3_skal_sum = zero;
    

    m_0_vec_sum_low = zero;
    m_1_vec_sum_low = zero;
    m_2_vec_sum_low = zero;
    m_0_vec_sum_high = zero;
    m_1_vec_sum_high = zero;
    
    m_0_skal_sum_low = zero;
    m_1_skal_sum_low = zero;
    m_0_skal_sum_high = zero;
    m_1_skal_sum_high =zero;

    en_lauf = 0;

    for (energyc = energy_start; energyc <= ndim_o_c; energyc++) 
    {
	if (c_erpa[energyc] == zero)
	  erp_ok = 1;
	else
	  erp_ok = 0;
	
	 
	
	if ((erpa[energyc] > 2.0) && (erp_ok == 1)
	 && (erpa[energyc] < exc_erg_max )  ) 
	{
	    en_lauf++;
	    
	    // m-minus1-sumrule
	    if (j == 0) 
	    {		
	        m_minus1_skal[en_lauf] = bmonskal[energyc]/erpa[energyc];
		m_minus1_vec[en_lauf] = bmonvec[energyc]/erpa[energyc];
                m_0_skal[en_lauf] = bmonskal[energyc];

                m_1_skal[en_lauf] = bmonskal[energyc]*erpa[energyc];
                m_3_skal[en_lauf] = bmonskal[energyc]*pow(erpa[energyc],3);
		
                m_minus1_skal_sum += m_minus1_skal[en_lauf];
		m_minus1_vec_sum += m_minus1_vec[en_lauf];

                m_0_skal_sum += m_0_skal[en_lauf];
                m_1_skal_sum += m_1_skal[en_lauf];
                m_3_skal_sum += m_3_skal[en_lauf];
		
	    }
	    

	    //m_1_sumrule and m_0
	    else
	    {
		if (natural_parity == 1)
		{
		    
		    m_0_skal[en_lauf] = belskal[energyc];
		    m_0_vec[en_lauf] = belvec[energyc];
		    
		    m_1_skal[en_lauf] = belskal[energyc]*erpa[energyc];

                    m_3_skal[en_lauf] = belskal[energyc]*pow(erpa[energyc],3);
		    m_1_vec[en_lauf] = belvec[energyc]*erpa[energyc];

                    m_2_vec[en_lauf] = belvec[energyc]*erpa[energyc]*erpa[energyc];
		}
		else
		{
		    m_0_skal[en_lauf] = bmagskal[energyc];
		    m_0_vec[en_lauf] = bmagvec[energyc];
		    
		    m_1_skal[en_lauf] = bmagskal[energyc]*erpa[energyc];
		    m_1_vec[en_lauf] = bmagvec[energyc]*erpa[energyc];  
		}
		

		m_0_skal_sum += m_0_skal[en_lauf];
		m_0_vec_sum += m_0_vec[en_lauf];
		
		m_1_skal_sum += m_1_skal[en_lauf];
		m_1_vec_sum += m_1_vec[en_lauf];

                m_3_skal_sum += m_3_skal[en_lauf];

		if(erpa[energyc] <= ewsr_max) 
//                   if(erpa[energyc] <= 19.0 && erpa[energyc] >= 13.0)
		{
		 m_0_vec_sum_low+=m_0_vec[en_lauf];
		 m_1_vec_sum_low+=m_1_vec[en_lauf];
                 m_0_skal_sum_low+=m_0_skal[en_lauf];
		 m_1_skal_sum_low+=m_1_skal[en_lauf];

                 m_2_vec_sum_low += m_2_vec[en_lauf];
		 

		}
		else
		{
		 m_0_vec_sum_high+=m_0_vec[en_lauf];
		 m_1_vec_sum_high+=m_1_vec[en_lauf];
		 m_0_skal_sum_high+=m_0_skal[en_lauf];
		 m_1_skal_sum_high+=m_1_skal[en_lauf];
		}
		
	    }
	    
	}
    }
        
    strengthfile << "---------------------------------------------------" << endl;

    if (j == 0)
    {	
	strengthfile << "#isovector m_-1-strength: " << m_minus1_vec_sum 
	             << endl << endl;
        strengthfile << "#isoscalar m_-1-strength: " << m_minus1_skal_sum
                     << endl << endl;
        strengthfile << "#isoscalar m_0-strength: " << m_0_skal_sum
                     << endl << endl;
        strengthfile << "#isoscalar m_1-strength: " << m_1_skal_sum
                     << endl << endl;
        strengthfile << "#isoscalar m_3-strength: " << m_3_skal_sum
                     << endl << endl;

        strengthfile << "#isoscalar m_1/m_0 = "
          << m_1_skal_sum/m_0_skal_sum<< endl;

        strengthfile << "#isoscalar SQRT(m_3/m_1) = "
          << sqrt(m_3_skal_sum/m_1_skal_sum) << endl;

        strengthfile << "#isoscalar SQRT(m_1/m_minus1_skal) = "
          << sqrt(m_1_skal_sum/m_minus1_skal_sum) << endl;


    }
    else 
    { 
	strengthfile << "#isoscalar m_0-strength: " << m_0_skal_sum 
	  << endl << endl;
	strengthfile << "#isovector m_0-strength: " << m_0_vec_sum 
	  << endl << endl;


	strengthfile << "#isoscalar m_1-strength: " << m_1_skal_sum 
	  << endl << endl;
	strengthfile << "#isovector m_1-strength: " << m_1_vec_sum 
	  << endl << endl;
      if(j == 1)
      {
       strengthfile << "IV m_1 strength/TRK" <<
			m_1_vec_sum/(14.9*nneu*npro/nama) << endl;
       strengthfile << "IV m_strength_low/TRK" 
			<< m_1_vec_sum_low/(14.9*nneu*npro/nama) << endl;
      }
        strengthfile << "#isoscalar m_1/m_0 = "
          << m_1_skal_sum/m_0_skal_sum<< endl;

        strengthfile << "#isoscalar SQRT(m_3/m_1) = "
          << sqrt(m_3_skal_sum/m_1_skal_sum) << endl;

        strengthfile << "#isovector m_1 low (E<" << ewsr_max << " MeV) strength: " 
	 << m_1_vec_sum_low << endl <<endl;
        strengthfile << "#isovector m_0 low (E<" << ewsr_max << " MeV) strength: "
	 << m_0_vec_sum_low << endl << endl;
        strengthfile << "#isovector m_1 high (E>" << ewsr_max << " MeV) strength: "
	 << m_1_vec_sum_high << endl << endl;
        strengthfile << "#isovector m_0 high (E>" << ewsr_max << " MeV) strength: "
	 << m_0_vec_sum_high << endl << endl;
//        strengthfile << "#IVGDR CENTROID ENERGY (SN ISOTOPES) =" 
//	 << m_1_vec_sum_low/m_0_vec_sum_low << endl;
        strengthfile << "#isovector m_1/m_0 low (E<" << ewsr_max << " MeV)="
         << m_1_vec_sum_low/m_0_vec_sum_low << endl;
        strengthfile << "#isovector m_1/m_0 high (E>" << ewsr_max << " MeV)="
	 << m_1_vec_sum_high/m_0_vec_sum_high << endl;
        strengthfile << "#isovector m_1 low/m_1 high = "
	 << m_1_vec_sum_low/m_1_vec_sum_high << endl << endl;

        strengthfile << "#isoscalar m_1/m_0 low (E<" << ewsr_max << " MeV)="
	  << m_1_skal_sum_low/m_0_skal_sum_low << endl;
        strengthfile << "#isoscalar m_1/m_0 high (E>" << ewsr_max << " MeV)="
		   << m_1_skal_sum_high/m_0_skal_sum_high << endl;
        strengthfile << "#width low ="
                     << sqrt(m_2_vec_sum_low/m_0_vec_sum_low-
                        pow(m_1_vec_sum_low/m_0_vec_sum_low,2)) << " MeV" << endl;
        
        strengthfile << "m_2_vec_sum_low/m_0_vec_sum_low = " 
                     << m_2_vec_sum_low/m_0_vec_sum_low << endl;
        strengthfile << "pow(m_1_vec_sum_low/m_0_vec_sum_low,2)" 
                     << pow(m_1_vec_sum_low/m_0_vec_sum_low,2) << endl; 


    }
    } // for ews_max
    
    strengthfile << endl << endl;    
    strengthfile << "#percentages:" << endl;
    

    en_lauf = 0;
    
    for (energyc = energy_start; energyc <= ndim_o_c; energyc++) 
    {
	if (c_erpa[energyc] == zero)
	  erp_ok = 1;
	else
	  erp_ok = 0;
			
	if ((erpa[energyc] > 0.0) && (erp_ok == 1)
	  && (erpa[energyc] < exc_erg_max)  ) 
	{  
	    en_lauf++;
	     
	    strengthfile << "erpa[" << energyc << "]: " 
	      << erpa[energyc] << endl;
		
	    if (j == 0) 
	    {
		strengthfile << "isoscalar m_-1: " <<
		  m_minus1_skal[en_lauf]/m_minus1_skal_sum*100. << " %"
		    << endl;
		strengthfile << "isovector m_-1: " <<
		  m_minus1_vec[en_lauf]/m_minus1_skal_sum*100. << " %"
		    << endl;
	    }
	    else 
	    {
		strengthfile << "isoscalar m_0: " <<
		  m_0_skal[en_lauf]/m_0_skal_sum*100. << " %"
		    << endl;
		strengthfile << "isovector m_0: " <<
		  m_0_vec[en_lauf]/m_0_vec_sum*100. << " %"
		    << endl;

		strengthfile << "isoscalar m_1: " <<
		  m_1_skal[en_lauf]/m_1_skal_sum*100. << " %"
		    << endl;
		strengthfile << "isovector m_1: " <<
		  m_1_vec[en_lauf]/m_1_vec_sum*100. << " %"
		    << endl;
		
	    }
	}
    } 

} // excstr


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



static void write_head(fstream &resfile, int ispar, int ihar)
{
    int i;
    
    
    resfile << "#RPA-results:" << endl;
    resfile << "#Nucleus: " << nucnam << " " << nama << endl;
    resfile << "#Excitation: ";
    resfile << j;
      
    if (parity == 0)
      resfile << " -" << endl;
    else
      resfile << " +" << endl;
    	
    resfile << "#Total number of pairs: " << npair << endl; 
    resfile << "#Number of ph-/ah-pairs: " <<
	  npair_ph << "/" << npair_ah << endl;
    
    resfile 
	  << "#Maximal excitation-energy for particle-hole-pairs: " 
	    << int(ediffmaxu)
	      << endl;
    resfile 
	  << "#Maximal excitation-energy for antiparticle-hole-pairs: " 
	    << int(ediffmaxd)
	      << endl;

    if (im_count > 0)
      resfile << "#" << im_count << " imaginary eigenvalues" << endl;
    else
      resfile << "#No imaginary eigenvalues" << endl;

    if (im_count > 0) 
    {
	resfile << "#Listing imaginary eigenvalues:" << endl;
	
	for (i = 1; i <= im_count; i++)
	{
	    resfile << "#Imaginary part: " << erpa_im[i][1] << endl;
	    resfile << "#Real part: " << erpa_im[i][2] << endl;
	}
    }
    resfile << endl;
    
    
    resfile << "#Parameterset: " << txtfor << endl;

    if (natural_parity == 1)
      resfile << "#natural parity: yes" << endl;
    else
      resfile << "#natural parity: no" << endl;
    
    if (ispar == 0)
      resfile << "#Isoscalar result:" << endl;
    else if (ispar == 1)
      resfile << "#Isovector result:" << endl;

    if (ihar == 1)
      resfile << "#Hartree-Solution!!" << endl;
    
    if (calc == 0)
    {
	if (calcfile_found == 1) 
	{	    
	    resfile << "#relevant interaction parameters " 
	      << "from the original calculation:"
		<< endl;
	    resfile << "#calc_j = " << calc_j << endl;
	    resfile << "#calc_parity = " << calc_parity << endl;
	    resfile << "#calc_ediffmaxu = " << calc_ediffmaxu << endl;
	    resfile << "#calc_ediffmaxd = " << calc_ediffmaxd << endl;
	    resfile << "#calc_xyprint = " << calc_xyprint << endl;
	    resfile << "#calc_hartree = " << calc_hartree << endl;
	}
	else 
	{
	    resfile << "#original file calc.out not found" << endl;
	    resfile << "#please makes sure that binary matrices" 
	      << "matching your calculation" << endl;
	    resfile << "#relevant interaction parameters " 
	      << "from file ftes_start.dat"
		<< endl;
	    resfile << "#j = " << j << endl;
	    resfile << "#parity = " << parity << endl;
	    resfile << "#ediffmaxu = " << ediffmaxu << endl;
	    resfile << "#ediffmaxd = " << ediffmaxd << endl;
	    resfile << "#xyprint = " << xyprint << endl;
	    resfile << "#hartree = " << hartree << endl;
	}
    }
    
	
    resfile << endl;
    


}

static char lname(int nn)
{
 
  char lang[]= {'s','p','d','f','g','h','i','j','k','l','m','n',
    'o','\0'};
  char notkn[] = "?";

  if (nn > 11) return notkn[0];
  else return lang[nn];
}




