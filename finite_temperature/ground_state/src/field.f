c======================================================================c

      subroutine field(lpr)

c======================================================================c
c
c     calculation of the meson-fields in the oscillator basis
c     the fields are given in (fm^-1)
c
c----------------------------------------------------------------------c
      include 'paramet'
      parameter (ndwork = nwork-3*ngh-3)
c
      implicit real*8 (a-h,o-z)
      logical lpr
c
      common /baspar/ hom,hb0,b0
      common /fields/ sig(ngh),ome(ngh),rho(ngh),cou(ngh)
      common /gaussh/ xh(ngh),wh(ngh),ph(ngh)
      common /iterat/ si,siold,epsi,xmix,xmix0,xmax,maxi,ii,inxt,iaut
      common /mathco/ zero,one,two,half,third,pi
      common /mespar/ amsig,amome,amrho,gsigs,gomes,grhos
      common /optopt/ icm,icou,it1,it2,ncut
      common /physco/ amu,hqc,alphi,r0
      common /rhorho/ rs(ngh,2),rv(ngh,2),dro(ngh)
      common /tapes / l6,lin,lou,lwin,lwou,lplo
      common /work  / so(ngh),phi(ngh),sig1(ngh),dwork(ndwork)
      common /coupl/  gsig(ngh),gome(ngh),grho(ngh)
      common /rearen/ er,rear(ngh)
c
      data maxs/50/
c
      if (lpr)
     &write(l6,*) ' ****** BEGIN FIELD ********************************'
c
c
c---- Mixing of new and old fields: 
      xmi = xmix
      si  = zero
c---- reare. contribution
      call dend2(.false.,1)
c
c
c---- sigma-meson
      ami2 = (hqc/amsig)**2
      do ih = 1,ngh
         f    = -gsig(ih)*ami2      
         so(ih) = f*(rs(ih,1)+rs(ih,2))
      enddo
      call gordon(1,so,phi)
      do ih = 1,ngh
         sv       = phi(ih) - sig(ih)
         sig(ih)  = sig(ih) + xmi*sv
         si = max(si,abs(sv))
      enddo
c
       write(*,*) 'test sv = ', sv

c
c---- omega-meson
      ami2 = (hqc/amome)**2
      do ih = 1,ngh
         f  = +gome(ih)*ami2      
         so(ih) = f*(rv(ih,1)+rv(ih,2))
      enddo
      call gordon(2,so,phi)
      do ih = 1,ngh
         sv       = phi(ih) - ome(ih)
         ome(ih)  = ome(ih) + xmi*sv
         si = max(si,abs(sv))
      enddo
c

       write(*,*) 'test sv = ', sv

c
c---- rho-meson
      ami2 = (hqc/amrho)**2
      do ih = 1,ngh
         f  = +grho(ih)*ami2      
         so(ih) = f*(-rv(ih,1)+rv(ih,2))
      enddo
      call gordon(3,so,phi)
      do ih = 1,ngh
         sv       = phi(ih) - rho(ih)
         rho(ih)  = rho(ih) + xmi*sv
         si = max(si,abs(sv))
      enddo
C
C
       write(*,*) 'test sv = ', sv

C---- photon
      if (icou.ge.1) then
         call coulom(phi)
         do ih = 1,ngh
            sv       = phi(ih) - cou(ih)
            cou(ih)  = cou(ih) + xmi*sv
            si = max(si,abs(sv))
         enddo
      endif
c
      si = si*hqc
c

c
      if (lpr) then
         call prigh(0,sig,one,'x(fm) ')
         call prigh(1,sig,one,'Sigma ')
         call prigh(1,ome,one,'Omega ')
         call prigh(1,rho,one,'Rho   ')
         call prigh(1,cou,one,'Coulom')
      endif
C  
       write(*,*) 'test sv = ', sv, phi(1), cou(1) 
      if (lpr)
     &write(l6,*) ' ****** END FIELD **********************************'
      return
C-end-FIELD
      end
c======================================================================c

      subroutine gordon(imes,so,phi)

c======================================================================c
C
C     SOLUTION OF THE KLEIN-GORDON-EQU. BY EXPANSION IN OSCILLATOR
c     imes: number of the meson
c     so:   source
c     phi:  meson field
c
c----------------------------------------------------------------------c
      include 'paramet'
      parameter (nox2 = nox*nox)
c
      implicit real*8 (a-h,o-z)
c
      dimension so(ngh),phi(ngh)
      dimension gi(nox,nox),rr(nox,ngh)
C
      common /baspar/ hom,hb0,b0
      common /physco/ amu,hqc,alphi,r0
      common /dimens/ n0f,n0b,nrm,nlm
      common /gaussh/ xh(ngh),wh(ngh),ph(ngh)
      common /greens/ gg(ngh,1:ngh,1:3),igreen(3)
      common /gfvsq / sq(0:igfv)
      common /gfvsqh/ sqh(0:igfv)
      common /mathco/ zero,one,two,half,third,pi
      common /mespar/ ames(3),gsigs,gomes,grhos
      common /radbos/ rnb(1:nox,ngh)
      common /tapes / l6,lin,lou,lwin,lwou,lplo
c
      data igreen/0,0,0/
c
c     write(l6,*) ' ****** BEGIN GORDON *******************************'
c
c
c---- calculation of the Greens function
      if (igreen(imes).eq.0) then
         f  = (hqc/(ames(imes)*b0))**2
         no = n0b/2 + 1
         do i = 1,no
            do k = 1,no
               gi(i,k) = zero
            enddo
         enddo
         do n = 1,no
            gi(n,n) = one + f*(2*n-half) 
            if (n.lt.no) then
               gi(n,n+1) = f*sq(n)*sqh(n)
               gi(n+1,n) = gi(n,n+1)
            endif
            do ih = 1,ngh
               rr(n,ih)=rnb(n,ih)*wh(ih)*xh(ih)**2
            enddo
         enddo
         call lingd(nox,nox,no,ngh,gi,rr,d,ifl)
         do ih = 0,ngh
            do kh = 1,ngh
               s = zero
               do n = 1,no
                  s = s + rnb(n,ih)*rr(n,kh)
               enddo
               gg(ih,kh,imes) = s
            enddo
         enddo      
         igreen(imes) = 1
      endif
c
c
c---- multiplication of source with Greens function
      do ih = 1,ngh
         s = zero
         do kh = 1,ngh
            s = s + gg(ih,kh,imes)*so(kh)
         enddo
         phi(ih) = s
      enddo
c
c     write(l6,*) ' ****** END GORDON *********************************'
      return
c-end-GORDON
      end
c======================================================================c
 
      subroutine coulom(cou)

c======================================================================c
c
c     Coulom-Field (direct part)
c
c----------------------------------------------------------------------c
      include 'paramet'
c
      implicit real*8 (a-h,o-z)
c
      dimension cou(ngh)
c
      common /baspar/ hom,hb0,b0
      common /coucal/ vc(ngh,ngh),icacou
      common /gaucor/ rb(ngh),wdcor(ngh)
      common /mathco/ zero,one,two,half,third,pi
      common /physco/ amu,hqc,alphi,r0
      common /rhorho/ rs(ngh,2),rv(ngh,2),dro(ngh)
      common /tapes / l6,lin,lou,lwin,lwou,lplo
c
      data icacou/0/
c
c     write(l6,*) ' ****** BEGIN COULOM *******************************'
c
c
c---- calculation of the Coulomb interaction
      if (icacou.eq.0) then
         f = one/(6*alphi)
         do ih = 1,ngh
            do kh = 1,ngh
               rg = dmax1(rb(ih),rb(kh))
               rk = dmin1(rb(ih),rb(kh))
               vc(ih,kh) = f * ( 3*rg + rk**2/rg) * wdcor(kh) 
            enddo
         enddo
         icacou = 1
      endif
c
c---- calculation of the Coulomb field
      do ih = 1,ngh
         s = zero
         do kh = 1,ngh
             s = s + vc(ih,kh) * dro(kh) 
         enddo
         cou(ih) = s
      enddo
c
c     f = hqc/(6*alphi)
c
c     do ih = 0,ngh
c        s = zero
c        do kh = 1,ngh
c            rg = dmax1(rb(ih),rb(kh))
c            rk = dmin1(rb(ih),rb(kh))
c            s = s + dro(kh) * ( 3*rg + rk**2/rg) * wdcor(kh) 
c        enddo
c        cou(ih) = f*s
c     enddo
c
c
c     write(l6,*) ' ****** END COULOM *********************************'
      return
c-end-COULOM
      end      
