      subroutine cmcd
      include 'paramet'
      implicit real*8(a-h,o-z)

      dimension l(2)
      common /baspar/ hom,hb0,b0
      common /bloblo/ nb,ijb(nbx),ilb(nbx),
     &                id(nbx),idq(nbx),ia(nbx),iaq(nbx)
      common /mathco/ zero,one,two,half,third,pi
      common /optopt/ icm,icou,it1,it2,ncut
      common /radosc/ rnl(1:nrx,0:nlx,ngh),rnl1(1:nrx,0:nlx,ngh)
      common /wavefg/ fg(nq2x,nb2x)
      common /wfc/ fgc(2*ngx,nb2x),dfgc(2*ngx,nb2x)    
      common /eeeeee/ ee(ntx,2),vv(ntx,2),vv1(ntx,2),mu(ntx)
      common /gaucor/ rb(ngh),wdcor(ngh)
      common /gaussh/ xh(ngh),wh(ngh),ph(ngh)
      common /gfviv / iv(0:igfv)
      common /physco/ amu,hqc,alphi,r0
      common /nucnuc/ amas,nama,nneu,npro,jmax
      common /cenmas/ ecm,partd,partn

      amu_fm = amu/hqc  !nucleon mass in fm^{-1}
      fac = one/(two*amu_fm*amas)
      fac = fac*hqc    ! correction in MeV
      partd = 0.0
      do it = it1,it2

c------- loop over the different j-blocks
         do ib = 1,nb
            ibg = ib - 1 + 2*mod(ib,2)
            nf  = id(ib)
            ng  = id(ibg)
            nd  = nf + ng
            imf = ia(ib)
            img = ia(ibg)
            m   = ib + (it-1)*nbx
	    j = ijb(ib)
            l(1) = ilb(ib)
            l(2) = ilb(ibg)
            part_ds = 0.0  
            nggh = ngh+ngh  
            do i = 1, nf  ! loop over states in block
               part_dl = 0.0
               do ifg=1,2 ! loop over large and small components
                  comp_1 = 0.0
                  comp_2 = 0.0
                  do ih=1,ngh
                     wx = wdcor(ih)
                     wx1 = wx/rb(ih)**2
                     ihg = (ifg-1)*ngh+ih
                     comp_1 = comp_1 + dfgc(ihg+(i-1)*nggh,m)**2*wx
                     comp_2 = comp_2 + fgc(ihg+(i-1)*nggh,m)**2*wx1
                  enddo
               part_dl = part_dl+comp_1  + l(ifg)*(l(ifg)+1)*comp_2
               enddo ! end loop over large and small components
               part_ds = part_ds + vv1(imf+i,it)*2*j*part_dl
            enddo  !end loop over states in block
            partd = partd + part_ds
         enddo
      enddo      
      partd = -partd*fac
      return
      end
