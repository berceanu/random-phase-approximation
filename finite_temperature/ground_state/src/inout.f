c======================================================================c

      subroutine inout(is,lpr)

c======================================================================c
c
c     is = 1: reads meson-fields from tape
c          2: writes meson-fields  to tape
c
c----------------------------------------------------------------------c
      include 'paramet'
      parameter (ndwork = nwork-3*ngh-3)
c
      implicit real*8 (a-h,o-z)
      logical lpr
c
      character*1 tp,tl,tis
      character*2 nucnam,nucnam1
      character*10 txtfor,txtfor1
c
      dimension ga1(2),gg1(2),del1(2),spk1(2),dec1(2),tz1(2)
      dimension npr1(2)
c
      common /baspar/ hom,hb0,b0
      common /bloblo/ nb,ijb(nbx),ilb(nbx),
     &                id(nbx),idq(nbx),ia(nbx),iaq(nbx)
      common /dimens/ n0f,n0b,nrm,nlm
      common /erwar / ea,rms,qp
      common /fermi / ala(2),tz(2)
      common /fields/ sig(ngh),ome(ngh),rho(ngh),cou(ngh)
      common /gaucor/ rb(ngh),wdcor(ngh)
      common /gaussh/ xh(ngh),wh(ngh),ph(ngh)
      common /initia/ vin,rin,ain,inin
      common /iterat/ si,siold,epsi,xmix,xmix0,xmax,maxi,ii,inxt,iaut
      common /mathco/ zero,one,two,half,third,pi
      common /mespar/ amsig,amome,amrho,gsigs,gomes,grhos
      common /nucnuc/ amas,nama,npr(2),jmax
      common /optopt/ icm,icou,it1,it2,ncut
      common /pair  / ga(2),gg(2),del(2),spk(2),dec(2),pwi
      common /physco/ amu,hqc,alphi,r0
      common /quaqua/ nt,nr(ntx),nl(ntx),nj(ntx)
      common /tapes / l6,lin,lou,lwin,lwou,lplo
      common /textex/ nucnam,tp(2),tis(2),tl(0:20),txtfor
      common /work  / xx(ngh),yy(ngh),yp(ngh),dwork(ndwork)
      common /coupl/  gsig(ngh),gome(ngh),grho(ngh) 
      common /cpara/ a_s,b_s,c_s,d_s,a_v,b_v,c_v,d_v,a_tv,dsat
      common /rearen/ er,rear(ngh)                      
c
      if (is.eq.1.and.inin.ne.0) return
c
      write(l6,*) ' ****** BEGIN INOUT ********************************'
c
c
c
c---- reading of meson fields from tape:
c-------------------------------------
      if (is.eq.1) then
         open(lwin,file='skys_' // 'dis.wel',status='old')
         read(lwin,100) 
     &        nucnam1,nama1,npr1,ngh1,n0f1,n0b1,nb1,nt1
  100    format(1x,a2,8i4)
         read(lwin,'(5x,f12.6,6x,f12.9,2f12.6)') 
     &        b01,si,ea,rms
         read(lwin,'(a10,4f10.4)') txtfor1,amsig1,amome1,amrho1
         read(lwin,'(10x,3f10.4)') gsigs1,gomes1,grhos1
	 read(lwin,'(10x,4f10.4)') a_s1,b_s1,c_s1,d_s1
	 read(lwin,'(10x,4f10.4)') a_v1,b_v1,c_v1,d_v1
	 read(lwin,'(10x,2f10.4)') a_tv1,dsat1		 	 
         read(lwin,103) ga1,gg1,pwi1
  103    format(10x,5f12.6)
         read(lwin,103) del1,dec1
         read(lwin,103) spk1
         read(lwin,103) ala,tz1
c
         read(lwin,101) sig
         read(lwin,101) ome
         read(lwin,101) rho
         read(lwin,101) cou
	 read(lwin,101) gsig
	 read(lwin,101) gome
	 read(lwin,101) grho
	 read(lwin,101) rear
  101    format(4e20.12)
         close(lwin)
         write(l6,*) ' potentials read from tape dis.wel:'
         write(l6,100) nucnam1,nama1,npr1,ngh1,n0f1,nb1,nt1 
         write(l6,102) b01,si
  102    format(5h b0 =,f12.6,6h  si =,f12.6) 
c
c
c     writing of potentials to tape:
c-----------------------------------
      else
         open(lwou,file='skys_' // 'dis.wel',status='unknown')
         write(lwou,100) nucnam,nama,npr,ngh,n0f,n0b,nb,nt
         write(lwou,'(5h b0 =,f12.6,6h  si =,f12.9,2f12.6)') 
     &              b0,si,ea,rms
         write(lwou,'(a10,4f10.4)') txtfor,amsig,amome,amrho
         write(lwou,'(10x,3f10.4)') gsigs,gomes,grhos
	 write(lwou,'(10x,4f10.4)') a_s,b_s,c_s,d_s
	 write(lwou,'(10x,4f10.4)') a_v,b_v,c_v,d_v
	 write(lwou,'(10x,2f10.4)') a_tv,dsat	 	 
         write(lwou,104) 'Pairing:  ',ga,gg,pwi
  104    format(a,5f12.6)
         write(lwou,104) 'Delta:    ',del,dec
         write(lwou,104) 'Spk:      ',spk
         write(lwou,104) 'Lambda:   ',ala,tz
         write(lwou,101) sig
         write(lwou,101) ome
         write(lwou,101) rho
         write(lwou,101) cou 
	 write(lwou,101) gsig
	 write(lwou,101) gome
	 write(lwou,101) grho
	 write(lwou,101) rear
         close(lwou)
         write(l6,*) ' potentials written to tape dis.wel'
      endif
c
      if (lpr) then
         call prigh(1,sig,one,'SIG ')
         call prigh(1,ome,one,'OME ')
         call prigh(1,rho,one,'RHO ')
         call prigh(1,cou,one,'COU ')
         call prigh(1,rho,hqc,'RHO M')
      endif
c
      close(lwou)
c
      write(l6,*) ' ****** END INOUT **********************************'
      return
c-end-INOUT
      end      
