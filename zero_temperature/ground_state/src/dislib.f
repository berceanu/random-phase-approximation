c======================================================================c

      subroutine aprint(is,it,ns,ma,n1,n2,a,t1,t2,text)

c======================================================================c
C
C     IS = 1    Full matrix  
C          2    Lower diagonal matrix    
c          3    specially stored symmetric matrix
C 
C     IT = 1    numbers for rows and columns
C          2    text for rows and numbers for columns
C          3    text for rows and columns
C
C     NS = 1     FORMAT  8F8.4      80 Coulums
C     NS = 2     FORMAT  8f8.2      80 Coulums
C     NS = 3     FORMAT 17F4.1      80 Coulums
C     NS = 4     FORMAT 30F4.1     120 Coulums
C     NS = 5     FORMAT  5F12.8     80 Coulums
C     NS = 6     FORMAT  5F12.4     80 Coulums
C     NS = 7     FORMAT  4E13.6     80 Coulums
C     NS = 8     FORMAT  8E15.8    130 Coulums
c
c----------------------------------------------------------------------c
      implicit double precision (a-h,o-z)
C
      character*8 t1(n1),t2(n2)
      character text*(*)
C
      dimension a(ma*n2)
C
      character*30 fmt1,fmt2
      character*20 fti,ftt,fmt(8),fmti(8),fmtt(8)
      dimension nsp(8)
c
      common /tapes / l6,lin,lou,lwin,lwou,lplo,laka,lvpp,lqrpa
c
      data nsp/8,8,17,30,5,5,4,8/
      data fmt /'8f8.4)',            '8F8.2)',
     &          '17f4.1)',           '30f4.1)',
     &          '5f12.8)',           '5f12.4)',
     &          '4e13.6)',           '8e15.8)'/
      data fmti/'(11x,8(i4,4x))',    '(11x,8(i4,4x))',
     &          '(11x,17(1x,i2,1x))','(11x,30(1x,i2,1x))',
     &          '(11x,6(i4,8x))',    '(11x,10(i4,8x))',
     &          '(11x,5(i4,9x))',    '(11x,8(i4,11x))'/
      data fmtt/'(11x,8a8)',         '(11x,8a8)',
     &          '(11x,17a4)',        '(11x,30a4)',
     &          '(11x,6(a8,2x))',    '(11x,10(a8,4x))',
     &          '(11x,5(a8,5x))',    '(11x,8(a8,7x))'/
C
      fmt1   = '(4x,i3,4x,' // fmt(ns)
      fmt2   = '(1x,a8,2x' // fmt(ns)
      fti    = fmti(ns)
      ftt    = fmtt(ns)
      nspalt = nsp(ns)

C
      write(l6,'(//,3x,a)') text
C
      ka = 1
      ke = nspalt
      nteil = n2/nspalt
      if (nteil*nspalt.ne.n2) nteil = nteil + 1
C
      do  10  nt = 1,nteil
      if (n2.gt.nspalt)  write(L6,100)  nt
  100 format(//, 10x,'Part',i5,' of the Matrix',/)
      if(nt.eq.nteil) ke = n2
      if (it.lt.3) then
        write(L6,fti) (k,k=ka,ke)
      else
        write(L6,ftt) (t2(k),k=ka,ke)
      endif
C
      do 20  i=1,n1
         kee=ke
         if (is.ge.2.and.ke.gt.i) kee=i
         if (ka.gt.kee) goto 20
         if (is.eq.3) then
            if (it.eq.1) then
               write(l6,fmt1) i,(a(i+(k-1)*(n1+n1-k)/2),k=ka,kee)
            else
               write(l6,fmt2) t1(i),(a(i+(k-1)*(n1+n1-k)/2),k=ka,kee)
            endif
         else
            if (it.eq.1) then
               write(l6,fmt1) i,(a(i+(k-1)*ma),k=ka,kee)
            else
               write(l6,fmt2) t1(i),(a(i+(k-1)*ma),k=ka,kee)
            endif
         endif
   20 continue
c
      ka=ka+nspalt
      ke=ke+nspalt
   10 continue
C
      return
C-end-APRINT
      end
C=======================================================================

      subroutine gfv

C=======================================================================
C
C     Calculates sign, sqrt, factorials, etc. of integers and half int.
C
c     iv(n)  =  (-1)**n
c     sq(n)  =  sqrt(n)
c     sqi(n) =  1/sqrt(n)
c     sqh(n) =  sqrt(n+1/2)
c     shi(n) =  1/sqrt(n+1/2)
c     fak(n) =  n!
c     fad(n) =  (2*n+1)!!
c     fdi(n) =  1/(2*n+1)!!
c     fi(n)  =  1/n!
c     wf(n)  =  sqrt(n!)
c     wfi(n) =  1/sqrt(n!)
c     wfd(n) =  sqrt((2*n+1)!!)
c     gm2(n) =  gamma(n+1/2)
c     gmi(n) =  1/gamma(n+1/2)
c     wg(n)  =  sqrt(gamma(n+1/2))
c     wgi(n) =  1/sqrt(gamma(n+1/2))
C
C-----------------------------------------------------------------------
      implicit double precision (a-h,o-z)
C
      include 'dis.par'
c
      common /gfviv / iv(0:igfv)
      common /gfvsq / sq(0:igfv)
      common /gfvsqi/ sqi(0:igfv)
      common /gfvsqh/ sqh(0:igfv)
      common /gfvshi/ shi(0:igfv)
      common /gfvfak/ fak(0:igfv)
      common /gfvfad/ fad(0:igfv)
      common /gfvfi / fi(0:igfv)
      common /gfvfdi/ fdi(0:igfv)
      common /gfvwf / wf(0:igfv)
      common /gfvwfi/ wfi(0:igfv)
      common /gfvwfd/ wfd(0:igfv)
      common /gfvgm2/ gm2(0:igfv)
      common /gfvgmi/ gmi(0:igfv)
      common /gfvwg / wg(0:igfv)
      common /gfvwgi/ wgi(0:igfv)
      common /mathco/ zero,one,two,half,third,pi
c
c---- mathemathical constants
      data zero/0.0d0/,one/1.d0/,two/2.d0/
      data half/0.5d0/,third/0.333333333333333333d0/
      data pi/3.141592653589793d0/
C
      third = one/3.d0
      pi = 4*atan(one)
c
      iv(0)  = +1
      sq(0)  =  zero
      sqi(0) =  1.d30
      sqh(0) =  sqrt(half)
      shi(0) =  1/sqh(0)
      fak(0) =  one
      fad(0) =  one
      fi(0)  =  one
      fdi(0) =  one
      wf(0)  =  one
      wfi(0) =  one
      wfd(0)=  one
c     gm2(0) = Gamma(1/2) = sqrt(pi)
      gm2(0) =  sqrt(pi)
      gmi(0) =  1/gm2(0)
      wg(0)  =  sqrt(gm2(0))
      wgi(0) =  1/wg(0)
      do i = 1,igfv
         iv(i)  = -iv(i-1)
         sq(i)  = dsqrt(dfloat(i))
         sqi(i) = one/sq(i)
         sqh(i) = sqrt(i+half)
         shi(i) = one/sqh(i)
         fak(i) = i*fak(i-1)
	 fad(i) = (2*i+1)*fad(i-1)
         fi(i)  = one/fak(i)
         fdi(i) = one/fad(i)
         wf(i)  = sq(i)*wf(i-1)
         wfi(i) = one/wf(i)
	 wfd(i) = sqrt(fad(i))
         gm2(i) = (i-half)*gm2(i-1)
         gmi(i) = one/gm2(i)
         wg(i)  = sqh(i-1)*wg(i-1)
         wgi(i) = one/wg(i)
      enddo
c
c     write(6,*) ' ****** END GFV *************************************' 
      return
c-end-GFV
      end
c======================================================================c
  
      function itestc()
  
c======================================================================c
c
C    yields 1, if interrupted
c           2, if convergence
c
c    the iteration is determined by the parameter XMIX
c    it can be fixed, or automatically adjusted according to
c
c     IAUT = 0 fixed value for XMIX
c          = 1 automatic adjustment of XMIX
c           
c     INXT = 0 with out inputs from the console
c          > 0 after INXT iterations INX and XMIX are read
c
c     INX  = 0 immediate interruption of the iteration
c          > 0 further INX steps with fixed XMIX, which is read  
c          < 0 further ABS(INX) steps with automatic change of XMIX  
c
c----------------------------------------------------------------------c
      implicit real*8 (a-h,o-z)
      integer itestc
c
      common /iterat/ si,siold,epsi,xmix,xmix0,xmax,maxi,ii,inxt,iaut
c
      if (ii.ge.2.and.si.lt.epsi) then
         itestc = 2
         return
      endif
c
c     change of XMIX by reading from the console:
      if (inxt.eq.ii) then
c        write(6,*) 
c     &   'next stop? (0 right now, >0 fixed xmix, <0 autom. xmix)'
c        read(*,*)  inx
c        for running the program without console
         inx=-30
c
         if (inx.eq.0) then
            itestc = 1
            return
         endif
         if (inx.lt.0) then
            iaut = 1
         endif
         if (inx.gt.0) then
            iaut = 0
         endif
         inxt = ii+iabs(inx)
c        write(6,*) 'new value for xmix?'
c        read(*,*) xmix
c        write(6,*) inxt,xmix
         xmix0 = xmix
      endif
c
c     automatic change of XMIX:
      if ((si.lt.siold).and.iaut.eq.1) THEN
         xmix = xmix * 1.04
         if (xmix.gt.xmax) xmix = xmax
      else
         xmix = xmix/1.04                !changes YF.Niu
         if (xmix.lt.0.1) xmix=0.1
      endif
      siold  = si
      itestc = 0
c
      return
c-end-ITESTC
      end 
C=======================================================================
  
      subroutine lingd(ma,mx,n,m,a,x,d,ifl)

C=======================================================================
C
C     solves the system of linear equations A*X = B 
C     at the beginning the matrix B is stored in X
C     during the calculation it will be overwritten
C     D is the determinant of A
C
C-----------------------------------------------------------------------
      implicit real*8 (a-h,o-z)
C
c     solves the system A*X=B, where B is at the beginning on X
c     it will be overwritten lateron, d is the determinant
C
      dimension  a(ma,m),x(mx,m)
C
      data tollim/1.d-10/,one/1.d0/,zero/0.d0/
C
      ifl=1 
      p=zero 
      do 10 i=1,n   
         q=zero         
         do 20 j=1,n
 20      q=q+ abs(a(i,j)) 
         if (q.gt.p)   p=q 
 10   continue         
      tol=tollim*p
      d=one
      do 30 k=1,n     
         p=zero           
         do 40 j=k,n   
            q = abs(a(j,k))
            if (q.lt.p) goto 40
            p=q 
            i=j 
 40      continue          
         if (p.gt.tol) goto 70
         write (6,200) ('-',j=1,80),tol,i,k,a(i,k),('-',j=1,80)
  200    format (/1x,80a1/' *****  ERROR IN LINGD , TOLERANZ =',e10.4,
     1 ' VALUE OF A(',i3,',',i3,') IS ',e10.4/1x,80a1)
         ifl=-1                                         
         return
   70    cp=one/a(i,k)
         if (i.eq.k) goto 90
         d=-d
         do 81 l=1,m
            cq=x(i,l)
            x(i,l)=x(k,l) 
   81       x(k,l)=cq
         do 80 l=k,n
            cq=a(i,l)
            a(i,l)=a(k,l) 
   80       a(k,l)=cq
   90       d=d*a(k,k)
            if (k.eq.n) goto 1
            k1=k+1
            do 120 i=k1,n 
               cq=a(i,k)*cp
               do 106 l=1,m
  106             x(i,l)=x(i,l)-cq*x(k,l) 
               do 120 l=k1,n 
  120             a(i,l)=a(i,l)-cq*a(k,l) 
   30 continue
    1 do 126 l=1,m
  126    x(n,l)=x(n,l)*cp
         if (n.eq.1) return
         n1=n-1
         do 140 k=1,n1 
            cp=one/a(n-k,n-k)
            do 140 l=1,m
               cq=x(n-k,l)
               do 141 i=1,k
  141             cq=cq-a(n-k,n+1-i)*x(n+1-i,l)
  140          x(n-k,l)=cq*cp
c
c
      return
c-end-LINGD
      end 
C=======================================================================

      subroutine nucleus(is,npro,te)

C=======================================================================
C
C     is = 1 determines the symbol for a given proton number npro
c          2 determines the proton number for a given symbol te
c
C-----------------------------------------------------------------------
C
      PARAMETER (MAXZ=129)
C
      CHARACTER TE*2,T*(2*MAXZ+2)
C
      T(  1: 40) = '   HHELIBE B C N O FNENAMGALSI P SCLAR K'
      T( 41: 80) = 'CASCTI VCRMNFECONICUZNGAGEASSEBRCRRBSR Y'
      T( 81:120) = 'ZRNBMOTCRORHPDAGCDINSNSBTE;OXECSBA;ACEPR'
      T(121:160) = 'NDPMSMEUGDTBDYHOERTMYBLUHFTA WREODIRPTAU'
      T(161:200) = 'HGTLPBBIPOATRNFRRAACTHPA UNPPUAMCMBKCFES'
      T(201:240) = 'FMMDNOLRG4G5G6G7G8G9GGX1X2X3X4X5X6X7X8X9'
      T(241:260) = 'XXW1W2W3W4W5W6W7W8W9'
c      T(201:222) = 'FMMDNOLR040506070809GG'
C
      if (is.eq.1) then
         if (npro.lt.0.or.npro.gt.maxz) stop 'in NUCLEUS: npro wrong' 
         te = t(2*npro+1:2*npro+2)
         return
      else
         do np = 0,maxz
            if (te.eq.t(2*np+1:2*np+2)) then
               npro = np
	       if (npro.eq.110) npro = 130
               return
            endif
         enddo
         write(6,100) TE
  100    format(//,' NUCLEUS ',A2,'  UNKNOWN')
      endif
c
      stop
C-END-NUCLEUS
      END
c=======================================================================
  
      subroutine ordi(n,e,mu)
  
c=======================================================================
c     
C     orders a set of numbers according to their size
c
c-----------------------------------------------------------------------
      implicit double precision (a-h,o-z)
C
      dimension e(n),mu(n)
c  
      do 10 i = 1,n
         k  = i 
         p  = e(i)
         if (i.lt.n) then
            do 20 j = i+1,n 
               if (e(j).lt.p) then 
                  k = j 
                  p = e(j)
               endif
   20       continue
            if (k.ne.i) then
               e(k)  = e(i)
               e(i)  = p
               mk    = mu(k)
               mu(k) = mu(i)
               mu(i) = mk
            endif
         endif
   10 continue
c
      return
c-end-ORDI
      end 
c=======================================================================
  
      subroutine ordx(n,e,a1,a2,bb)
  
c=======================================================================
c     
C     orders a set of numbers according to their size
c
c-----------------------------------------------------------------------
      implicit double precision (a-h,o-z)
C
      dimension e(n),a1(n),a2(n),bb(n,n)
c  
      do 10 i = 1,n
         k  = i 
         p  = e(i)
         if (i.lt.n) then
            do 20 j = i+1,n 
               if (e(j).lt.p) then 
                  k = j 
                  p = e(j)
               endif
   20       continue
            if (k.ne.i) then
               e(k)  = e(i)
               e(i)  = p
               x     = a1(k)
               a1(k) = a1(i)
               a1(i) = x
               x     = a2(k)
               a2(k) = a2(i)
               a2(i) = x
               do j = 1,n
                  x       = bb(j,k)
                  bb(j,k) = bb(j,i)
                  bb(j,i) = x
               enddo
            endif
         endif
   10 continue
c
      return
c-end-ORD3
      end 
C=======================================================================
C=======================================================================

      double precision function racslj(K,L1,L2,J2,J1)

C=======================================================================
C
C     Calculates the Racah-coefficient     (  k   l1   l2 )
c                                          ( 1/2  j2   j1 )
c
C     for integer values        k = K, l1 = L1,     l2 = L2
C     and half integer values          j1 = J1-1/2, j2 = J2-1/2
C
C     Method of Edmonds
C
C-----------------------------------------------------------------------
      implicit double precision (a-h,o-z)
c
      include 'dis.par'
c
      common /gfviv / iv(0:igfv)
      common /gfvsq / sq(0:igfv)
      common /gfvsqi/ sqi(0:igfv)
C
      w(i,j,k,l,m,n) = sq(i)*sq(j)*sqi(k)*sqi(l)*sqi(m)*sqi(n) 
c
      racslj = 0.d0
c
      l12m = l1 - l2
      l12p = l1 + l2
      j12m = j1 - j2
      j12p = j1 + j2 - 1
c     check of triangular rule
      if ( (iabs(l12m).gt.k .or. k.gt.l12p) .or.
     &     (iabs(j12m).gt.k .or. k.gt.j12p) ) return
c
      if (j1.eq.l1+1) then
         if (j2.eq.l2+1) then
            racslj = -w(j12p+k+1,j12p-k,2*j1-1,j1,2*j2-1,j2)
         elseif (j2.eq.l2) then
            racslj =  w(k-l12m,k+j12m,2*j1-1,j1,l2,2*l2+1)
         endif
      elseif (j1.eq.l1) then
         if (j2.eq.l2+1) then
            racslj =  w(k+l12m,k-j12m,2*j2-1,j2,l1,2*l1+1)
         elseif (j2.eq.l2) then
            racslj =  w(l12p+k+1,l12p-k,l1,2*l1+1,l2,2*l2+1)
         endif
      endif      
      racslj = iv(l12p+k)*racslj/2
c
      return
c-end-RACSLJ
      end
C=======================================================================

      subroutine sdiag(nmax,n,a,d,x,e,is)

C=======================================================================
C
C     A   matrix to be diagonalized
C     D   eigenvalues    
C     X   eigenvectors
C     E   auxiliary field
C     IS = 1  eigenvalues are ordered and major component of X is positiv
C          0  eigenvalues are not ordered            
C-----------------------------------------------------------------------
      implicit double precision (a-h,o-z)
C
      dimension a(nmax,nmax),x(nmax,nmax),e(n),d(n)
C
      data tol,eps/1.e-32,1.e-10/                           
C
      if (n.eq.1) then
         d(1)=a(1,1)  
         x(1,1)=1.
         return
      endif
c
      do 10 i=1,n 
      do 10 j=1,i 
   10    x(i,j)=a(i,j)
c
ccc   householder-reduktion
      i=n
   15 if (i-2) 200,20,20
   20 l=i-2
      f=x(i,i-1)
      g=f            
      h=0  
      if (l) 31,31,32
   32 do 30 k=1,l
   30 h=h+x(i,k)*x(i,k)
   31 s=h+f*f         
      if (s-tol) 33,34,34              
   33 h=0                             
      goto 100                       
   34 if (h) 100,100,40             
   40 l=l+1                        
      g= dsqrt(s)
      if (f.ge.0.) g=-g        
      h=s-f*g                 
      hi=1.d0/h                
      x(i,i-1)=f-g          
      f=0.0                 
      if (l) 51,51,52     
   52 do 50 j=1,l        
      x(j,i)=x(i,j)*hi  
      s=0.0             
      do 55 k=1,j     
   55 s=s+x(j,k)*x(i,k)                      
      j1=j+1                                
      if (l-j1) 57,58,58                   
   58 do 59 k=j1,l                        
   59 s=s+x(k,j)*x(i,k)                  
   57 e(j)=s*hi                         
   50 f=f+s*x(j,i)                     
   51 f=f*hi*.5d0                      
c                                    
      if (l) 100,100,62             
   62 do 60 j=1,l                  
      s=x(i,j)                    
      e(j)=e(j)-f*s              
      p=e(j)                    
      do 65 k=1,j              
   65 x(j,k)=x(j,k)-s*e(k)-x(i,k)*p        
   60 continue                            
  100 continue                           
      d(i)=h                            
      e(i-1)=g                         
      i=i-1                           
      goto 15            
c            
ccc   Bereitstellen der Transformationmatrix 
  200 d(1)=0.0                               
      e(n)=0.0                              
      b=0.0                                
      f=0.0                               
      do 210 i=1,n                      
      l=i-1                            
      if (d(i).eq.0.) goto 221        
      if (l) 221,221,222             
  222 do 220 j=1,l                  
      s=0.0                         
      do 225 k=1,l                
  225 s=s+x(i,k)*x(k,j)          
      do 226 k=1,l              
  226 x(k,j)=x(k,j)-s*x(k,i)   
  220 continue                
  221 d(i)=x(i,i)            
      x(i,i)=1              
      if (l) 210,210,232   
  232 do 230 j=1,l        
      x(i,j)=0.0          
  230 x(j,i)=0.0         
  210 continue         
c
ccc   Diagonalisieren der Tri-Diagonal-Matrix
      DO 300 L=1,N                     
      h=eps*( abs(d(l))+ abs(e(l)))
      if (h.gt.b) b=h             
c
ccc   Test fuer Splitting        
      do 310 j=l,n              
      if ( abs(e(j)).le.b) goto 320
  310 continue                 
c
ccc   test fuer konvergenz    
  320 if (j.eq.l) goto 300   
  340 p=(d(l+1)-d(l))/(2*e(l))          
      r= dsqrt(p*p+1.d0)
      pr=p+r                           
      if (p.lt.0.) pr=p-r             
      h=d(l)-e(l)/pr                 
      do 350 i=l,n                  
  350 d(i)=d(i)-h                  
      f=f+h                       
c
ccc   QR-transformation          
      p=d(j)                    
      c=1.d0                     
      s=0.0                    
      i=j                    
  360 i=i-1                 
      if (i.lt.l) goto 362 
      g=c*e(i)            
      h=c*p              
      if ( abs(p)- abs(e(i))) 363,364,364
  364 c=e(i)/p                          
      r= dsqrt(c*c+1.d0)
      e(i+1)=s*p*r                     
      s=c/r                           
      c=1.d0/r                         
      goto 365                      
  363 c=p/e(i)                     
      r= dsqrt(c*c+1.d0)
      e(i+1)=s*e(i)*r             
      s=1.d0/r                      
      c=c/r                     
  365 p=c*d(i)-s*g             
      d(i+1)=h+s*(c*g+s*d(i)) 
      do 368 k=1,n           
         h=x(k,i+1)            
         x(k,i+1)=x(k,i)*s+h*c
  368    x(k,i)=x(k,i)*c-h*s 
      goto 360           
  362 e(l)=s*p          
      d(l)=c*p         
      if ( abs(e(l)).gt.b) goto 340
c
ccc   konvergenz      
  300 d(l)=d(l)+f    
c
      if (is.eq.0) return
ccc   ordnen der eigenwerte    
      do 400 i=1,n            
      k=i                    
      p=d(i)                
      j1=i+1               
      if (j1-n) 401,401,400   
  401 do 410 j=j1,n          
      if (d(j).ge.p) goto 410 
      k=j                    
      p=d(j)                
  410 continue             
  420 if (k.eq.i) goto 400
      d(k)=d(i)          
      d(i)=p            
      do 425 j=1,n     
      p=x(j,i)        
      x(j,i)=x(j,k)  
  425 x(j,k)=p      
  400 continue     
c                 
c     signum
      do  71 k=1,n
      s=0.0
      do 72 i=1,n
      h= abs(x(i,k))
      if (h.gt.s) then
         s=h
         im=i
      endif
   72 continue
      if (x(im,k).lt.0.0) then
         do 73 i=1,n
   73    x(i,k)=-x(i,k)
      endiF
   71 continue
c 
      return
c-end-SDIAG
      end 
c======================================================================c

      subroutine spline(x,y,y2,n,yp0,ypn)

c======================================================================c
c
c     SPLINE-Routine of "Numerical Recipies" p.88
c
c input:
c     X,Y       tabulated function (0..N)
c     YP0,YPN   first derivatives at point 0 and N 
c               of the interpolating spline-function
c               (if larger then 1.e30, natural spline: y''= 0)   
c output:
c     Y2        second derivatives of the interpolating function
c               is used as input for function SPLINT
c
c----------------------------------------------------------------------c
      implicit real*8(a-h,o-z)
      parameter (nmax=500)
      dimension x(0:n),y(0:n),y2(0:n),u(0:nmax)
c
      if (nmax.lt.n) stop ' in SPLINE: nmax too small'
      if (yp0.gt.999d30) then
         y2(0) = 0.0
         u(0)  = 0.0
      else
         y2(0) = -0.5d0
         u(0)  = (3.d0/(x(1)-x(0))) * ((y(1)-y(0))/(x(1)-x(0))-yp0)
      endif
      do 11 i = 1,n-1
         sig   = (x(i)-x(i-1))/(x(i+1)-x(i-1))
         p     = sig*y2(i-1) + 2.d0
         y2(i) = (sig - 1.d0)/p
         u(i)  = (6.d0*( (y(i+1)-y(i))/(x(i+1)-x(i)) -
     &                   (y(i)-y(i-1))/(x(i)-x(i-1)) )/
     &                   (x(i+1)-x(i-1)) - sig*u(i-1))/p
   11    continue
      if (ypn.gt..999d30) then
         qn = 0.0
         un = 0.0
      else
         qn = 0.5d0
         un = (3.d0/(x(n)-x(n-1))) * (ypn-(y(n)-y(n-1))/(x(n)-x(n-1)))
      endif
      y2(n) = (un-qn*u(n-1))/(qn*y2(n-1)+1.d0)
      do 12 k = n-1,0,-1
         y2(k) = y2(k)*y2(k+1)+u(k)
   12 continue
c
      return
c-end-SPLINE
      end
c======================================================================c

      subroutine splint(is,xa,ya,y2a,n,x,y,y1,y2)

c======================================================================c
c
c     SPLINT-Routine of "Numerical Recipies" p.89
c
c input:
c     XA,YA     tabulated function (0:N)
c     Y2A       first derivatives (output von SPLINE) 
c     X         given value on the abscissa
c
c output:
c   is = 0:  Y  interpolated value  Y(x)
c   is = 1;  y1 in addition interpolated value of the derivativ dY/dx  
c   is = 2;  y2 in addition interpolated value of 2nd derivativ d2Y/dx2
c  
c----------------------------------------------------------------------c
      implicit real*8(a-h,o-z)
      dimension xa(0:n),ya(0:n),y2a(0:n)
      data sixth/0.1666666666666666667d0/
c
      klo = 0
      khi = n
    1 if (khi-klo.gt.1) then
         k = (khi+klo)/2
         if (xa(k).gt.x) then
            khi = k
         else 
            klo = k
         endif
         goto 1
      endif
      h = xa(khi)-xa(klo)
      if (h.eq.0.0) pause ' in SPINT: bad xa input '
      hi = 1.d0/h
      a  = (xa(khi)-x)*hi
      b  = (x-xa(klo))*hi
c
c     value of the function
      y = a*ya(klo)+b*ya(khi)+
     &    ((a**3-a)*y2a(klo)+(b**3-b)*y2a(khi))*(h**2)*sixth
c 
c     first derivative 
      if (is.lt.1) return
      y1 = hi*(-ya(klo)+ya(khi)) + 
     &    (-(3*a**2-1)*y2a(klo)+(3*b**2-1)*y2a(khi))*h*sixth
c
c     second derivative
      if (is.lt.2) return
      y2 = a*y2a(klo) + b*y2a(khi)
c
      return
c-end-SPLINT
      end
c=======================================================================
c 
      function spur(n,a)
c
c=======================================================================
c 
c     calculates the trace of the matrix A
c
c-----------------------------------------------------------------------
      implicit real*8 (a-h,o-z)
c
      dimension a(n*n)
c
      s = 0.d0
      do i = 1,n
         s = s + a(i+(i-1)*n)
      enddo
      spur = s
c
      return
c-end-SPUR
      end
c=======================================================================

      double precision function talman(n1,l1,n2,l2,n3,l3)

c=======================================================================
c
c     calculates T-coefficients C^{n3 l3}_{n1 l1, n2 l2} 
c     coupling three spherical oscillators
c     as defined in in Eq. (15) of Talman, Nucl. Phys. A141 (1970) 273 
c     and multiplies by c_{n3 l3} as defined in Eq. (7) 
c     and divides it by  sq(2*l1+1)*sq(2*l2+1)*wig(l1,l2,l3,0,0,0)
c
c     the oscillator quantum numbers start with n = 0,1,2,...
c
c-----------------------------------------------------------------------
      include 'dis.par'
c
      implicit real*8 (a-h,o-z)
c
      common /gfviv / iv(0:igfv) 
      common /gfvfad/ fad(0:igfv)
      common /gfvfak/ fak(0:igfv)
      common /gfvfi / fi(0:igfv)
      common /gfvfdi/ fdi(0:igfv)
      common /gfvsqi/ sqi(0:igfv)
      common /gfvwf / wf(0:igfv)
      common /gfvwfd/ wfd(0:igfv)
c
c     pi1 = (pi)**(-3/4)
c     data pi1/0.423777208d0/
c     pi2 = (pi)**(-3/2)
      data pi2/0.179587122125d0/
c
      l123 = (l1 + l2 + l3)/2 
      l    = l123 - l3
      s1 = 0.d0
      do i1 = 0,n1
         s2 = 0.d0
         do i2 = 0,n2
            if (i1+i2+l-n3.ge.0) then
               s2 = s2 + iv(i1+i2)*fad(i1+i2+l123)*
     &                   fi(i1+i2+l-n3)*fak(i1+i2+l)*fi(i2)*
     &                   fi(n2-i2)*fdi(i2+l2)
            endif
         enddo
         s1 = s1 + s2*fi(i1)*fi(n1-i1)*fdi(i1+l1)
      enddo
c
c     multiplication by the wigner-coefficients
c      s1 = s1 * (2*l1+1)*(2*l2+1) * 2**l * wiglll(l1,l2,l3)
c      talman = s1
c
c     multiplication by the factors c_nl
c      cnl1 = pi1*wf(n1)*wfd(n1+l1)*sqi(2*l1+1)*sqi(2)**(n1+l1)
c      cnl2 = pi1*wf(n2)*wfd(n2+l2)*sqi(2*l2+1)*sqi(2)**(n2+l2)
c      talman = talman*cnl1*cnl2
c
c     division by the wigner
c      talman = talman * sqi(2*l1+1)*sqi(2*l2+1)/wiglll(l1,l2,l3)
c 
      talman = s1*pi2*wf(n1)*wf(n2)*sqi(2)**(n1+n2+l3)* 
     &                wfd(n1+l1)*wfd(n2+l2) 
c
      return
c-end-TALMAN
      end
C=======================================================================

      double precision function gintmu(k,n1,n2,smu)

c=======================================================================
c
c     Twofold integral over Gauss function for oscillators.
c     Talman, Nucl.Phys. A141 (1970) 273, Eq. (46)
c
c     smu = mu_i / b0       
c
c     the oscillator quantum numbers start with n = 0,1,2,...
c
c-----------------------------------------------------------------------
      include 'dis.par'
c
      implicit real*8 (a-h,o-z)
c
      common /gfviv / iv(0:igfv)
      common /gfvfad/ fad(0:igfv)
      common /gfvfi / fi(0:igfv)
      common /gfvfdi/ fdi(0:igfv)
      common /gfvsqh/ sqh(0:igfv)
      common /mathco/ zero,one,two,half,third,pi

c
      x  = smu*sqh(0)
c      
       gintmu = 4*pi*(pi*x)**3 * iv(n1+n2) *
c     &         fad(n1+n2+k)/2**(n1+n2) *
     &         fad(n1+n2+k)/2**n1/2**n2 * 
     &         fi(n1)*fi(n2)*fdi(n1+k)*fdi(n2+k) /
     &         (1+x**2)**(n1+n2+k+1.5d0)
c      write(6,*) k,n1,n2,smu,x,gintmu

      return
c-end-GINTMU
      end
C=======================================================================

      double precision function wiglll(l1,l2,l3)

C=======================================================================
C
C     Calculates the Wigner-coefficient    ( l1  l2  l3 )
c                                          (  0   0   0 )
c     for integer values of l1,l2,l3
c
C     Method of Edmonds
C
C-----------------------------------------------------------------------
      implicit double precision (a-h,o-z)
c
      include 'dis.par'
c
      common /gfvfak/ fak(0:igfv)
      common /gfvfi / fi(0:igfv)
      common /gfviv / iv(0:igfv)
      common /gfvwf / wf(0:igfv)
      common /gfvwfi/ wfi(0:igfv)
c
      wiglll = 0.d0
c
      l = l1 + l2 + l3
      if (mod(l,2).ne.0) return
      l12p = l1 + l2
      l12m = l1 - l2
      lh   = l/2
c
c     check of triangular rule
      if (iabs(l12m).gt.l3 .or. l3.gt.l12p) return
c
      wiglll = iv(lh)*wf(l12p-l3)*wf(l12m+l3)*wfi(l+1)*wf(l3-l12m)* 
     &         fak(lh)*fi(lh-l1)*fi(lh-l2)*fi(lh-l3)
c
      return
c-end-WIGLLL
      end
