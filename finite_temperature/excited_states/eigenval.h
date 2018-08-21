#ifndef _eigenval_h
#define _eigenval_h

class Eigenvalue
{
    
  private:
    
    int n;    
    int issymmetric;    
    double1(d);
    double1(e);    
    double2(V);
    double2(H);
    double1(ort);
    double cdivr;
    double cdivi;
    

    void tred2();
    void tql2();
    void orthes();
    void hqr2();
    double hypot0(double a, double b);
    void cdiv(double xr, double xi, double yr, double yi);


  public:
      
    double** getV();
    double* getRealEigenvalues();
    double* getImagEigenvalues();    
        

    Eigenvalue(double** A, int nn);

    ~Eigenvalue();
    

};


#endif
