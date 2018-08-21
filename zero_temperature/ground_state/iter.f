c======================================================================c

      subroutine iter(lpr)

c======================================================================c
c
c     main iteration for the spherical Dirac program
c
c----------------------------------------------------------------------c
c
      implicit real*8 (a-h,o-z)
      logical lpr,lprx
c
      common /erwar / ea,rms,qp
      common /iterat/ si,siold,epsi,xmix,xmix0,xmax,maxi,ii,inxt,iaut
      common /mathco/ zero,one,two,half,third,pi
      common /optopt/ icm,icou,it1,it2,ncut
      common /pair  / ga(2),gg(2),del(2),spk(2),spk0(2),dec(2),pwi
      common /tapes / l6,lin,lou,lwin,lwou,lplo,laka,lvpp,lqrpa
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
c            if (l6.ne.6) write(6,'(i3,a,f12.8,2(a,f7.3),a,f5.2)') 
c     &      ite,'. Iteration:  si = ',si,'  E/A = ',ea,'  R = ',rms, 
c     &      '  mix =',xmix
         endif
c
c------- potentials in oscillator space
         call potgh(.true.)
c
c------- loop over neutrons and protons
         do it = it1,it2
c
c---------- calculation of the Dirac-Matrix
            call gamma(it,.true.)
c
c---------- calculation of the pairing field
            call delta(it,.false.)
c
c---------- diagonalization of the Dirac-HFB-Matrix
            call dirhfb(it,.false.,.false.)
c
c---------- calculation of new densities in oscillator basis
            call denssh(it,.false.)
c
c---------- transformation to the canonical basis
c            call canon(it,1)
c
         enddo
c
c
c------- calculation of new densities in r-space
         call densit(.true.)
c
c------- calculation of expectation values
         lprx = mod(ii,10).eq.1
         call expect(lprx)
c
c------- new coupling constants
         call dend1(.true.)
c------- convergence criterion for Delta
         si = zero
         do it = it1,it2
            si = max(si,abs(spk(it)-spk0(it)))
            spk0(it) = spk(it)
         enddo
c        
c------- calculation of new fields
          call field(.true.)
c          do it = it1,it2
c             call delta(it,.false.)
c          enddo
c
c------- check for convergence
         ic = itestc()
         if (ic.eq.1) goto 20
         if (ic.eq.2) goto 30
c
   10 continue
   20 write(l6,101) ii,si
c      if (l6.ne.6) write(6,101) ii,si
      write(*,101) ii,si !add YF.Niu
  101 format(//,1x,68(1h*),/,' *   Iteration interrupted after',i4,
     &             ' steps   si =',f17.10,'  *',/,1x,68(1h*))
      goto 40
c
   30 continue
      write(l6,100) ii,si
c      if (l6.ne.6) write(6,100) ii,si
      write(*,100) ii,si  !add YF.Niu
  100 format(//,1x,68(1h*),/,' *   Iteration converged after',i4,
     &             ' steps   si =',f17.10,'    *',/,1x,68(1h*))
c
   40 write(l6,*) ' ****** END ITER ***********************************'
      return
c-end-ITER
      end
