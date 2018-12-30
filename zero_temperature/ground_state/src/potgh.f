c======================================================================c

      subroutine potgh(lpr)

c======================================================================c
C
C     CALCULATION OF THE POTENTIALS AT GAUSS-MESHPOINTS
C
c----------------------------------------------------------------------c
      include 'dis.par'
c
      implicit real*8 (a-h,o-z)
      logical lpr
c

      common /fields/ sig(ngh),ome(ngh),rho(ngh),cou(ngh)
      common /mathco/ zero,one,two,half,third,pi
      common /mespar/ amsig,amome,amrho,gsigs,gomes,grhos
      common /physco/ amu,hqc,alphi,r0
      common /potpot/ vps(ngh,1:2),vms(ngh,1:2)
      common /tapes / l6,lin,lou,lwin,lwou,lplo
      common /pot1pot/ vvps(ngh,2),vvms(ngh,2)
       common /gaussh/ xh(ngh),wh(ngh),ph(ngh)
      common /coupl/  gsig(ngh),gome(ngh),grho(ngh)  
      common /rearen/ er,rear(ngh) 
ccc
      common /pot2pot/ vs(ngh,2)
      if (lpr)
     &write(l6,*) ' ****** BEGIN POTGH ********************************'

c
      do ih = 1,ngh
         s  = gsig(ih)*sig(ih)*hqc
         go = gome(ih)*ome(ih)*hqc
         gr = grho(ih)*rho(ih)*hqc 
         rea = rear(ih)
         v1 = go - gr + rea*hqc
         v2 = go + gr + cou(ih)*hqc + rea*hqc
         vps(ih,1) = v1 + s
         vms(ih,1) = v1 - s
         vps(ih,2) = v2 + s
         vms(ih,2) = v2 - s     
      enddo
c
      if (lpr) then
         call prigh(0,sig,one,'X(FM) ')
         call prigh(1,vps(1,1),one,'V+S  n')
         call prigh(1,vms(1,1),one,'V-S  n')
         call prigh(1,vps(1,2),one,'V+S  p')
         call prigh(1,vms(1,2),one,'V-S  p')
      ENDIF

c
      if (lpr)
     &write(l6,*) ' ****** END POTGH **********************************'
      return
c-end-POTGH
      end
c======================================================================c

      subroutine pot(n,nh,l,v,tt)

c======================================================================c
      include 'dis.par'
c
      implicit real*8 (a-h,o-z)
c
      dimension tt(nh,nh),v(ngh)
c
      common /gaussh/ xh(ngh),wh(ngh),ph(ngh)
      common /radosc/ rnl(1:nrx,0:nlx,ngh),rnl1(1:nrx,0:nlx,ngh)
c
      do 10 n2 = 1,n
      do 10 n1 = n2,n
         s = 0.0
         do 20 ih = 1,ngh
            s = s + v(ih)*rnl(n1,l,ih)*rnl(n2,l,ih)
   20    continue
         tt(n1,n2) = s
   10 continue
c
      return
c-end-POT
      end
