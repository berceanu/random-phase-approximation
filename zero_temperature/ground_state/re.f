c--------------------------------------------------------------------c
      double precision function dip1(x,a,b,c,d)
 
      implicit double precision (a-h,o-z)        

      dip1 = a*(1+b*(x+d)**2)/(1+c*(x+d)**2)  
      return
      end
c--------------------------------------------------------------------c
      double precision function dip2(x,a,b,c,d)
      
      implicit double precision(a-h,o-z)
      
      dip2 = 1.d0 + a*(x-1) + b*(x-1)**2
      return
      end
c--------------------------------------------------------------------c      
      double precision function dip3(x,a,b,c,d)  
          
      implicit double precision(a-h,o-z)
      
      dip3 = exp(-(x-1)*a)           
      return
      end
c--------------------------------------------------------------------c
      double precision function d_dip1(sat,dsat,x,a,b,c,d)
  
      implicit double precision (a-h,o-z)
      
      fk = a*(2.d0*(x+d)*(b-c))/(1+c*(x+d)**2)**2
      d_dip1 = (sat/dsat)*fk
      return
      end
c--------------------------------------------------------------------c 
      double precision function d_dip2(sat,dsat,x,a,b,c,d)

      implicit double precision(a-h,o-z)
      
      fk = a + 2.d0*b*(x-1.d0)
      d_dip2 = (sat/dsat)*fk
      return
      end 
c--------------------------------------------------------------------c
      double precision function d_dip3(sat,dsat,x,a,b,c,d)

      implicit double precision(a-h,o-z)
      
      fk = (-a)*dip3(x,a,b,c,d)
      d_dip3 = (sat/dsat)*fk
      return
      end           
c--------------------------------------------------------------------c
      double precision function dddip1(sat,dsat,x,a,b,c,d)
  
      implicit double precision (a-h,o-z)
      
      fk = 2.d0*a*(b-c)*(1.d0-3.d0*c*(x+d)**2)/(1+c*(x+d)**2)**3
      dddip1 = (sat/dsat**2)*fk
      return
      end
c--------------------------------------------------------------------c 
      double precision function dddip2(sat,dsat,x,a,b,c,d)

      implicit double precision(a-h,o-z)
      
      fk = 2.d0*b
      dddip2 = (sat/dsat**2)*fk
      return
      end 
c--------------------------------------------------------------------c
      double precision function dddip3(sat,dsat,x,a,b,c,d)

      implicit double precision(a-h,o-z)
      
      fk = (a**2)*dip3(x,a,b,c,d)
      dddip3 = (sat/dsat**2)*fk
      return
      end       
     
