#include "common.h"
#include "sla.h"
#include "funk.h"
#include "edmonds.h"


int isospin(int, int, int, int, int);

// calculates the isospin for ph-matrixelement
 

int isospin(int ti, int ti1, int ti2, int ti3, int ti4) {

    int isospinret;
    
    

    switch(ti) 
    {
      case 0:
	isospinret = deltafunk(ti1,ti3)*deltafunk(ti2,ti4);
	break;
	

      case 1:
	isospinret = (2*deltafunk(ti1,ti4)*deltafunk(ti3,ti2))-
	  (deltafunk(ti1,ti3)*deltafunk(ti2,ti4));
	break;
	


      default:
	
	cout << "Falscher Wert fuer isospin()!" << endl;
	cout << "Programm wird beendet!" << endl;
	exit(1);
	

    }
    
//    cout << "isospin = " << isospinret << endl;
    

    return isospinret;
    
}
