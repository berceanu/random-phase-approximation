c=====================================================================c

      subroutine plotwf(lpr)

c=====================================================================c
C
C     prepares plot of specific wafefunctions f(r) and g(r)
c     in the canonical basis
c     it = 1 for neutrons,  it = 2 for protons
c     j  = j+1/2
c     ip = 1 for positive,  ip = 2 for negative parity
c     k  = number of the wavefunction in the j-parity block
c
c---------------------------------------------------------------------c
      include 'dis.par'
c
      implicit real*8 (a-h,o-z)
      logical lpr
      character tp*1,tl*1,tis*1,nucnam*2,tb*8,tit*8,txtfor*10,txb*25
c
      common /baspar/ hom,hb0,b0
      common /bloblo/ nb,ijb(nbx),ilb(nbx),
     &                id(nbx),idq(nbx),ia(nbx),iaq(nbx)
      common /eeeeee/ eqp(ntx,2),ee(ntx,2),v2(ntx,2),mu(ntx)
      common /gaussh/ xh(ngh),wh(ngh),ph(ngh)
      common /mathco/ zero,one,two,half,third,pi
      common /optopt/ icm,icou,it1,it2,ncut
      common /tapes / l6,lin,lou,lwin,lwou,lplo,laka,lvpp,lqrpa
      common /textex/ nucnam,tp(2),tis(2),tit(2),tl(0:20),txtfor
      common /texblo/ tb(ntx),txb(nbx)
c
c
      if (lpr)
     &write(l6,*) ' ****** BEGIN PLOTW ********************************'
c
c
c      do ib = 1,nbx
c	 if (j.eq.ijb(ib).and.mod(ip+ilb(ib),2).eq.1) goto 111
c      enddo 
c      stop 'in PLOTW: wrong quantum numbers'
c
c     number of points for the plot
      mxpl = 300
c
c     plot step in (fm)
      stpl = 0.05

c
c     plot for wavefunctions:
c----------------------------
c      k0 = ia(ib) + k
c      open(lplo,file='dish_' //'dis.wplo',status='unknown')
c         write(lplo,101) ' wavefunction f(r)',
c     &                   tit(it),txb(ip),k,v2(k0,it)
c  101    format(a,a,a,' n =',i3,f15.3)
c         if (lpr) then
c            write(l6,101) ' wavefunction f(r) ',
c     &                   tit(it),txb(ip),k,v2(k0,it)
c         endif
c         r = zero
c         s = zero
c         do ist = 0,mxpl
c            call rwave(it,ib,k,r,f,g)
c            write(lplo,100) r,f
 100  format(f10.3,2f15.6) 
c            if (lpr) write(l6,100) r,f 
c            s = s + (f*f+g*g)*r*r
c            r = r + stpl
c         enddo
c         write(6,*) ' check norm of f and g',s*stpl
c         write(l6,*) ' check norm of f and g',s*stpl
c
c         write(lplo,101) ' wavefunction g(r)',
c     &                   tit(it),txb(ip),k,v2(k0,it)
c         if (lpr) then
c            write(l6,101) ' wavefunction g(r) ',
c     &                   tit(it),txb(ip),k,v2(k0,it)
c         endif
c         r = zero
c         s = zero
c         do ist = 0,mxpl
c            call rwave(it,ib,k,r,f,g)
c            write(lplo,100) r,g
c           if (lpr) write(l6,100) r,f,g 
c            if (lpr) write(l6,100) r,g 
c            s = s + (f*f+g*g)*r*r
c            r = r + stpl
c         enddo
c         write(6,*) ' check norm of f and g',s*stpl
c         write(l6,*) ' check norm of f and g',s*stpl
c      close(lplo)
c
c-------- print wave functions to unit 45
c
                 
        do it = 1, 2
         do ib = 1,nb
           nf  = id(ib)
               if(mod(ilb(ib),2).eq.1) then 
                  ip =2 
                    else
                   ip=1 
                  endif
             do k=1,nf
               k0 = ia(ib) + k
                 if(v2(k0,it).gt.0.0001) then
        WRITE(45,1000)
c        WRITE(45,1002) tb(it), nf , ee(k0,it), v2(k0,it) 
      WRITE(45,1002)tis(it), tb(k0),tp(ip),ijb(ib) , ee(k0,it), 
     &          v2(k0,it)
      WRITE(45,1005)
      write(6,1002) tis(it), tb(k0),tp(ip),ijb(ib) , ee(k0,it), 
     &           v2(k0,it) 
c
         r = zero
          do ist = 0,mxpl
            call rwaves(it,ib,k,r,f,g)
             write(45,1010) r,f,g
              r= r + stpl 
                enddo        
                 endif
               enddo
              enddo 
             enddo
 1000 FORMAT(//,'  State          kappa     eigenvalue      v^2')
 1002 FORMAT(' '''A1,A8,'''',3X,A1,I1,4X,2F12.5)
 1005 FORMAT(/,'      X(fm)',5X,'           G ',12X,'       F')
C
 1010 FORMAT(' ',F12.6,5X,1PE16.8,5X,1PE16.8)




      if (lpr)
     &write(l6,*) ' ****** END PLOTW **********************************'
      return
C-end-PLOT
      end
c======================================================================c

      subroutine rwaves(it,ib,k,r,f,g)

c======================================================================c
c
c     calculation of the wavefunctions f(r) and g(r) at point x
c     in the canonical basis
c     x is given in units of the oscillator lenght: x = r/b0f 
c     it = 1:  neutron,  it = 2: proton
c     j  = j+1/2
c     ip = 1:  positive  it = 2: negative parity
c     k  = number of the wavefunction in the j-parity block
c
c----------------------------------------------------------------------c
      include 'dis.par'
c
      implicit real*8 (a-h,o-z)
c
      dimension rnl(nrx,2)
C
      common /baspar/ hom,hb0,b0
      common /bloblo/ nb,ijb(nbx),ilb(nbx),
     &                id(nbx),idq(nbx),ia(nbx),iaq(nbx)
      common /dimens/ n0f,n0b,nrm,nlm
      common /gfvsq / sq(0:igfv)
      common /gfvsqi/ sqi(0:igfv)
      common /gfvsqh/ sqh(0:igfv)
      common /gfvshi/ shi(0:igfv)
      common /gfvwgi/ wgi(0:igfv)
      common /mathco/ zero,one,two,half,third,pi
      common /tapes / l6,lin,lou,lwin,lwou,lplo,laka,lvpp,lqrpa
      common /canonw/ fg(nhqx,nb2x)
c
      if (r.eq.zero) r = 0.0000001
      ibg = ib - 1 + 2*mod(ib,2)
      nf  = id(ib)
      ng  = id(ibg)
      nd  = nf + ng
      mf  = ib + (it-1)*nbx
      lf  = ilb(ib)
      lg  = ilb(ibg)
c
      x  = r/b0f
      xx = x*x
      f  = b0f**(-1.5d0)
      rnl(1,1) = sq(2)*f*wgi(lf+1)*x**lf*exp(-half*xx)
      rnl(2,1) = rnl(1,1)*(lf+1.5d0-xx)*shi(lf+1)
      rnl(1,2) = sq(2)*f*wgi(lg+1)*x**lg*exp(-half*xx)
      rnl(2,2) = rnl(1,2)*(lg+1.5d0-xx)*shi(lg+1)
      do n = 3,nrm
         rnl(n,1)  = ((2*n+lf-2.5d0-xx)*rnl(n-1,1) -
     &           sq(n-2)*sqh(n-2+lf)*rnl(n-2,1))*sqi(n-1)*shi(n-1+lf)
         rnl(n,2)  = ((2*n+lg-2.5d0-xx)*rnl(n-1,2) -
     &           sq(n-2)*sqh(n-2+lg)*rnl(n-2,2))*sqi(n-1)*shi(n-1+lg)
      enddo
c
      sf = zero
      sg = zero
      do n = 1,nf
         sf = sf + fg(n+(k-1)*nd,mf)*rnl(n,1)
      enddo
      do n = 1,ng
         sg = sg + fg(nf+n+(k-1)*nd,mf)*rnl(n,2)
      enddo
      f = sf
      g = sg
c
      return
c-end-RWAVE
      end

