c======================================================================c

      subroutine radgh(lpr)

c======================================================================c
c
c     calculates the radial functions for the spherical oscillator
c
c     the wave function phi(nlj) of the spherical oscillator are: 
c
c     phi(r,Omega) = b^(-3/2) * R_nl(r) * Y_ljm(Omega) 
c     
c     R_nl(r) = N_nl * r^l  * L^(l+1/2)_(n-1)(x*x) * exp(-x*x/2)
c
c     N_nl    = sqrt(2 * n!/(n+l+1/2)!)     and    x=r/b
c
c     the contribution to the density from the shell j is
c
c     rho_j(r)= 1/(4*pi*b0**3) * (2*j+1) * R_nl(r)^2
c
c     the radial function at meshpoint xh(ih) is stored in RNL(n,l,ih)
c     in the following way: RNL is normalized in such way that the
c     norm integral reads
c
c     \int d^3r |phi(r)|^2 = 1 = \sum_i RNL(n,l,i)**2
c
c     this means, that RNL contains the following factors:
c
c     a)  the radial part of the wavefunction r * R_nl(r)
c     b)  the length units factor  b ** (3/2)
c     c)  the Gaussian weight sqrt( WH(i) ): 
c         \inf_0^inf f(x) dx = \sum_i f(x_i) * WH(i)
c
c     having RNL(n,l,i) we get the radial wavefunction:
c
c     R_nl(r) =  RNL(n,l,i) / ( x_i * sqrt(WH(i)) )  
c
c     and the density contribution from the shell j
c
c     rho_j(r) = (2*j+1) * RNL(n,l,i)**2 / ( 4 * pi x_i**2 * WH(i) * b**3)   
c
c----------------------------------------------------------------------c
c

c     RNL1 contains the radial derivatives in the following form:
c
c     d/dr R_nl(r) = 1/b * RNL1(n,l,i) / (x_i * sqrt(WH(i) )
c
c----------------------------------------------------------------------c
c
c     RNB(n,i) is the radial function for the expansion of the mesonfields
c     differnently defined form RNL: 
c
c     RNB(n,i) = R_n0(r) 
c
c----------------------------------------------------------------------c
      include 'dis.par'
c
      implicit real*8 (a-h,o-z)
      logical lpr
c
      common /dimens/ n0f,n0b,nrm,nlm
      common /gaussh/ xh(ngh),wh(ngh),ph(ngh)
      common /gfvsq / sq(0:igfv)
      common /gfvsqi/ sqi(0:igfv)
      common /gfvsqh/ sqh(0:igfv)
      common /gfvshi/ shi(0:igfv)
      common /gfvwgi/ wgi(0:igfv)
      common /mathco/ zero,one,two,half,third,pi
      common /radosc/ rnl(1:nrx,0:nlx,ngh),rnl1(1:nrx,0:nlx,ngh)
      common /radbos/ rnb(1:nox,ngh)
      common /tapes / l6,lin,lou,lwin,lwou,lplo
c
      if (lpr)
     &write(l6,*) ' ****** BEGIN RADGH ********************************'
c
      f = 2*wgi(0)
      nbo = n0b/2+1
c
      do 10 ih = 1,ngh
         r  = xh(ih)
         rr = r*r
         ri = 1/r 
         fe = f*exp(-half*rr)
c
c------- basis for fermions
c------------------------------------
c        renormalization for fermions
         u1 = fe*sqrt(wh(ih)*rr)
c------------------------------------
         do l = 0,nlm
            rnl(1,l,ih)  = u1
            rnl(2,l,ih)  = u1*(l+1.5d0-rr)*shi(l+1)
            u1           = u1*r*shi(l+1)
            rnl1(1,l,ih) =    (l-rr)*rnl(1,l,ih)*ri
            rnl1(2,l,ih) = ((2+l-rr)*rnl(2,l,ih) - 
     &                       2*sqh(l+1)*rnl(1,l,ih))*ri
            do n = 3,nrm
               rnl(n,l,ih)  = ((2*n+l-2.5d0-rr)*rnl(n-1,l,ih) -
     &           sq(n-2)*sqh(n-2+l)*rnl(n-2,l,ih))*sqi(n-1)*shi(n-1+l)
               rnl1(n,l,ih) = ((2*n+l-2-rr)*rnl(n,l,ih) -
     &           2*sq(n-1)*sqh(n-1+l)*rnl(n-1,l,ih))*ri
            enddo
         enddo
c
c
c---- basis for bosons
         rnb(1,ih) = fe
         rnb(2,ih) = rnb(1,ih)*(1.5d0-rr)*shi(1)
         do n = 3,nbo
            rnb(n,ih)  = ((2*n-2.5d0-rr)*rnb(n-1,ih) -
     &          sq(n-2)*sqh(n-2)*rnb(n-2,ih))*sqi(n-1)*shi(n-1)
         enddo
c
   10 continue
c
c
c
c
c---- Test of orthogonality
      if (lpr) then
         do 40 l = 0,nlm
            write(l6,'(/,80(1h*))')
            do 41 n = 1,nrm
               write(l6,'(a,2i3)') 
     &         ' Radial function and derivative for n,l =',n,l
               ix = 5
               write(l6,'(5f15.8)') (rnl(n,l,ih),ih=1,ix)
               write(l6,'(5f15.8)') (rnl1(n,l,ih),ih=1,ix)
   41       continue
            do 50 n2 = 1,nrm
            do 50 n1 = n2,nrm 
               s1 = zero
               s2 = zero
               s3 = zero
               sb = zero
               do ih = 1,ngh
                  rr = xh(ih)**2
                  s0 = rnl(n1,l,ih)*rnl(n2,l,ih)
                  s1 = s1 + s0
                  s2 = s2 + rr*s0
                  s3 = s3 + (rnl1(n1,l,ih)*rnl1(n2,l,ih)
     &                       + rnl1(n1,l,ih)*rnl(n2,l,ih)/xh(ih)
     &                       + rnl(n1,l,ih)*rnl1(n2,l,ih)/xh(ih)
     &                       + s0*(1+l*(l+1))/rr)
                  if (l.eq.0) sb = sb + rnb(n1,ih)*rnb(n2,ih)*rr*wh(ih)
               enddo
               write(l6,'(a,2i3,4f12.8)') 
     &                  ' RNL(n,l) test ',n1,n2,s1,s2,s3,sb
   50       continue
   40    continue
         write(l6,'(/,80(1h*))')
      endif
c
      if (lpr)
     &write(l6,*) ' ****** END RADGH **********************************'
      return
c-end-RADGH
      end
