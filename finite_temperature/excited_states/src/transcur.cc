#include "common.h"
#include "base.h"
#include "sla.h"
#include "funk.h"
#include "edmonds.h"
#include "mesh.h"

#define NRANSI
#define float double
#include "nr.h"


static int lcal(int, int, int);
static double Y_plus_z(int, double);
static double Y_minus_z(int, double);
static double Y_plus_rho(int, double);
static double Y_minus_rho(int, double);
static void write_head(fstream &, int, int);

static double trans_r_cur(int, int, int, int, int, int, int, int, int, 
			  int, int, int, int);
static double Yred1(int ,  int ,  int ); 


void transcur(double *erpa, double **xrpa,
	      double **yrpa, int npair, int j, char *filecur,
	      char * filevel, int hp)
{

    int pairc;
    int energyc;
    int st1, l1, j1;
    int st2, l2, j2;
    int l1g, l2g;    
    int iso;
    int n;
    fstream cur_tot_file;        
    fstream vel_tot_file;
    fstream cur_neutron_file;        
    fstream vel_neutron_file;
    fstream cur_proton_file;        
    fstream vel_proton_file;    
    fstream cursumfile;
    fstream descfile;
    fstream jtotfile;
    int nl1, nl2;
    double xwidth;    
    double strength_1, strength_2, strength_3;

    int imesh;

    double3(tc_neutron);
    double3(tc_proton);
    double3(tc_total); 

    double3(vc_neutron); 
    double3(vc_proton);
    double3(vc_total); 

    double1(theta_mesh);

    int n_theta = 180; 
    //original n_theta=180;

    double1init(theta_mesh,n_theta);
    double h_theta = pi/n_theta;
  //  double h_theta= pi/180;   

    for (n = 0; n <= n_theta; n++)
      theta_mesh[n] = n*h_theta;
    
    double3init(tc_neutron,nmesh-1,n_theta,2);
    double3init(tc_proton,nmesh-1,n_theta,2);
    double3init(tc_total,nmesh-1,n_theta,2);    
    double3init(vc_neutron,nmesh-1,n_theta,2);   
    double3init(vc_proton,nmesh-1,n_theta,2);
    double3init(vc_total,nmesh-1,n_theta,2);    

    double1(j_plus_neutron);
    double1(j_plus_proton);
    double1(j_minus_neutron);
    double1(j_minus_proton);

    double1(j_theta);
    double1(j_r);
    double1(jr_int_theta);
    double1(jr_int_r);
    double a_theta, a_r, a_2;

    double2(ro);
    double2(zz);
    double1(Iarg1_z);
    double1(Iarg1_ro);
    double1(I1_z);
    double1(I1_ro);
    double I2_z, I2_ro;
    double1(jz_theta);
    double1(jro_theta);
    double1(jz_int_r);
    double1(jro_int_r);

    double1(j_plus_total);
    double1(j_minus_total);
    
    double1init(j_theta,n_theta);
    double1init(j_r,n_theta);
    double1init(jr_int_theta,nmesh-1);
    double1init(jr_int_r,nmesh-1);
    
    double2init(ro,nmesh-1,n_theta);
    double2init(zz,nmesh-1,n_theta);
    double1init(Iarg1_z,nmesh-1);
    double1init(Iarg1_ro,nmesh-1);
    double1init(I1_z,n_theta);
    double1init(I1_ro,n_theta);
    double1init(jz_theta,n_theta);
    double1init(jro_theta,n_theta);
    double1init(jz_int_r,nmesh-1);
    double1init(jro_int_r,nmesh-1);
    double a_z, a_ro;

    double1init(j_plus_neutron,nmesh-1);
    double1init(j_plus_proton,nmesh-1);
    double1init(j_minus_neutron,nmesh-1);
    double1init(j_minus_proton,nmesh-1);

    double1init(j_minus_total,nmesh-1);
    double1init(j_plus_total,nmesh-1);
    
    //tamara
    double1(temp1);
    double1(temp2);
    double1init(temp1,nmesh-1);
    double1init(temp2,nmesh-1);
    double x,y,a;
    //tamara
    

    double y_p_z;
    double y_m_z;
    double y_p_rho;
    double y_m_rho;
    double x_theta;
    double vec_max_input;
        
    
    int energy_start;
    
    
    energy_start = 1;
    
    int erp_ok_1;
        
    int erp_ok_2;
        
    int tr_st_ind;
    int tr_st_set = 0;
    
    int i, k, index;

    double dens_max = zero;
    double dens_cut = 1.0;    
    double rdens_max;
    double rmeshorig_cut;
    int nmesh_cut;

    double1(dens0_cuti);
    double dens0_cut;
    
    double1init(dens0_cuti,nmesh);


    // calculating density-cut-off

    for (i = 0; i <= nmesh; i++)
    {
	if (dens0[i] > dens_max)
	  dens_max = dens0[i];
    }
    
    cout << "maximal value of ground-state-density: " << dens_max << endl;
    
    for (i = 0; i <= nmesh; i++)
    {	
 	if (dens0[i] < (dens_max*dens_cut/100.))	    
//	if(rmeshorig[i] > 6.5)
	  break;	
    }

    rmeshorig_cut = rmeshorig[i];
    nmesh_cut = i;

    if (nmesh_cut >= nmesh)
    {
	cout << "something`s wrong with nmesh_cut" << endl;
	cout << "nmesh = " << nmesh << endl;
	cout << "nmesh_cut = " << nmesh_cut << endl;
	cout << "program is terminating" << endl;
	exit(1);
    }
    
            
    cout << "radius-cut-off at " << dens_cut 
      << "% of maximum ground-state-density: " << rmeshorig_cut << endl;
    

    for (i = 1; i <= nmesh_cut; i++) 	
      dens0_cuti[i] = dens0[i]*pow(rmeshorig[i],2.0); 

    dens0_cut = simps(dens0_cuti,nmesh_cut,hmesh)*4.*pi;

    cout << "dens0_cut = " << dens0_cut << endl;
    

    // calculating the derivatives of the wave-functions
    // mesh is only calculated form 1*hmesh to (nmesh-1)*hmesh

    
    // counting of imaginary eigenvalues

    im_count = 0;
    

    for (energyc = energy_start; energyc <= ndim_o_c; energyc++)
    {
	if (c_erpa[energyc] != zero)
	  im_count++;
    }
    double2init(erpa_im,im_count,2);
    
    im_count = 0;    
    for (energyc = energy_start; energyc <= ndim_o_c; energyc++)
    {
	if (c_erpa[energyc] != zero)
	{
	    erpa_im[im_count][1] = erpa[energyc];  
	    erpa_im[im_count][2] = c_erpa[energyc];
	}	
    }

      

    // summing up excitations strengths for valid energies
    for (energyc = energy_start; energyc <= ndim_o_c; energyc++) 
    {

	if (abs0(erpa[energyc]-tc_erg) < 1.e-2)
	{	
	    tr_st_set++;	    
	    tr_st_ind = energyc;
	    break;
	}
    }
    


    if (tr_st_set != 1)
    {
	cout << tr_st_set << " valid energies found!" << endl;
	cout << "exact one matching energy is allowed" << endl;	
	cout << "program is terminating" << endl;
	cout << "Transition-energy in ftes_start.dat = " << tc_erg << endl;
	exit(1);
    }
    
    // no imaginary states
    if ((c_erpa[tr_st_ind] == zero) && (erpa[tr_st_ind] > 0.0))
      erp_ok_1 = 1;
    else
      erp_ok_1 = 0;
     
    if (erp_ok_1 != 1)
    {
	cout << "error in function transcur" << endl;
	cout << "wrong values for matching energy" << endl;
	cout << "index = " << tr_st_ind << endl;	
	cout << "erpa = " << erpa[tr_st_ind] << endl;
	cout << "c_erpa = " << c_erpa[tr_st_ind] << endl;
	cout << "energy should be positive and real" << endl;
	cout << "program is terminating" << endl;
	exit(1);
    }

    cout << "calculating transition-current-stuff for " 
      << erpa[tr_st_ind] << endl;
    
    

    energyc = tr_st_ind;

           	       
    for (pairc = 1; pairc <= npair; pairc++) 
    {    
				    	    
	iso = iph[pairc][3];
		    

	st1 = iph[pairc][1];
	l1 = nl[st1][iso];		  
	j1 = nj[st1][iso];
	l1g = lcal(l1,j1,2);
		  

	st2 = iph[pairc][2];
	l2 = nl[st2][iso];
	j2 = nj[st2][iso];
	l2g = lcal(l2,j2,2);
	
		  		  

	strength_1 =(xrpa[pairc][energyc]
	  -iv[abs0(j)]*yrpa[pairc][energyc]);

		
	for (i = 1; i < nmesh; i++)
	{

	    if (iso == 1) 
	    {	
		{
		j_plus_neutron[i] += trans_r_cur(st1,j1,l1,l1g,iso,
		             st2,j2,l2,l2g,iso,j,i,1)*strength_1;
		j_minus_neutron[i] += trans_r_cur(st1,j1,l1,l1g,iso,
		             st2,j2,l2,l2g,iso,j,i,-1)*strength_1;
                }
	    }
	    else 
	    {
		j_plus_proton[i] += trans_r_cur(st1,j1,l1,l1g,iso,
		             st2,j2,l2,l2g,iso,j,i,1)*strength_1;
		j_minus_proton[i] += trans_r_cur(st1,j1,l1,l1g,iso,
		             st2,j2,l2,l2g,iso,j,i,-1)*strength_1;
	    }
	}
	

    }
    
    // summing up total j_plus and j_minus

    jtotfile.open("ftes_t_jtotal.out", ios::out | ios::trunc);    
    write_head(jtotfile,0,hp);
    jtotfile << "#total j_plus and j_minus for " << erpa[tr_st_ind] << " MeV" 
      << endl;
    jtotfile << "# r \t j_plus \t j_minus" << endl;
    for (i = 1; i < nmesh; i++)
    {
	if (tc_iso == 0)
	{
	    j_plus_total[i] = j_plus_neutron[i] + j_plus_proton[i];
	    j_minus_total[i] = j_minus_neutron[i] + j_minus_proton[i];	    
	}
	else 
	{
	    j_plus_total[i] = j_plus_neutron[i] - j_plus_proton[i];
	    j_minus_total[i] = j_minus_neutron[i] - j_minus_proton[i];
	}
    }
    
    if ((j == 1) && (tc_iso == 0))
    {
        for(i = 1; i < nmesh; i++)
        {
            temp1[i] = j_minus_total[i]*pow(rmeshorig[i],2.0);
	    temp2[i] = dens0[i]*pow(rmeshorig[i],2.0);
        }  
        x = simps(temp1,nmesh,hmesh);
        y = simps(temp2,nmesh,hmesh);
        a = x/y;    
        for(i = 1; i < nmesh; i++)
        {
            j_minus_total[i] = j_minus_total[i] - a*dens0[i];	
        }        
    }
    
    for (i = 1; i < nmesh; i++)
    {
       jtotfile << rmeshorig[i] << "\t" 
	  << j_plus_total[i] << "\t" << j_minus_total[i] << endl;
    }     

    for (k = 0; k <= n_theta; k++)
    {

	x_theta = k*h_theta;	
	y_p_z = Y_plus_z(j,x_theta);
	y_m_z = Y_minus_z(j,x_theta);
	y_p_rho = Y_plus_rho(j,x_theta);
	y_m_rho = Y_minus_rho(j,x_theta);

	for (i = 1; i < nmesh; i++)
	{   
	    tc_neutron[i][k][1] = j_minus_neutron[i]*y_m_z
	      +j_plus_neutron[i]*y_p_z;
	    
	    tc_neutron[i][k][2] = j_minus_neutron[i]*y_m_rho
	      +j_plus_neutron[i]*y_p_rho;

	    tc_proton[i][k][1] = j_minus_proton[i]*y_m_z
	      +j_plus_proton[i]*y_p_z;
	    
	    tc_proton[i][k][2] = j_minus_proton[i]*y_m_rho
	      +j_plus_proton[i]*y_p_rho;


	    
	   
	    if (tc_iso == 0)
	    {
		tc_total[i][k][1] = tc_neutron[i][k][1]
		  +tc_proton[i][k][1];
		tc_total[i][k][2] = tc_neutron[i][k][2]
		  +tc_proton[i][k][2];		

	    }
	    else 
	    {
		tc_total[i][k][1] = tc_neutron[i][k][1]
		  -tc_proton[i][k][1];
		tc_total[i][k][2] = tc_neutron[i][k][2]
		  -tc_proton[i][k][2];
		
	    }
	}
    }

    descfile.open("ftes_t_desc.out", ios::out | ios::trunc);    
    write_head(descfile,0,hp);
    descfile << "#Transitioncurrents for " << erpa[tr_st_ind] << " MeV" 
      << endl;
    descfile << "# z \t rho \t j_z \t j_rho" << endl;

    cur_tot_file.open("ftes_t_cur_tot.out", ios::out | ios::trunc);    
    cur_tot_file.setf(ios::scientific);

    vel_tot_file.open("ftes_t_vel_tot.out", ios::out | ios::trunc);    
    vel_tot_file.setf(ios::scientific);

    cur_neutron_file.open("ftes_t_cur_neutron.out", ios::out | ios::trunc);    
    cur_neutron_file.setf(ios::scientific);
    
    vel_neutron_file.open("ftes_t_vel_neutron.out", ios::out | ios::trunc);    
    vel_neutron_file.setf(ios::scientific);

    
    cur_proton_file.open("ftes_t_cur_proton.out", ios::out | ios::trunc);    
    cur_proton_file.setf(ios::scientific);
    
    vel_proton_file.open("ftes_t_vel_proton.out", ios::out | ios::trunc);    
    vel_proton_file.setf(ios::scientific);



        
    double z_plot;
    double rho_plot;


    double vec_size;
    double vec_size_max;
    

    vec_size_max = zero;

    // calculating velocities

    for (i = 1; i < nmesh; i++) 
    {
	for (k = 0; k <= n_theta; k++)
	{
	    vc_total[i][k][1] = tc_total[i][k][1]/dens0[i];
	    vc_total[i][k][2] = tc_total[i][k][2]/dens0[i];

	    vc_neutron[i][k][1] = tc_neutron[i][k][1]/dens0[i];
	    vc_neutron[i][k][2] = tc_neutron[i][k][2]/dens0[i];

	    vc_proton[i][k][1] = tc_proton[i][k][1]/dens0[i];
	    vc_proton[i][k][2] = tc_proton[i][k][2]/dens0[i];

	}
    }
    
    // vector-fields

    double vel_max;
    double vel_max_val;
    

    vel_max = zero;
    
    int i_max;
    int k_max;
    


    for (k = 0; k <= n_theta; k++)
    {	
	x_theta = k*h_theta;	

	for (i = 1; i <= nmesh_cut; i++)
	{
	    
	    if (abs0(vc_total[i][k][1]) > vel_max) 
	    {		
		vel_max = abs0(vc_total[i][k][1]);
		vel_max_val = vc_total[i][k][1];		
		i_max = i;
		k_max = k;
	    }
	}
    }
    
    cout << "maximum z-velocity: " << vel_max_val << endl;
    cout << "at z = " << rmeshorig[i_max]*cos(k_max*h_theta)
      << " and " <<  "rho = " 
	<< sqrt(rmeshorig[i_max]*rmeshorig[i_max]
		-(rmeshorig[i_max]*cos(k_max*h_theta)
		  *rmeshorig[i_max]*cos(k_max*h_theta)))
	  << endl;
    
    // vector-fields


    vel_max = zero;
        

    for (k = 0; k <= n_theta; k++)
    {	
	x_theta = k*h_theta;	

	for (i = 1; i <= nmesh_cut; i++)
	{
	    
	    if (abs0(vc_neutron[i][k][1]) > vel_max) 
	    {		
		vel_max = abs0(vc_neutron[i][k][1]);
		vel_max_val = vc_neutron[i][k][1];		
		i_max = i;
		k_max = k;
	    }
	    
	 //t   vc_neutron[i][k][1] = vc_neutron[i][k][1] - 
	  //t    vz_sign_neutron*abs0(vz_cm_neutron);

	}
    }
    
    cout << "maximum z-velocity: " << vel_max_val << endl;
    cout << "at z = " << rmeshorig[i_max]*cos(k_max*h_theta)
      << " and " <<  "rho = " 
	<< sqrt(rmeshorig[i_max]*rmeshorig[i_max]
		-(rmeshorig[i_max]*cos(k_max*h_theta)
		  *rmeshorig[i_max]*cos(k_max*h_theta)))
	  << endl;


    // vector-fields


    vel_max = zero;
        

    for (k = 0; k <= n_theta; k++)
    {	
	x_theta = k*h_theta;	

	for (i = 1; i <= nmesh_cut; i++)
	{
	    
	    if (abs0(vc_proton[i][k][1]) > vel_max) 
	    {		
		vel_max = abs0(vc_proton[i][k][1]);
		vel_max_val = vc_proton[i][k][1];		
		i_max = i;
		k_max = k;
	    }
	}
    }
    
    cout << "maximum z-velocity: " << vel_max_val << endl;
    cout << "at z = " << rmeshorig[i_max]*cos(k_max*h_theta)
      << " and " <<  "rho = " 
	<< sqrt(rmeshorig[i_max]*rmeshorig[i_max]
		-(rmeshorig[i_max]*cos(k_max*h_theta)
		  *rmeshorig[i_max]*cos(k_max*h_theta)))
	  << endl;


    vec_size_max = zero;
    

    // normalizing total velocity

    for (k = 0; k <= n_theta; k++)
    {	
	x_theta = k*h_theta;	

	for (i = 1; i <= nmesh_cut; i++)
	{
	
           vec_size = sqrt(vc_total[i][k][1]*vc_total[i][k][1]
        		    +vc_total[i][k][2]*vc_total[i][k][2]);
	   
	    if (vec_size > vec_size_max)
	      vec_size_max = vec_size;
	    	    	    
	}
    }


    // normalizing to 1
    cout << "maximal neutron velocity is "<< vec_size_max << endl;
    cout<< "normalization with maximal neutron velocity" << endl;
    cout<< "Value for normalization (0=automatic with " << vec_size_max << ") ---->";
    cin >> vec_max_input;

    if (vec_max_input !=0) vec_size_max = vec_max_input;

    for (k = 0; k <= n_theta; k++)
    {	
	x_theta = k*h_theta;	
	
	for (i = 1; i <= nmesh_cut; i++)
	{
	    
	    vc_total[i][k][1] /= vec_size_max;
	    vc_total[i][k][2] /= vec_size_max;
	    
	    vc_neutron[i][k][1] /= vec_size_max;
	    vc_neutron[i][k][2] /= vec_size_max;

	    vc_proton[i][k][1] /= vec_size_max;
	    vc_proton[i][k][2] /= vec_size_max;
	    	    
	}
    }
    
    // plotting

    for (k = 0; k <= n_theta; k += 10)
    {	
	x_theta = k*h_theta;	

	for (i = 20; i <= nmesh_cut; i += 10)
	{

	    z_plot = rmeshorig[i]*cos(x_theta);
	    rho_plot = sqrt(rmeshorig[i]*rmeshorig[i]-z_plot*z_plot);

	    if ((sqrt(vc_total[i][k][1]*vc_total[i][k][1]
		     +vc_total[i][k][2]*vc_total[i][k][2]) > 0.0005)&&
		     rmeshorig[i]<8.0)
	    {		
		vel_tot_file << rho_plot << " " << z_plot << " " 
		  << vc_total[i][k][2] << " " 
		    << vc_total[i][k][1] << endl;
	    
		vel_neutron_file << rho_plot << " " << z_plot << " " 
		  << vc_neutron[i][k][2] << " " 
		    << vc_neutron[i][k][1] << endl;

		vel_proton_file << rho_plot << " " << z_plot << " " 
		  << vc_proton[i][k][2] << " " 
		    << vc_proton[i][k][1] << endl;
	    }
	    
	}
	
    }
    

    // searching for maximum
    
    vec_size_max = zero;
    
    for (k = 0; k <= n_theta; k++)
    {	
	x_theta = k*h_theta;	

	for (i = 1; i <= nmesh_cut; i++)
	{
	    vec_size = sqrt(tc_total[i][k][1]*tc_total[i][k][1]
			    +tc_total[i][k][2]*tc_total[i][k][2]);
	    
	    if (vec_size > vec_size_max)
	      vec_size_max = vec_size;
	    	    	    
	}
    }

     // normalizing to 1

    for (k = 0; k <= n_theta; k++)
    {	
	x_theta = k*h_theta;	
	
	for (i = 1; i <= nmesh_cut; i++)
	{
	    
	    tc_total[i][k][1] /= vec_size_max;
	    tc_total[i][k][2] /= vec_size_max;

	    tc_neutron[i][k][1] /= vec_size_max;
	    tc_neutron[i][k][2] /= vec_size_max;
	    
	    tc_proton[i][k][1] /= vec_size_max;
	    tc_proton[i][k][2] /= vec_size_max;

	    	    
	}
    }
     
// plotting
   
    for (k = 0; k <= n_theta; k+=4)
    {	
	x_theta = k*h_theta;	

	for (i = 20; i <= 161; i += 6)
	{
         
	    z_plot = rmeshorig[i]*cos(x_theta);
	    rho_plot = sqrt(rmeshorig[i]*rmeshorig[i]-z_plot*z_plot);

	    if (sqrt(tc_total[i][k][1]*tc_total[i][k][1]
		     +tc_total[i][k][2]*tc_total[i][k][2]) > 0.0005)
		     
	    {		
		cur_tot_file << rho_plot << " " << z_plot << " " 
		  << tc_total[i][k][2] << " " 
		    << tc_total[i][k][1] << endl;
		
		cur_neutron_file << rho_plot << " " << z_plot << " " 
		  << tc_neutron[i][k][2] << " " 
		    << tc_neutron[i][k][1] << endl;

		cur_proton_file << rho_plot << " " << z_plot << " " 
		  << tc_proton[i][k][2] << " " 
		    << tc_proton[i][k][1] << endl;
	    }
	}
    }
    

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
    
    resfile << "#Parameterset: " << txtfor << endl;

    if (natural_parity == 1)
      resfile << "#natural parity: yes" << endl;
    else
      resfile << "#natural parity: no" << endl;
    
    if (ispar == 0)
      resfile << "#Isoscalar transition:" << endl;
    else if (ispar == 1)
      resfile << "#Isovector transition:" << endl;

       
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
    
}

static double Y_plus_z(int l, double x) 
{

    double y_ret;
    
    y_ret = -sqrt((l+1.)/(4.*pi))*plgndr(l+1,0,cos(x));
    
    return y_ret;
    
}

static double Y_minus_z(int l, double x) 
{

    double y_ret=0;
    if (l==0)
        return y_ret;
    
    y_ret = sqrt((l)/(4.*pi))*plgndr(l-1,0,cos(x));
    
    return y_ret;
    
}

static double Y_plus_rho(int l, double x) 
{

    double y_ret;
    
    //    y_ret = -sqrt((l+1.)/(4*pi))*plgndr(l+1,1,cos(x))/(l+1.);
    // different convention for P_lm: (-)^m
    y_ret = sqrt((l+1.)/(4*pi))*plgndr(l+1,1,cos(x))/(l+1.);
    
    return y_ret;
    
}

static double Y_minus_rho(int l, double x) 
{

    double y_ret;
    
    if ((l-1) < 1)
      return zero;
    
    // y_ret = -sqrt((l)/(4*pi))*plgndr(l-1,1,cos(x))/l;
    // different convention for P_lm: (-)^m
    y_ret = sqrt((l)/(4*pi))*plgndr(l-1,1,cos(x))/l;
    return y_ret;
    
}




static double trans_r_cur(int st1, int j1, int l1, int l1g, int t1,
			  int st2, int j2, int l2, int l2g, int t2, int j,
			  int m_index, int jsig) 
{

    double trans_r_cur_ret=0;
    int jmax,i;
    double fac1,fac2,fac3,fac4;

    if ((jsig != 1) && (jsig != -1))
    {
	cout << "error in trans_cur" << endl;
	cout << "jsig must be +1 or -1" << endl;
	cout << "jsig = " << jsig << endl;	
	cout << "program is terminating" << endl;
	exit(1);
    }
    if ((m_index <= 0) || (m_index >= nmesh))
    {
	cout << "error in trans_cur" << endl;
	cout << "m_index must be > 0  and < " << nmesh << endl;
	cout << "m_index = " << m_index << endl;	
	cout << "program is terminating" << endl;
	exit(1);
    }
    fac2 = sqrt(2*j1)*sqrt(2*j2)*sqrt(2*j+1)*sqrt(6.0);
            	    	    
    if (jsig == -1)
    {
        if (j == 0 )
	   return trans_r_cur_ret;
        fac3 = s9jslj(1,l1,l2g,j-1,j1,j2,j)*Yred1(l1,l2g,j-1)*
	       wfg[st1][m_index][t1]*wfg[st2][m_index+nmesh][t2];
	fac4 = s9jslj(1,l1g,l2,j-1,j1,j2,j)*Yred1(l1g,l2,j-1)*
	       wfg[st1][m_index+nmesh][t1]*wfg[st2][m_index][t2];
    } 
    else
    {
        fac3 = s9jslj(1,l1,l2g,j+1,j1,j2,j)*Yred1(l1,l2g,j+1)*
	       wfg[st1][m_index][t1]*wfg[st2][m_index+nmesh][t2];
	fac4 = s9jslj(1,l1g,l2,j+1,j1,j2,j)*Yred1(l1g,l2,j+1)*
	       wfg[st1][m_index+nmesh][t1]*wfg[st2][m_index][t2];
    } 
    trans_r_cur_ret = fac2*(fac3-fac4);

    return trans_r_cur_ret;
    

}

static double Yred1(int l1,  int l2,  int j) 
{

    double yred_ret1=0.0;
    
    if ((j > (l1+l2)) ||(j < abs0(l1-l2))) 
      return yred_ret1;
    yred_ret1 = iv[abs0(l1)]*sqrt(2*l1+1)*sqrt(2*l2+1)*sqrt(2*j+1)
               *wigner(l1,j,l2,0,0,0)/sqrt(4*pi);
    return yred_ret1;
}










