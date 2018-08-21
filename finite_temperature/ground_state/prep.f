c======================================================================c

      subroutine prep

c======================================================================c
c
c     preparations
c
c----------------------------------------------------------------------c
c
      include 'paramet'
c
      implicit real*8 (a-h,o-z)
      character*1 tp,tl,tis
      character*2 nucnam
      character*10 txtfor
c
      common /baspar/ hom,hb0,b0
      common /gaucor/ rb(ngh),wdcor(ngh)
      common /gaussh/ xh(ngh),wh(ngh),ph(ngh)
      common /iterat/ si,siold,epsi,xmix,xmix0,xmax,maxi,ii,inxt,iaut
      common /mathco/ zero,one,two,half,third,pi
      common /mespar/ amsig,amome,amrho,gsigs,gomes,grhos
      common /nucnuc/ amas,nmas,nneu,npro,jmax
      common /optopt/ icm,icou,it1,it2,ncut
      common /pair  / ga(2),gg(2),del(2),spk(2),dec(2),pwi
      common /physco/ amu,hqc,alphi,r0
      common /potpot/ ss(ngh,1:2),vv(ngh,1:2)
      common /rhorho/ ros(ngh,2),rov(ngh,2),dro(ngh)     
      common /tapes / l6,lin,lou,lwin,lwou,lplo
      common /textex/ nucnam,tp(2),tis(2),tl(0:20),txtfor
      common /para/ ipara
      common /cpara/ a_s,b_s,c_s,d_s,a_v,b_v,c_v,d_v,a_tv,dsat                
c
c
c
      write(l6,*) ' ****** BEGIN PREP *********************************'
c
      if (ipara.eq.0) then
c         c_s = third/d_s**2
         d_s = one/sqrt(3.d0*c_s)
         a_s = (one+c_s*(one+d_s)**2)/(one+b_s*(one+d_s)**2)
c         c_v = third/d_v**2
         d_v = one/sqrt(3.d0*c_v)
         facs=two*a_s*(b_s-c_s)*(one-3.d0*c_s*(one+d_s)**2)/
     &                (one+c_s*(1+d_s)**2)**3
         faco=(one-3.d0*c_v*(one+d_v)**2)/(one+c_v*(1+d_v)**2)**3
         x=facs/(two*faco)
         fac1=x+c_v*(one+c_v*(one+d_v)**2)
         fac2 = one+c_v*(one+d_v)**2-x*(one+d_v)**2
c         b_v = fac1/fac2
         a_v =(one+c_v*(one+d_v)**2)/(one+b_v*(one+d_v)**2)
      endif 
c     signs and factorials
      call gfv
c
c---- nuclear parameters
      call nucleus(2,npro,nucnam)
      nneu = nmas - npro
      amas = nmas
      if (nneu.eq.0) it1 = 2
      if (npro.eq.0) it2 = 1
      write(l6,'(a,a,i4,i6,i4)') ' Nucleus: ',nucnam,nmas,nneu,npro
c
c---- basis parameters
      hb0 = hqc**2/(two*amu)
      hom = 41.0*amas**(-third)    
      if (icm.gt.0) hb0 = hb0*(one - one/amas)
      if (b0.le.0.0) then
         b0 = sqrt(two*hb0/hom)
          write(l6,*) ' b0 is calculated: ',b0
      endif
       call gauleg(0.d0,20.d0/b0,xh,wh,ngh)     
      do ih = 1,ngh
         rb(ih) = xh(ih)*b0
c
c        metric element for three-dimensional integration 
         wdcor(ih) = b0**3 * 4*pi * xh(ih)**2 * wh(ih)
      enddo
c
c---- pairing force
      do it = 1,2
         del(it) = del(it) + dec(it)
         gg(it)  = ga(it)/amas
      enddo
      pwi = 2.5*hom
      pwi =2.d+10
c
      write(l6,*) ' hom = ',hom
      write(l6,*) ' hb0 = ',hb0
      write(l6,*) ' b0  = ',b0 
c
c
c---- printout of force:
      write(l6,'(/,a,a)') ' Meson-Parameters: ',txtfor
      write(l6,'(a,f10.4,a,f10.4)') 
     &          ' msig  = ',amsig,'  gsigs = ',gsigs
      write(l6,'(a,f10.4,a,f10.4)') 
     &          ' mome  = ',amome,'  gomes = ',gomes
      write(l6,'(a,f10.4,a,f10.4)') 
     &          ' mrho  = ',amrho,'  grhos = ',grhos

      if (ipara.eq.0) then
         write(l6,'(a)') 'Parametrization type : Typel & Wolter'
      elseif (ipara.eq.1) then
         write(l6,'(a)') 'Parametrization type : Polynom'
      elseif (ipara.eq.2) then
         write(l6,'(a)') 'Parametrization type: Exponential' 
      else
         write(*,*) 'Wrong value for ipara'
	 stop
      endif
      write(l6,'(a)') 'Density dependence parameters:'
      write(l6,'(a,f10.4,a,f10.4,a,f10.4,a,f10.4)')
     &   ' a_s = ',a_s,' b_s = ',b_s,' c_s = ',c_s,' d_s = ',d_s
      write(l6,'(a,f10.4,a,f10.4,a,f10.4,a,f10.4)')
     &   ' a_v = ',a_v,' b_v = ',b_v,' c_v = ',c_v,' d_v = ',d_v
      write(l6,'(a,f10.4)') ' a_tv = ',a_tv
c---- printout pairing:
      write(l6,'(a,2f10.4)') '  Gap parameter = ',dec
      write(l6,'(a,2(f10.4,2h/A))') '  Pairing const.= ',ga
      write(l6,'(a,2f10.4)') '  Pairing window= ',pwi/hom

c
c
      if (icou.eq.0) write(l6,*) ' without Coulomb force'
      if (icou.eq.1) write(l6,*) ' with Coulomb force'
      if (icou.eq.2) write(l6,*) ' with Coulomb force with exchange'
      if (icm.eq.1)  write(l6,*) ' with center of mass correction '
      write(l6,*) ' Mixing-Parameter xmix: ',xmix
c
c
      do it = 1,2
      do ih = 1,ngh
            ss(ih,it)  = zero
            vv(ih,it)  = zero
            ros(ih,it) = zero
            rov(ih,it) = zero
      enddo
      enddo
c
c
c
      write(l6,*) ' ****** END PREP ***********************************'
      return
c-end PREP
      end 
