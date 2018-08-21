c======================================================================c

      subroutine potgh(lpr)

c======================================================================c
C
C     CALCULATION OF THE POTENTIALS AT GAUSS-MESHPOINTS
C
c----------------------------------------------------------------------c
      include 'paramet'
c
      implicit real*8 (a-h,o-z)
      logical lpr
c

      common /fields/ sig(ngh),ome(ngh),rho(ngh),cou(ngh)
      common /mathco/ zero,one,two,half,third,pi
      common /mespar/ amsig,amome,amrho,gsigs,gomes,grhos
      common /physco/ amu,hqc,alphi,r0
      common /potpot/ vps(ngh,1:2),vms(ngh,1:2)
      common /potvec/ vec(ngh,1:2)
      common /tapes / l6,lin,lou,lwin,lwou,lplo
      common /gaussh/ xh(ngh),wh(ngh),ph(ngh) 
      common /coupl/  gsig(ngh),gome(ngh),grho(ngh)  
      common /rearen/ er,rear(ngh)
      common /gaucor/ rb(ngh),wdcor(ngh)
      common /nucnuc/ amas,nmas,nneu,npro,jmax                 
ccc
      common /pot2pot/ vs(ngh,2)
      if (lpr)
     &write(l6,*) ' ****** BEGIN POTGH ********************************'

c
      do ih = 1,ngh
         s  = gsig(ih)*sig(ih)
         go = gome(ih)*ome(ih)
         gr = grho(ih)*rho(ih)
	 rea = rear(ih) 
         v1 = go - gr + rea
         v2 = go + gr + rea + cou(ih) 
	 vec(ih,1) = v1
	 vec(ih,2) = v2
         vps(ih,1) = v1 + s
         vms(ih,1) = v1 - s
         vps(ih,2) = v2 + s
         vms(ih,2) = v2 - s     
      enddo
c
      if (lpr) then
         call prigh(1,rb,one,'X(FM) ')
         call prigh(1,vps(1,1),hqc,'V+S  n')
         call prigh(1,vms(1,1),hqc,'V-S  n')
         call prigh(1,vps(1,2),hqc,'V+S  p')
         call prigh(1,vms(1,2),hqc,'V-S  p')
      ENDIF

c
      if (lpr)
     &write(l6,*) ' ****** END POTGH **********************************'
      return
c-end-POTGH
      end
