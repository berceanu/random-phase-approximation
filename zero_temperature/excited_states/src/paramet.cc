#include "common.h"
#include "base.h"
#include "sla.h"
#include "funk.h"

void nextequal1(fstream &);
static void write_parameters();
static void write_calc_parameters();
static void read_calc_parameters(fstream &);
static int newline(fstream &);


int j;
int parity;
double ediffmaxu;
double ediffmaxd;
int calc;
int xyprint; 
int lorchange;
double lorswidth;
double lorvwidth;
double hlorswidth;
double hlorvwidth;
int hartree;
int matprint;
int xyread;
int xyprobe;
int exccalc;
int transdens;
int transiso;
double transerg;
int tc_cur;
int tc_iso;
double tc_erg;
double qptresh;
int respair;
int calc_j;
int calc_parity;
double calc_ediffmaxu;
double calc_ediffmaxd;
int calc_calc;
int calc_xyprint; 
int calc_lorchange;
double calc_lorswidth;
double calc_lorvwidth;
double calc_hlorswidth;
double calc_hlorvwidth;
int calc_hartree;

int calcfile_found;


void paramet(char *filename) {


    fstream datenfile;
    fstream calcfile;
    

    datenfile.open(filename, ios::in) ;
    if (!datenfile) {
	cerr << "\n*** Error opening file " << filename << " ***\n";
	cerr << "Execution terminated !" << endl; 
	exit(1);
    }


    nextequal1(datenfile);
    datenfile >> j;

    nextequal1(datenfile);
    datenfile >> parity;
       
    nextequal1(datenfile);
    datenfile >> ediffmaxu;

    nextequal1(datenfile);
    datenfile >> ediffmaxd;

    nextequal1(datenfile);
    datenfile >> calc;
   
    nextequal1(datenfile);
    datenfile >> xyprint;
    
    nextequal1(datenfile);
    datenfile >> lorchange;

    nextequal1(datenfile);
    datenfile >> lorswidth;

    nextequal1(datenfile);
    datenfile >> lorvwidth;
    
    nextequal1(datenfile);
    datenfile >> hlorswidth;

    nextequal1(datenfile);
    datenfile >> hlorvwidth;

    nextequal1(datenfile);
    datenfile >> hartree;
    
    nextequal1(datenfile);
    datenfile >> matprint;    

    nextequal1(datenfile);
    datenfile >> xyread;
    
    nextequal1(datenfile);
    datenfile >> xyprobe;

    nextequal1(datenfile);
    datenfile >> exccalc;

    nextequal1(datenfile);
    datenfile >> transdens;

    nextequal1(datenfile);
    datenfile >> transiso;

    nextequal1(datenfile);
    datenfile >> transerg;

    nextequal1(datenfile);
    datenfile >> tc_cur;

    nextequal1(datenfile);
    datenfile >> tc_iso;

    nextequal1(datenfile);
    datenfile >> tc_erg;
    
    nextequal1(datenfile);
    datenfile >> qptresh;

    nextequal1(datenfile);
    datenfile >> respair;    

    // just for check

    write_parameters();
    
    if (calc == 1)
      write_calc_parameters();
    else 
    {
	calcfile.open("ztes_calc.out", ios::in);
	if (!calcfile) {
	    cout << "there should be a file named calc.out on disk"
	      << endl;
	    cout << "writing a new one" << endl;	    
	    write_calc_parameters(); 
	    calcfile_found = 0;	    
	}
	else 
	{	    
	  read_calc_parameters(calcfile);	  
	  calcfile_found = 1;
      }
	
    }
    

  
}

void write_parameters() 
{
    fstream paramf;
    

    paramf.open("ztes_par.out", ios::out | ios::trunc);

    paramf << "Parameters read from start.dat: " << endl;
    paramf << "j = " << j << endl;    
    paramf << "parity = " << parity << endl;
    paramf << "ediffmaxu = " << ediffmaxu << endl;
    paramf << "ediffmaxd = " << ediffmaxd << endl;
    paramf << "calc = " << calc << endl;
    paramf << "xyprint = " << xyprint << endl; 
    paramf << "lorchange = " << lorchange << endl;
    paramf << "lorswidth = " << lorswidth << endl;
    paramf << "lorvwidth = " << lorvwidth << endl;
    paramf << "hlorswidth = " << hlorswidth << endl;
    paramf << "hlorvwidth = " << hlorvwidth << endl;
    paramf << "hartree = " << hartree << endl;   
    paramf << "xyread = " << xyread << endl;
    paramf << "xyprobe = " << xyprobe << endl;
    paramf << "exccalc = " << exccalc << endl;
    paramf << "transdens = " << transdens << endl;    
    paramf << "transiso = " << transiso << endl;
    paramf << "transerg = " << transerg << endl;
    paramf << "tc_cur = " << tc_cur << endl;
    paramf << "tc_iso = " << tc_iso << endl;
    paramf << "tc_erg = " << tc_erg << endl;

    return;
    
}

void write_calc_parameters() 
{
    fstream calcf;
    
    calcf.open("ztes_calc.out", ios::out | ios::trunc);

    calcf << j << endl;    
    calcf << parity << endl;
    calcf << ediffmaxu << endl;
    calcf << ediffmaxd << endl;
    calcf << xyprint << endl; 
    calcf << hartree << endl;     
    
    return;
    
}


void read_calc_parameters(fstream &calcin) 
{
    int l_count = 0;
    

    calcin >> calc_j;
    l_count += newline(calcin);
    
    calcin >> calc_parity;
    l_count += newline(calcin);

    calcin >> calc_ediffmaxu;
    l_count += newline(calcin);

    calcin >> calc_ediffmaxd;
    l_count += newline(calcin);

    calcin >> calc_xyprint;
    l_count += newline(calcin);

    calcin >> calc_hartree;
    l_count += newline(calcin);

    return;
    
}

void nextequal1(fstream &efile1) {

    int ec;

    while (!0) {

	ec = efile1.get();

	if (ec == EOF) {
	    cerr << "EOF in nextequal1 !" << endl;
	    cerr << "Execution terminated !" << endl;
	    exit(-1);
	}

	else if (ec == '=')
	  break;

    }

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


