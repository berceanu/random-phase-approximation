c=====================================================================c

       subroutine plotd(lpr)

c=====================================================================c
C
C     prepares plot of densities in coordinate space
C
c---------------------------------------------------------------------c
      include 'paramet'
c
      implicit real*8 (a-h,o-z)
      character*40 filename
      logical lpr
c
      dimension pn(nox),ri(64,2)
      dimension ppn(164),ppc(164),dd(164,2),dd1(164,2),dd2(164,2)
      dimension vin(64),vinn(64)
c
      common /baspar/ hom,hb0,b0
      common /gaussh/ xh(ngh),wh(ngh),ph(ngh)
      common /mathco/ zero,one,two,half,third,pi
      common /optopt/ icm,icou,it1,it2,ncut
      common /rhorho/ rs(ngh,2),rv(ngh,2),dro(ngh)
      common /tapes / l6,lin,lou,lwin,lwou,lplo
      common /potpot/ vps(ngh,1:2),vms(ngh,1:2)
      common /potvec/ vec(ngh,1:2)
      common /physco/ amu,hqc,alphi,r0
      common /coupl/  gsig(ngh),gome(ngh),grho(ngh)       
      common /fields/ sig(ngh),ome(ngh),rho(ngh),cou(ngh)
      common /gaucor/ rb(ngh),wdcor(ngh)
      common /file/ filename
c
      if (lpr)
     &write(l6,*) ' ****** BEGIN PLOTD ********************************'
c
c
c-------------------------------------------------
c     test:
c     do ih=1,ngh
c        ro = rdens(1,rs(1,1),pn,xh(ih))
c        write(l6,*) 'rs neut',ih,xh(ih)*b0,ro
c     enddo
c     do ih=1,ngh
c        ro = rdens(1,rv(1,1),pn,xh(ih))
c        write(l6,*) 'rv neut',ih,xh(ih)*b0,ro
c     enddo
c-------------------------------------------------
c
c---- number of points for the plot
      mxpl = 128
c
c---- plot step in (fm)
      stpl = 0.1
c
c---- plot for densities:
      open(lplo,file=filename(1:4)//'dens.pn',status='unknown')
      open(54,file=filename(1:4)//'dens.tot',status='unknown')     
      do it = it1,it2
         write(lplo,'(/,a,i3)') ' #scalar density it =',it
         r = zero
         do ist = 0,mxpl
            x  = r/b0
            ro = rdens(1,rs(1,it),pn,x)
            write(lplo,100) r,ro
  100       format(f10.3,f15.6) 
            r = r + stpl
         enddo
         write(lplo,'(/,a,i3)') ' #vector density it =',it
         r = zero
         do ist = 0, mxpl
            x  = r/b0
            ro = rdens(1,rv(1,it),pn,x)
            write(lplo,100) r,ro
            r = r + stpl
         enddo
      enddo
       
      write(54,'(/,a,i3)') ' #total scalar density' 
      r= zero
      do ist = 0, mxpl
         x  = r/b0
         ro1 = rdens(1,rs(1,1),pn,x)
         ro2 = rdens(1,rs(1,2),pn,x)
         write(54,100) r,ro1+ro2      
         r = r + stpl
      enddo
      write(54,'(/,a,i3)') ' #total vector density' 
      r= zero
      do ist = 0,mxpl
         x  = r/b0
         ro1 = rdens(1,rv(1,1),pn,x)
         ro2 = rdens(1,rv(1,2),pn,x)
         write(54,100) r,ro1+ro2      
         r = r + stpl
      enddo
      close(lplo)
      close(54)
c      
c---- plot for potentials
      open(91,file=filename(1:4)//'pot.cen',status='unknown')
      open(92,file=filename(1:4)//'pot.so',status='unknown')
      do it = it1,it2
         write(91,'(/,a,i3)') ' #central potential it =',it
	 write(92,'(/,a,i3)') ' #spin-orbit potential it =',it
         r = zero
         do ist = 0,mxpl
            x  = r/b0
            ro = rdens(1,vps(1,it),pn,x)
	    ro1 = rdens(1,vms(1,it),pn,x)*hqc
	    ro1 = ro1*amu/(amu-0.5*ro1)
            write(91,100) r,ro*hqc
	    write(92,100) r,ro1
	    r=r+stpl
	 enddo
      enddo
      close(91)
      close(92)     
c---- plot for effective masses
      open(91,file=filename(1:4)//'ameff',status='unknown')
      do it = it1,it2
         write(91,'(/,a,i3)') ' #effective mass it =',it
         r = zero
         do ist = 0,mxpl
            x  = r/b0
            ro = rdens(1,vec(1,it),pn,x)*hqc
            ameff = one-ro/amu
            write(91,100) r,ameff
	    r=r+stpl
	 enddo
      enddo       
      close(91)
      
c---- plot for effective masses 2
      open(99,file=filename(1:4)//'ameff2',status='unknown')
      do it = it1,it2
         write(99,'(/,a,i3)') ' #effective mass2 it =',it
         r = zero
         do ist = 0,mxpl
            x  = r/b0
            ro = rdens(1,vms(1,it),pn,x)*hqc
            ameff = one-ro/(2*amu)
            write(99,100) r,ameff
	    r=r+stpl
	 enddo
      enddo       
      close(99)
                        
c
      if (lpr)
     &write(l6,*) ' ****** END PLOTD **********************************'
      return
C-end-PLOT
      end
c======================================================================c
      function cad(h,ix)
ccc coulomb potential
c
      include 'paramet'
c 
      implicit real*8 (a-h,o-z)
      common /baspar/ hom,hb0,b0
      common /gaucor/ rb(ngh),wdcor(ngh)
      common /mathco/ zero,one,two,half,third,pi
      common /physco/ amu,hqc,alphi,r0
      common /rhorho/ rs(ngh,2),rv(ngh,2),dro(ngh) 
c  
      rx = h*ix
      f= one /(6*alphi)
      s = zero
      do kh = 1,ngh
      rg = dmax1(rx,rb(kh))
      rk = dmin1(rx,rb(kh))
      s = s+f*(3*rg+rk**2/rg)*wdcor(kh)*dro(kh)
      enddo
      cad = s
      return
      end
c======================================================================c

      double precision function rdens(is,ro,pn,x)

c======================================================================c
c
c     calculation of the density ro at arbitrary meshpoint x
c     x is given in units of the oscillator lenght: x = r/b0 
c
c     is = 1: density given at Gauss-Meshpoints ro(ih)
c          2: density given through oscillator expansion pn(n)
c
c----------------------------------------------------------------------c
      include 'paramet'
c
      implicit real*8 (a-h,o-z)
c
      dimension ro(ngh),pn(nox),rnr(nox)
C
      common /dimens/ n0f,n0b,nrm,nlm
      common /gaussh/ xh(ngh),wh(ngh),ph(ngh)
      common /gfvsq / sq(0:igfv)
      common /gfvsqi/ sqi(0:igfv)
      common /gfvsqh/ sqh(0:igfv)
      common /gfvshi/ shi(0:igfv)
      common /gfvwgi/ wgi(0:igfv)
      common /mathco/ zero,one,two,half,third,pi
      common /radbos/ rnb(1:nox,ngh)
      common /tapes / l6,lin,lou,lwin,lwou,lplo
c
c
      no = n0b/2 + 1
c
c---- calculation of the oscillator expansion for ro
      if (is.eq.1) then
         do n = 1,no
            s = zero
            do ih = 1,ngh
               s = s + ro(ih)*rnb(n,ih)*wh(ih)*xh(ih)**2
            enddo
            pn(n) = s
         enddo
      endif
c
      xx = x*x
      rnr(1) = 2*wgi(0)*exp(-half*xx)
      rnr(2) = rnr(1)*(1.5d0-xx)*shi(1)
      do n = 3,no
         rnr(n)  = ((2*n-2.5d0-xx)*rnr(n-1) -
     &              sq(n-2)*sqh(n-2)*rnr(n-2))*sqi(n-1)*shi(n-1)
      enddo
c
      s = zero
      do n = 1,no
         s = s + pn(n)*rnr(n)
      enddo
      rdens = s
c
      return
c-end-RDENS
      end
c=====================================================================c

      subroutine plotw(it,ib,k,lpr)

c=====================================================================c
C
C     prepares plot of specific wafefunctions f(r) and g(r)
c     it = 1 for neutrons,  it = 2 for protons
c     ib number of block
c     k  number of specific wavefunction in this block
C
c---------------------------------------------------------------------c
      include 'paramet'
c
      implicit real*8 (a-h,o-z)
      character*40 filename
      logical lpr
c
c
      common /baspar/ hom,hb0,b0
      common /gaussh/ xh(ngh),wh(ngh),ph(ngh)
      common /mathco/ zero,one,two,half,third,pi
      common /optopt/ icm,icou,it1,it2,ncut
      common /tapes / l6,lin,lou,lwin,lwou,lplo
      common /file/ filename
c
c
      if (lpr)
     &write(l6,*) ' ****** BEGIN PLOTW ********************************'
c
c     number of points for the plot
      mxpl = 80
c
c     plot step in (fm)
      stpl = 0.1

c
c     plot for wavefunctions:
c----------------------------
      open(lplo,file=filename(1:4)//'dis.wplo',status='unknown')
      write(lplo,'(a,3i3)') ' #wavefunction f(r)',it,ib,k
      r = zero
      s = zero
      do ist = 0,mxpl
         call rwave(it,ib,k,r,f,g)
         write(lplo,100) r,f
100      format(f10.3,2f15.6) 
         s = s + (f*f+g*g)*r*r
         r = r + stpl
      enddo
      write(l6,*) ' check norm of f and g',s*stpl
      write(lplo,'(a,3i3)') ' #wavefunction g(r)',it,ib,k
      r = zero
      s = zero
      do ist = 0,mxpl
         call rwave(it,ib,k,r,f,g)
         write(lplo,100) r,g
         s = s + (f*f+g*g)*r*r
         r = r + stpl
      enddo
      close(lplo)
c
      if (lpr)
     &write(l6,*) ' ****** END PLOTW **********************************'
      return
C-end-PLOT
      end
c======================================================================c

      subroutine rwave(it,ib,k,r,f,g)

c======================================================================c
c
c     calculation of the wavefunctions f(r) and g(r) at point x
c     x is given in units of the oscillator lenght: x = r/b0 
c     it = 1:  neutron,  it = 2: proton
c     ib is the block charakterized by j,l
c     k  is the number of the wavefunction within this block
c
c----------------------------------------------------------------------c
      include 'paramet'
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
      common /tapes / l6,lin,lou,lwin,lwou,lplo
      common /wavefg/ fg(nq2x,nb2x)
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
      x  = r/b0
      xx = x*x
      f  = b0**(-1.5d0)
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


