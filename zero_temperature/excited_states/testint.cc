#include "common.h"
#include "base.h"
#include "sla.h"
#include "funk.h"
#include "edmonds.h"
#include "mesh.h"



void testint() 
{
    

    
    fstream testfile;


    // variables for test-purposes
    
    double1(fgtest);

    double normret = zero;
    double normretneu = zero;    
    double normrenorm = zero;
    double maxerror = zero;
    double temperror = zero;
    double maxerrorneu = zero;
    double temperrorneu = zero;
    
    int index;
    int n, m, l, k;
    int zaehl;
    


    // just a test for norm of wavefunction

    testfile.open("normtest.out", ios::out | ios::app);

   
    // correcting norm (1: yes, 0:no)
    int correctnorm = 0;
    

// printing common mesh

/*

    for (n = 1; n <= nfe; n++) 
    {
	testfile << "FE Nummer: " << n << endl;
	
	for (m = 1; m <= point[n]; m++)
	{
	    testfile << m << "\t" << rmesh[mapin[n][m]] << endl;
	}
	
	if (n < nfe) 
	{	    
	    testfile << "aeusserer Punkt: " << rmesh[mapex[n]] << endl;
	} 

    }
    

    exit(0);
    
*/
    


    for (n = 1; n <= 2; n++) 
    {
	for (m = 1; m <= ntpar[n]; m++) 
	{
	    normret = zero;
	    zaehl = 0;
	    normretneu = zero;
	    
	    
	    for (l = 1; l <= nfe; l++)
	    {
		for (k = 1; k <= point[l]; k++)
		{	
		    index = mapin[l][k];
		    	    
		    normret += (wfgauss[m][index][n]*wfgauss[m][index][n]
				+wfgauss[m][index+nmixmesh][n]
				*wfgauss[m][index+nmixmesh][n])
		      *rmeshin[l][k]*rmeshin[l][k]*wlin[l][k];
		    		    
		}

	    }


	    if (correctnorm == 1)
	    {
					    
		// renormalization of the wavefunctions on the totalmesh

		cout << "correcting norm on gaussian wavefunctions" << endl;
		
		normrenorm = sqrt(normret);
		
		
		for (l = 1; l <= nmixmesh; l++) 
		{
		    wfgauss[m][l][n] /= normrenorm;
		    wfgauss[m][l+nmixmesh][n] /= normrenorm;
		}
	    }   
	    

	    temperror = abs0(one-normret);
	    if (temperror > maxerror)
	      maxerror = temperror;
	    

	}
    }

    cout << "maximum error with" << 
      " original normalization in gaussian integration: " 
	<< maxerror << endl;
    
    testfile << "maximum error with" << 
      " original normalization in gaussian integration: " 
	<< maxerror << endl;


    if (correctnorm == 1) 
    {
		
	
	// norm-test after renormalization

	maxerror = zero;
	temperror = zero;
    

	for (n = 1; n <= 2; n++) 
	{
	    for (m = 1; m <= ntpar[n]; m++) 
	    {
		normret = zero;
		zaehl = 0;
	    
	    
		for (l = 1; l <= nfe; l++)
		{
		    for (k = 1; k <= point[l]; k++)
		    {	
			index = mapin[l][k];
		    	    
			normret += (wfgauss[m][index][n]*wfgauss[m][index][n]
				    +wfgauss[m][index+nmixmesh][n]
				    *wfgauss[m][index+nmixmesh][n])
			  *rmeshin[l][k]*rmeshin[l][k]*wlin[l][k];
		    		    
		    }
		
		}

		temperror = abs0(one-normret);
		if (temperror > maxerror)
		  maxerror = temperror;
	    

	    }
	}

	cout << "maximum error after corrected normalization " 
	  << "in gaussian integration: " 
	  << maxerror << endl;

	testfile << "maximum error after corrected normalization " 
	  << "in gaussian integration: " 
	  << maxerror << endl;


    }
    

    testfile.close();
    

}
