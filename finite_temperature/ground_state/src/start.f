c======================================================================c

      subroutine start(lpr)

c======================================================================c
c
c     initializes potentials
c     inin = 0:   reads fields from tape lwin
c            1:   uses default fields
c            2:   saxon-woods
c            3:   oscillator
c
c----------------------------------------------------------------------c
c
      include 'paramet'
c
      implicit real*8 (a-h,o-z)
      logical lpr
c
      common /baspar/ hom,hb0,b0
      common /gaussh/ xh(ngh),wh(ngh),ph(ngh)
      common /fields/ sig(ngh),ome(ngh),rho(ngh),cou(ngh)
      common /initia/ vin,rin,ain,inin
      common /mathco/ zero,one,two,half,third,pi
      common /mespar/ amsig,amome,amrho,gsigs,gomes,grhos
      common /nucnuc/ amas,nama,npr(2),jmax
      common /optopt/ icm,icou,it1,it2,ncut
      common /physco/ amu,hqc,alphi,r0
      common /potpot/ ss(ngh,1:2),vv(ngh,1:2),vps1(ngh,1:2),
     &			vms1(ngh,1:2)
      common /tapes / l6,lin,lou,lwin,lwou,lplo
      common /woodsa/ v0,akv,vso(2),r0v(2),av(2),rso(2),aso(2)
      common /rearen/ er,rear(ngh)
      common /coupl/  gsig(ngh),gome(ngh),grho(ngh)
c
c---- potentials are read in INOUT
      if (inin.eq.0) return
c
      if (lpr)
     &write(l6,*) ' ****** BEGIN START ********************************'
c
c---- default values
      if (inin.eq.1) then
         write(l6,'(/,a)') 
     &      ' uses default values as initial fields '
      endif

c---- saxon-woods potential
      if (inin.eq.2) then
c
         write(l6,'(a,f10.4)') ' v0     = ',v0
         write(l6,'(a,f10.4)') ' kappa  = ',akv
         write(l6,'(a,2f10.4)') ' lambda = ',vso
         write(l6,'(a,2f10.4)') ' r0     = ',r0v
         write(l6,'(a,2f10.4)') ' a      = ',av
         write(l6,'(a,2f10.4)') ' r0-so  = ',rso
         write(l6,'(a,2f10.4)') ' a-so   = ',aso
         do 10 it = 1,2
            ita = 3-it
            rav = r0v(it)*amas**third
            rao = rso(it)*amas**third
            vp  = v0*(1 - akv*(npr(it)-npr(ita))/amas)
c           vls = half*(hqc/amu)**2 * vp * vso(it)
            vls = vp * vso(it)
            do ih = 1,ngh
               r = xh(ih)*b0
               argv = (r - rav)/av(it)
               if (argv.le.65.d0) then
                  u = vp/(one + exp(argv))
               else
                  u = zero
               endif
               argo = (r - rao)/aso(it)
               if (argo.le.65.d0) then
                  w = -vls/(one + exp(argo))
               else
                  w = zero
               endif
               ss(ih,it) = half * (u - w)
               vv(ih,it) = half * (u + w)
            enddo
   10    continue
c
c------- Coulomb potenital
         if (icou.eq.0) then
            do ih =1,ngh
               cou(ih) = zero
            enddo
         else
            rc = r0v(2)*amas**third
            do ih = 1,ngh
               r = xh(ih)*b0
               if (r.lt.rc) then
                  c = half*(3/rc - r*r/rc**3)
               else
                  c = one/r
               endif
               cou(ih) = c*npr(2)/alphi
            enddo
         endif
         write(l6,'(/,a)') 
     &      ' Initial potentials of Saxon-Woods shape '
      endif
c
c
c---- Harmonic oscillator potential
      if (inin.eq.3) then
       stop ' in START: init = 3 not yet implemented'
         v0  = - 70.d0
         vls = -0.35
         f   = half * hom
         fls = vls*b0**2
c
c        initial deformation
c
         write(l6,*) ' v0  = ',v0
         write(l6,*) ' vls = ',vls
         do ih = 1,ngh
            rr = xh(ih)**2
            pot  = v0 +  f*rr
            spot = fls * f*rr
         enddo
         write(l6,*) ' initial potentials of oscillator shape'
      endif
c
c---- calculation of the meson-fields
      if (inin.ge.2) then
         fsig = half/(hqc*gsigs)
         fome = half/(hqc*gomes)
         frho = half/(hqc*grhos)
         do ih = 1,ngh
            sig(ih) = fsig * ( ss(ih,1) + ss(ih,2))
            ome(ih) = fome * ( vv(ih,1) + vv(ih,2))
            rho(ih) = frho * (-vv(ih,1) + vv(ih,2))
         enddo
      endif
      do ih=1,ngh
         rear(ih) = zero
         gsig(ih) = gsigs
         gome(ih) = gomes
         grho(ih) = grhos
      enddo
c
      if (lpr) then
            call prigh(0,sig,one,'Mesh ')
            call prigh(1,sig,one,' SIG')
            call prigh(1,ome,one,' OME')
            call prigh(1,rho,one,' RHO')
            call prigh(1,cou,one,' COU')
      endif    
c
      if (lpr)
     &write(l6,*) ' ****** END START **********************************'
      return
c-end START
      end 
