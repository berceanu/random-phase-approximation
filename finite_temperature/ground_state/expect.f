c======================================================================c

      subroutine expect(lpr)

c======================================================================c
c
c     calculates expectation values
c
c----------------------------------------------------------------------c
      include 'paramet'
      parameter (ndwork = nwork-4*ngh-4)
c
      implicit real*8 (a-h,o-z)
      logical lpr
c
      dimension xn(3),r2(3),xs(3)
      dimension rx4(2),rx6(2)
      dimension ept(3),ekt(3),epart(3),entro(3),vir(3)
      dimension h0(nq4x)
c
      dimension vvnor(ntx,2)    
c
      common /bloblo/ nb,ijb(nbx),ilb(nbx),
     &                id(nbx),idq(nbx),ia(nbx),iaq(nbx)
      common /baspar/ hom,hb0,b0
      common /eeeeee/ ee(ntx,2),vv(ntx,2),vv1(ntx,2),mu(ntx)
      common /erwar / ea,rms,qp
      common /fermi / ala(2),tz(2)
      common /dimens/ n0f,n0b,nrm,nlm
      common /fields/ sig(ngh),ome(ngh),rho(ngh),cou(ngh)
      common /gaucor/ rb(ngh),wdcor(ngh)
      common /gaussh/ xh(ngh),wh(ngh),ph(ngh)
      common /mathco/ zero,one,two,half,third,pi
      common /mespar/ amsig,amome,amrho,gsigs,gomes,grhos
      common /nucnuc/ amas,nama,npr(2),jmax 
      common /optopt/ icm,icou,it1,it2,ncut
      common /pair  / ga(2),gg(2),del(2),spk(2),dec(2),pwi
      common /physco/ amu,hqc,alphi,r0
      common /potpot/ vps(ngh,1:2),vms(ngh,1:2)
      common /quaqua/ nt,nr(ntx),nl(ntx),nj(ntx)
      common /rhorho/ rs(ngh,2),rv(ngh,2),dro(ngh)
      common /tapes / l6,lin,lou,lwin,lwou,lplo
      common /work  / dsig(ngh),dome(ngh),drho(ngh),dcou(ngh),
     &                dwork(ndwork)
      common /wavefg/ fg(nq2x,nb2x)
      common /single/ sp(nqx,nbx)
      common /rearen/ er,rear(ngh)
      common /coupl/  gsig(ngh),gome(ngh),grho(ngh)            
      common /cenmas/ ecm,partd,partn
c
      common /temper/ temp
c
      if (lpr)
     &write(l6,*) ' ****** BEGIN EXPECT *******************************'
c
c
      emcc2=2*amu/hqc
      do it = 1,3
         xn(it) = zero
	 xs(it) = zero 
         r2(it) = zero
         rx4(it) = zero
         rx6(it) = zero
      enddo
c
c---- particle number and radii
      do ih = 1,ngh
         r  = rb(ih)
         rr = r*r  
         r4= r*r*r*r
         r6= r*r*r*r*r*r
         wx = wdcor(ih)
         do it = it1,it2
            x      = wx*rv(ih,it)
            xn(it) = xn(it) + x
	    xs(it) = xs(it) +wx*rs(ih,it)
            r2(it) = r2(it) + x*rr
            rx4(it) = rx4(it) + x*r4
            rx6(it) = rx6(it) + x*r6
         enddo
      enddo
c
c add for RPA sum rule
       r2_SR = (r2(1) + r2(2))/nama
c       Scal_dipol_m1 = hqc**2/(2*amu)*npr(2)**2*9.0/(4*pi*nama)
       Vec_dipol_m1 = hqc**2/(2*amu)*npr(1)*npr(2)*9/(4*pi*nama)
c       Scal_quad_m1 = Scal_dipol_m1*r2_SR*50.0/9.0
       Scal_mon_m1 = hqc**2/amu*2*(r2(1)+r2(2))
       Scal_quad_m1 = hqc**2/amu*25.0*(r2(1)+r2(2))/(4.0*pi)
c       Scal_dipol_m1 = hqc**2/amu*0.75*(r2(1)+r2(2))/pi
c add end

      do it = it1,it2
         r2(it) = sqrt(r2(it)/xn(it))
         rx4(it) = rx4(it)/xn(it)
         rx6(it) = rx6(it)/xn(it)
      enddo
      rx4(2) = rx4(2)**(1./4.)
      rx6(2) = rx6(2)**(1./6.)       
      xn(3) = xn(1) + xn(2)
      xs(3) = xs(1) + xs(2) 
      r2(3) = sqrt((npr(1)*r2(1)**2+npr(2)*r2(2)**2)/amas)
      rc    = sqrt(r2(2)**2 + 0.64)
      rms   = r2(3)    
c    
c
c---- pairing-energy
      do it = it1,it2
         del(it) = gg(it)*spk(it) + dec(it)
         ept(it) = - del(it)*spk(it)
      enddo
      ept(3) = ept(1) + ept(2)
c
c---- kinetic energy
      do it=it1,it2
         ekt(it)=zero
         do ib=1,nb
            ibg=ib-1+2*mod(ib,2)
	    nf=id(ib)
	    ng=id(ibg)
            lf  = ilb(ib)
            if (lf.gt.n0f) goto 11
	    nd=nf+ng
	    m=ib+(it-1)*nbx
            imf=ia(ib)
c---- construction of the free Dirac-operator h0
            do n2=1,nf
               do n1=1,nf
                  h0(n1+(n2-1)*nd)=zero
               enddo
               do n1=1,ng
                  h0(nf+n1+(n2-1)*nd)=sp(n1+(n2-1)*ng,ib)
                  h0(n2+(nf+n1-1)*nd)=h0(nf+n1+(n2-1)*nd)
               enddo
            enddo
            do n2=nf+1,nd
               do n1=nf+1,nd
                  h0(n1+(n2-1)*nd)=zero
               enddo
               h0(n2+(n2-1)*nd)=-emcc2
            enddo
c----       cut off large components with highest N
            if (2*(nf-1)+lf.gt.n0f) then
               do i = 1,nf
                  h0(nf+(i-1)*nd) = zero
               enddo
               do i = nf+1,nd
                  h0(i+(nf-1)*nd) = zero
               enddo
               h0(nf+(nf-1)*nd) = 1000.0
            endif 
            sr=zero
            do k=1,nf
               do n1=1,nd
                  sr1=zero
                  do n2=1,nd
                     sr1=sr1+h0(n1+(n2-1)*nd)*fg(n2+(k-1)*nd,m)
                  enddo
                  sr=sr+fg(n1+(k-1)*nd,m)*sr1*vv(imf+k,it)
               enddo
            enddo
            ekt(it)=ekt(it)+sr
         enddo
         ekt(it)=ekt(it)*hqc
11    continue
      enddo 
      ekt(3)=ekt(1)+ekt(2)           		     
c	         
c---- single particle energy
      do it = it1,it2
         epart(it) = zero
	 entro(it) = zero
         do i = 1,nt
            epart(it) = epart(it) + ee(i,it)*vv(i,it)
         enddo
      enddo
      epart(3) = epart(1) + epart(2)
c---- field energies
      esig  = zero
      eome  = zero
      erho  = zero
      ecou  = zero
      ecoex = zero
      enl   = zero
      do ih = 1,ngh
         wx   = wdcor(ih)
         esig = esig - gsig(ih)*sig(ih)*( rs(ih,1)+rs(ih,2))*wx
         eome = eome - gome(ih)*ome(ih)*( rv(ih,1)+rv(ih,2))*wx
         erho = erho - grho(ih)*rho(ih)*(-rv(ih,1)+rv(ih,2))*wx
         if (icou.ge.1) ecou = ecou - cou(ih)*rv(ih,2)*wx
         if (icou.eq.2) ecoex = ecoex + rv(ih,2)**(4*third)*wx
      enddo
      esig  = hqc*esig/2
      eome  = hqc*eome/2
      erho  = hqc*erho/2
      ecou  = hqc*ecou/2
      ecoex =  -(0.75d0*hqc/alphi)*(3/pi)**third*ecoex
c
c---- rearrengment energy
      call dend2(.false.,0)
      if (abs(ecm) .lt. 0.0001) then 
         ecm  = -0.75d0*hom 
      endif
c
      etot = epart(3) + esig + eome + erho + ecou + ecoex -
     &                  er*hqc + ept(3) + ecm
      ea = etot/amas
      etott= ekt(3)-esig-eome-erho-ecou+ept(3)+ecm 

      eaa=etott/amas 
c    
c---- entropy
      entropy=0 
      if ( temp .ne. 0.0) then
      do it=1,2
         do i=1,nt
            vvnor(i,it)= vv(i,it)/mu(i)
            if (vvnor(i,it) .eq. 0 .or. vvnor(i,it) .eq. 1 ) then
             entropy=entropy
            else    
             entropy= entropy+ mu(i)*( vvnor(i,it)*dlog(vvnor(i,it))+
     &           (1-vvnor(i,it))*dlog(1-vvnor(i,it)))
            endif
         enddo
      enddo
      entropy=-entropy     
      write(*,*)'entropy:   ',  entropy
      endif

c
c---- printout
      if (.not.lpr) return
      
      write(20,*) temp, etot, eaa, r2(1), rc, rms, entropy
c
      write(l6,'(/,28x,a,8x,a,9x,a)') 'neutron','proton','total'
c
c     particle number
      write(l6,'(a,6x,3f15.6)') ' particle number',xn
c
c     Lambda
      write(l6,'(a,7x,2f15.6)') ' lambda        ',ala
c
c     Delta
      write(l6,'(a,7x,2f15.6)') ' Delta         ',del
c
c     trace of kappa
      write(l6,'(a,7x,2f15.6)') ' spk           ',spk
c
c     rms-Radius    
      write(l6,'(a,7x,3f15.6)') ' rms-Radius    ',r2
c
c     charge-Radius    
      write(l6,'(a,22x,f15.6)') ' charge-Radius ',rc
c
c
c     kinetic energy
      write(l6,'(/,a,7x,3f15.6)') ' Kinetic Energy',ekt

c     single-particle energy
      write(l6,'(/,a,7x,3f15.6)') ' Particle Energ',epart
      write(l6,'(/,a,7x,3f15.6)') ' Selfconsistency test',etott-etot
c 
c     sigma energy 
      write(l6,'(a,37x,f15.6)') ' E-sigma       ',esig 
c 
c     nonlinear part sigma energy 
      write(l6,'(a,37x,f15.6)') ' Rearr. contr. ',-er*hqc 
c 
c     omega energy  
      write(l6,'(a,37x,f15.6)') ' E-omega       ',eome   
c 
c     rho-energy       
      write(l6,'(a,37x,f15.6)') ' E-rho         ',erho 
c
c     Coulomb energy (direct part)
      write(l6,'(a,37x,f15.6)') ' Coulomb direct',ecou 
c
c     Coulomb energy (exchange part in Slater approx.)
      write(l6,'(a,37x,f15.6)') ' Coulomb exch. ',ecoex 
c
c     pairing energy
      write(l6,'(a,7x,3f15.6)') ' Pairing Energy',ept
c
c     center of mass correction
      write(l6,'(a,37x,f15.6)') ' E-cm          ',ecm
c
c     total energy
      write(l6,'(a,37x,f15.6)') ' Total Energy  ',etot
c
c     energy per particle
      write(l6,'(a,37x,f15.6)') ' E/A           ',ea 
c
c    entropy
      write(l6,'(a, 37x,f15.6)') 'Entropy       ', entropy

c    RPA sum rule
      write(l6,'(a, 37x,f15.6)') '<r^2>         ', r2_SR   
      write(l6,'(a, 37x,f15.6)') 'IS dipole m1         ', Scal_dipol_m1
      write(l6,'(a, 37x,f15.6)') 'IV dipole m1         ', Vec_dipol_m1
      write(l6,'(a, 37x,f15.6)') 'IS quadrupole m1         ',
     $Scal_quad_m1
      write(l6,'(a, 37x,f15.6)') 'IS monopole m1         ',
     $Scal_mon_m1
   
      write(l6,*) ' ****** END EXPECT *********************************'
      return
c-end-EXPECT
      end


