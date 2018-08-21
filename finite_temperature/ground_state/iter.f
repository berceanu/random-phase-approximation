c======================================================================c

      subroutine iter(lpr)

c======================================================================c
c
c     main iteration for the spherical Dirac program
c
c----------------------------------------------------------------------c
c
      implicit real*8 (a-h,o-z)
      logical lpr
c
      common /erwar / ea,rms,qp
      common /optopt/ icm,icou,it1,it2,ncut
      common /iterat/ si,siold,epsi,xmix,xmix0,xmax,maxi,ii,inxt,iaut
      common /tapes / l6,lin,lou,lwin,lwou,lplo
      common /iteracija/ ite
c
      write(l6,*) ' ****** BEGIN ITER *********************************'
c
      do 10 ite = 1,maxi
         ii = ite
c
         if (lpr) then
            write(l6,'(i3,a,f12.8,2(a,f7.3),a,f5.2)') 
     &      ii,'.Iteration:  si = ',
     &      si,'  E/A = ',ea,'  R = ',rms,'  mix =',xmix  
            if (l6.ne.6) write(6,'(i3,a,f12.8,2(a,f7.3),a,f5.2)') 
     &      ite,'. Iteration:  si = ',si,'  E/A = ',ea,'  R = ',rms, 
     &      '  mix =',xmix
         endif
c
c------- potentials in oscillator space
         call potgh(.true.)
c
c------- diagonalization of Dirac equation in the oscillatorbasis
         call dirac(.false.) 
c
c------- fermi level
         call occup(4,.true.)

c------- calculation of new densities in oscillator basis
         call denssh(.true.)
c
c------- calculation of new densities in r-space
         call densit(.true.)

c------- calculation of expectation values 
          if (mod(ii,10).eq.1) then 
           call expect(.false.)
          else
             call expect(.false.)
          endif
c------- new coupling constants
         call dend1(.false.)
c------- calculation of new fields
         call field(.true.)
c
c------- check for convergence
         ic = itestc()
         if (ic.eq.1) goto 20
         if (ic.eq.2) goto 30
c
   10 continue
   20 write(l6,101) ii,si
      if (l6.ne.6) write(6,101) ii,si
  101 format(//,1x,68(1h*),/,' *   Iteration interrupted after',i4,
     &             ' steps   si =',f17.10,'  *',/,1x,68(1h*))
      goto 40
c
   30 continue
      write(l6,100) ii,si
      if (l6.ne.6) write(6,100) ii,si
  100 format(//,1x,68(1h*),/,' *   Iteration converged after',i4,
     &             ' steps   si =',f17.10,'    *',/,1x,68(1h*))
c
   40 write(l6,*) ' ****** END ITER ***********************************'
      return
c-end-ITER
      end
