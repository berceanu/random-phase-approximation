c======================================================================c

      double precision function rdens(is,ro,pn,x)

c======================================================================c
c
c     calculation of the density ro at arbitrary meshpoint x
c     x is given in units of the oscillator lenght: x = r/b0f 
c
c     is = 1: density given at Gauss-Meshpoints ro(ih)
c          2: density given through oscillator expansion pn(n)
c
c----------------------------------------------------------------------c
      include 'dis.par'
c
      implicit real*8 (a-h,o-z)
c
      dimension ro(ngh),pn(nox),rnr(nox)
C
      common /baspar/ hom,hb0,b0
      common /dimens/ n0f,n0b,nrm,nlm,nrbm,nb,nt,no
      common /gaussh/ xh(ngh),wh(ngh),ph(ngh)
      common /gfvsq / sq(0:igfv)
      common /gfvsqi/ sqi(0:igfv)
      common /gfvsqh/ sqh(0:igfv)
      common /gfvshi/ shi(0:igfv)
      common /gfvwgi/ wgi(0:igfv)
      common /mathco/ zero,one,two,half,third,pi
      common /radbos/ rnb(1:nox,ngh)
      common /tapes / l6,lin,lou,lwin,lwou,lplo,laka,lvpp,lqrpa
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
