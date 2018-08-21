c======================================================================c

      subroutine osc(n,l,x,rnl)

c======================================================================c
c
c     calculates the radial functions for the spherical oscillator
c
c     the wave function R_nl(r) of the spherical oscillator are: 
c
c     phi(r,Omega) = b^(-3/2) * R_nl(r) * Y_ljm(Omega) 
c     
c     R_nl(r) = N_nl * r**l * L^(l+1/2)_(n-1)(x*x) * exp(-x*x/2)
c
c     N_nl    = sqrt(2 * (n-1)!/(n+l-1/2)!)     and    x=r/b
c
c     R_nl is normalized in such way that the norm integral reads
c
c     \int dr r**2 R_nl(r)^2 = 1 
c
c----------------------------------------------------------------------c
c
      include 'paramet'
c
      implicit real*8 (a-h,o-z)
c
      dimension rnl(n)
c
      common /gfvsq / sq(0:igfv)
      common /gfvsqi/ sqi(0:igfv)
      common /gfvsqh/ sqh(0:igfv)
      common /gfvshi/ shi(0:igfv)
      common /gfvwgi/ wgi(0:igfv)
      common /mathco/ zero,one,two,half,third,pi
c      common /tapes / l6,lin,lou,lwin,lwou,lplo,laka,lvpp,lrpa
c
      xx = x*x 
      if (l.eq.0) then
	 xl = one
      else
	 xl = x**l
      endif
      rnl(1) = sq(2)*wgi(l+1)*exp(-half*xx)*xl
      rnl(2) = rnl(1)*(l+1.5d0-xx)*shi(l+1)
      do i = 3,n
         rnl(i) = ((2*i+l-2.5d0-xx)*rnl(i-1) -
     &             sq(i-2)*sqh(i-2+l)*rnl(i-2))*sqi(i-1)*shi(i-1+l)
      enddo
c
      return
c-end-OSC
      end
