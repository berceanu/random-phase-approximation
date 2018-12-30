#include "common.h"
#include "base.h"



static int newline(fstream &);

void lorneu(char *filepskal, char *filepvec, 
	    char *filelskal, char *filelvec)
	    
{

    double1(en_pur);
    double1(skal_pur);
    double1(vec_pur);
    int en_pur_count;
    int en_pur_count_temp;
    double en_pur_temp;
    int i;
    int l_skal_count = 0;
    int l_vec_count = 0;


    fstream inskalfile, invecfile;
    fstream lorskal, lorvec;
    

    inskalfile.open(filepskal, ios::in);
    if (!inskalfile) {
	cerr << "\n*** Error opening file " << filepskal << " ***\n";
	cerr << "program is terminating" << endl;
	exit(1);
    }

    invecfile.open(filepvec, ios::in);
    if (!invecfile) {
	cerr << "\n*** Error opening file " << filepvec << " ***\n";
	cerr << "program is terminating" << endl;
	exit(1);
    }
    
    


    inskalfile >> en_pur_count;
    l_skal_count += newline(inskalfile);    
    invecfile >> en_pur_count_temp;
    l_vec_count += newline(invecfile);
    
   

    if (en_pur_count != en_pur_count_temp)
    {
	cout << "number of values in scalar and vector file are different!"
	  << endl;
	cout << "program is terminating" << endl;
	exit(1);
    }

  
    
    double1init(en_pur,en_pur_count);    
    double1init(skal_pur,en_pur_count);
    double1init(vec_pur,en_pur_count);

   
    
    for (i = 1; i <= en_pur_count; i++)
    {
	inskalfile >> en_pur[i] >> skal_pur[i];
	l_skal_count += newline(inskalfile);
	
	invecfile >> en_pur_temp;
	
	if (en_pur_temp != en_pur[i]) 
	{
	    cout << "energies of scalar and vector file dont match!" 
	      << endl;
	    cout << "program is terminating" << endl;
	    exit(1);
	}
	invecfile >> vec_pur[i];
	l_vec_count += newline(invecfile);
    }

   
    




    int cn;
    
    cn = inskalfile.get();
    if (cn != EOF) 
    {	
	cout << "EOF in " << filepskal << " not reached!" << endl;
	cout << "program is terminating" << endl;
	exit(1);
    }
    

    cn = invecfile.get();
    if (cn != EOF) 
    {	
	cout << "EOF in " << filepvec << " not reached!" << endl;
	cout << "program is terminating" << endl;
	exit(1);
    }

  

    

    lorskal.open(filelskal, ios::out | ios::trunc);
    lorskal.setf(ios::scientific);

    lorvec.open(filelvec, ios::out | ios::trunc);
    lorvec.setf(ios::scientific);


    lorskal << "#lorswidth: " << lorswidth << endl;
    lorvec << "#lorvwidth: " << lorvwidth << endl;


   

    double2(xplot);
    double2init(xplot,5000,2);
    double lskalval;
    double lvecval;
    double lgiaival;
    double lgiaialtval;
    double1(gamlor);
    const double xxl = 0.01;
    int xi;    

    double1(xplot_skal_max);
    double1(xplot_vec_max);
    
   
    double1init(xplot_skal_max,2);
    double1init(xplot_vec_max,2);    
    
    double orig_skal_max;
    double orig_vec_max;
    
    orig_skal_max = zero;
    orig_vec_max = zero;
    xplot_skal_max[1] = zero;
    xplot_vec_max[1] = zero;


    double1init(gamlor,2);
    gamlor[1] = lorswidth;
    gamlor[2] = lorvwidth;

    for (i = 1; i <= en_pur_count; i++) 
    {
	if ((en_pur[i] > 3.0) || (j != 1))
	  lskalval = skal_pur[i];
	else
	  lskalval = zero;
	
	lvecval = vec_pur[i];
	
	if(skal_pur[i] > orig_skal_max) orig_skal_max = skal_pur[i];
	if(vec_pur[i] > orig_vec_max) orig_vec_max = vec_pur[i];

	for (xi = 0; xi <= 5000; xi++)
	{
	    xplot[xi][1] += lskalval*1./(pow(xi*xxl-en_pur[i],2.)
					 + (gamlor[1]*gamlor[1]/4.))
	      *(gamlor[1]*gamlor[1]/4.);		
		
	    xplot[xi][2] += lvecval*1./(pow(xi*xxl-en_pur[i],2.)
					+ (gamlor[2]*gamlor[2]/4.))
	      *(gamlor[2]*gamlor[2]/4.);
	
		if (xplot[xi][1] > xplot_skal_max[1]) 
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
	    

    }
	
	
    lorskal << "#maximum value: " << xplot_skal_max[1] << endl;
    lorskal << "#at energy: " << xplot_skal_max[2] << endl;

    lorvec << "#maximum value: " << xplot_vec_max[1] << endl;
    lorvec << "#at energy: " << xplot_vec_max[2] << endl;


   

	
    for (xi = 0; xi <= 5000; xi++)
    {
	lorskal << xi*xxl << "\t" << /*(orig_skal_max/xplot_skal_max[1])*
					 xplot[xi][1] << endl;*/
				     xplot[xi][1] << endl; 
	lorvec << xi*xxl << "\t" << (orig_vec_max/xplot_vec_max[1])*
					 xplot[xi][2] << endl;
    }

   
    

   
  ende:
    
    return;
    

}


   




static int newline(fstream &forf) {

    int cn;
    cn = forf.get();
    if ((cn != '\n') && (cn != EOF)) {
	cout << "Fehler beim Einlesen der Daten!\n";
	cout << "cn" << cn << "Ende" << endl;
	
	exit(1);
    }
    
    return(1);
}


