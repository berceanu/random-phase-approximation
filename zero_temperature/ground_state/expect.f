c======================================================================c

      subroutine expect(lpr)

c======================================================================c
c
c     calculates expectation values
c
c----------------------------------------------------------------------c
      include 'dis.par'
      parameter (ndwork = nwork-nhqx)
c
      implicit real*8 (a-h,o-z)
      logical lpr
c
      dimension xn(3),r2(3)
      dimension ept(3),ekt(3),epart(3)
      dimension del1(2),del2(2)
c
      common /baspar/ hom,hb0,b0
      common /bloosc/ ia(nbx,2),id(nbx,2)
      common /bloqua/ ijb(nbx),ilb(nbx,2),ipb(nbx),ikb(nbx)
      common /dimens/ n0f,n0b,nrm,nlm,nrbm,nb,nt,no
      common /eeeeee/ eqp(ntx,2),ee(ntx,2),v2(ntx,2),mu(ntx)
      common /erwar / ea,rms,qp
      common /fermi / ala(2),tz(2)
      common /fields/ sig(ngh),ome(ngh),rho(ngh),cou(ngh)
      common /gaucor/ rb(ngh),wdcor(ngh)
      common /gaussh/ xh(ngh),wh(ngh),ph(ngh)
      common /hfbhfb/ hh(nhqx,nb2x),de(nhqx,nb2x)
      common /kappa / aka(nqx,nb2x)
      common /kappag/ akag(nqx,nb2x)
      common /mathco/ zero,one,two,half,third,pi
      common /mespar/ amsig,amome,amrho,gsigs,gomes,grhos
      common /nucnuc/ amas,nama,npr(2),jmax 
      common /optopt/ icm,icou,it1,it2,ncut
      common /pair  / ga(2),gg(2),del(2),spk(2),spk0(2),dec(2),pwi
      common /physco/ amu,hqc,alphi,r0
      common /potpot/ vps(ngh,1:2),vms(ngh,1:2)
      common /rhorho/ rs(ngh,2),rv(ngh,2),dro(ngh)
      common /rhoro2/ rs2(ngh,2),rv2(ngh,2)
      common /single/ sp(nqx,nbx)
      common /tapes / l6,lin,lou,lwin,lwou,lplo,laka,lvpp,lqrpa
      common /ugugug/ itbl(2),jbl(2),ipbl(2),nbl(2),nrbl(2)
      common /wavefg/ fg(2*nhq2x,nb2x)
      common /work  / h0(nhqx),dwork(ndwork)
      common /rearen/ er,rear(ngh)
      common /coupl/  gsig(ngh),gome(ngh),grho(ngh) 
      common /cenmas/ ecm,partd,partn
c
      if (lpr)
     &write(l6,*) ' ****** BEGIN EXPECT *******************************'
c
c
      do it = 1,3
         xn(it) = zero
         r2(it) = zero
      enddo
c
c---- particle number and radii
      do ih = 1,ngh
         r  = rb(ih)
         rr = r*r
         wx = wdcor(ih)
         do it = it1,it2
            x      = wx*rv(ih,it)
            xn(it) = xn(it) + x
            r2(it) = r2(it) + x*rr
         enddo
      enddo
c
      do it = it1,it2
         r2(it) = sqrt(r2(it)/xn(it))
      enddo
c
      xn(3) = xn(1) + xn(2)
      r2(3) = sqrt((npr(1)*r2(1)**2+npr(2)*r2(2)**2)/amas)
      rc    = sqrt(r2(2)**2 + 0.64)
      rms   = r2(3)
c
c
c
c
c---- kinetic energy and pairing energy
      do it = it1,it2
c
c------- minimal quasiparticle energy
         s = 1000.d0
         do k = 1,nt
            s = min(s,eqp(k,it))
         enddo
         del1(it) = s
c
         ekt(it) = zero
         ept(it) = zero
         epart(it)=zero
	 ibl     = nbl(it)
	 kbl     = nrbl(it)
         do ib = 1,nb
            mul = ijb(ib)
            lf  = ilb(ib,1)
            if (lf.gt.n0f) goto 10
            nf  = id(ib,1)
            ng  = id(ib,2)
            nh  = nf + ng
            nhfb= nh + nh
            m   = ib + (it-1)*nbx
c
c---------- construction of the free Dirac-operator H0
            emcc2 = 2*amu
            do n2 = 1,nf
               do n1 = 1,nf
                  h0(n1+(n2-1)*nh) = zero
               enddo
               do n1 = 1,ng
                  h0(nf+n1+(n2-1)*nh) = sp(n1+(n2-1)*ng,ib)
                  h0(n2+(nf+n1-1)*nh) = h0(nf+n1+(n2-1)*nh)
               enddo
            enddo
            do n2 = nf+1,nh
               do n1 = nf+1,nh
                  h0(n1+(n2-1)*nh) = zero
               enddo
               h0(n2+(n2-1)*nh) = - emcc2
            enddo
c            call aprint(1,1,6,nh,nh,nh,h0,' ',' ','H0') 
c            call aprint(1,1,6,nh,nh,nh,de(1,m),' ',' ','DE') 
c
c---------- calculation of Tr(H0 * RO) and 1/2*Tr(Delta * Kappa)
            sr = zero
            sd = zero
            sh = zero
            do k = 1,nf
               do n1 = 1,nh
                  sr1 = zero
                  sd1 = zero
                  sh1 = zero
                  do n2 = 1,nh
                     sr1 = sr1 + h0(n1+(n2-1)*nh)
     &                          *fg(nh+n2+(k-1)*nhfb,m)
                     sd1 = sd1 + de(n1+(n2-1)*nh,m)
     &                          *fg(n2+(k-1)*nhfb,m)
                     sh1 = sh1 + hh(n1+(n2-1)*nh,m)
     &                         *fg(nh+n2+(k-1)*nhfb,m)
                  enddo
                  sr = sr + fg(nh+n1+(k-1)*nhfb,m)*sr1
                  sd = sd + fg(nh+n1+(k-1)*nhfb,m)*sd1
                  sh = sh + fg(nh+n1+(k-1)*nhfb,m)*sh1
               enddo
            enddo
            sr = 2*mul*sr
            sd =   mul*sd
            sh = 2*mul*sh
c
c---------- blocking
            if (ib.eq.ibl) then
               do n1 = 1,nh
                  sr1 = zero
                  sr2 = zero
                  sh1 = zero
                  sh2 = zero
                  sd1 = zero
                  do n2 = 1,nh
                  sr1 = sr1 + h0(n1+(n2-1)*nh)*fg(nh+n2+(kbl-1)*nhfb,m)
                  sr2 = sr2 + h0(n1+(n2-1)*nh)*fg(   n2+(kbl-1)*nhfb,m)
                  sh1 = sh1 + hh(n1+(n2-1)*nh,m)
     &                                        *fg(nh+n2+(kbl-1)*nhfb,m)
                  sh2 = sh2 + hh(n1+(n2-1)*nh,m)
     &                                        *fg(   n2+(kbl-1)*nhfb,m)
                  sd1 = sd1 + de(n1+(n2-1)*nh,m)*fg(n2+(kbl-1)*nhfb,m)
                  enddo
                  sr = sr - fg(nh+n1+(kbl-1)*nhfb,m)*sr1
     &                    + fg(   n1+(kbl-1)*nhfb,m)*sr2
                  sh = sh - fg(nh+n1+(kbl-1)*nhfb,m)*sh1
     &                    + fg(   n1+(kbl-1)*nhfb,m)*sh2
                  sd = sd - fg(nh+n1+(kbl-1)*nhfb,m)*sd1
               enddo
	    endif
c
            ekt(it) = ekt(it) + sr
            ept(it) = ept(it) - sd
            epart(it) = epart(it) + sh
c
            sd1 = zero
            il = 0
            do n2 = 1,nf
            do n1 = 1,nf
               il = il + 1
               sd1 = sd1 + de(n1+(n2-1)*nh,m)*aka(il,m)
            enddo
            enddo
   10    enddo
c
         del2(it) = - ept(it)/(spk(it)+1.d-10)
      enddo
      ekt(3) = ekt(1) + ekt(2)
      ept(3) = ept(1) + ept(2)
      epart(3) = epart(1) + epart(2)
c
c---- field energies
      esig  = zero
      eome  = zero
      erho  = zero
      ecou  = zero
      ecoex = zero
      do ih = 1,ngh
         wx   = wdcor(ih)
         esig = esig + gsig(ih)*sig(ih)*( rs(ih,1)+rs(ih,2))*wx
         eome = eome + gome(ih)*ome(ih)*( rv(ih,1)+rv(ih,2))*wx
         erho = erho + grho(ih)*rho(ih)*(-rv(ih,1)+rv(ih,2))*wx
         if (icou.ge.1) ecou = ecou + cou(ih)*rv(ih,2)*wx
         if (icou.eq.2) ecoex = ecoex - rv(ih,2)**(4*third)*wx
      enddo
      esig  = hqc*esig/2
      eome  = hqc*eome/2
      erho  = hqc*erho/2
      ecou  = hqc*ecou/2
      ecoex =  -(0.75d0*hqc/alphi)*(3/pi)**third*ecoex
c
c---- rearrangement contribution
      call dend2(.false.,0)

      if(abs(ecm).lt.0.0001)  ecm  = -0.75d0*hom
c
c      epart(3) = ekt(3) + 2*(esig+eome+erho+ecou)
      etot = epart(3) - esig - eome - erho - ecou + ecoex -
     &                  er*hqc + ept(3) + ecm
      etott = ekt(3)+esig+eome+erho+ecou+ecoex+ept(3)+ecm
      ea = etot/amas
      eaa = etott/amas
c
c---- printout
      if (.not.lpr) return
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
      write(l6,'(a,7x,2f15.6)') ' Delta  Emin   ',del1
      write(l6,'(a,7x,2f15.6)') ' Delta  Ep/spk ',del2
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
c     single-particle energy
      write(l6,'(a,7x,3f15.6)') ' Particle Energ',epart
      write(l6,'(/,a,7x,f15.6)') ' Selfconsistency test',etott-etot
c
c     kinetic energy
      write(l6,'(/,a,7x,3f15.6)') ' Kinetic Energy',ekt
c 
c     sigma energy 
      write(l6,'(a,37x,f15.6)') ' E-sigma       ',esig  
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
c     sigma energy 
      write(l6,'(a,37x,f15.6)') ' E-Rearr       ',-er*hqc 
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
c
      write(l6,*) ' ****** END EXPECT *********************************'
      return
c-end-EXPECT
      end
