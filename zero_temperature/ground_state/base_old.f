c======================================================================c

      subroutine base(lpr)

c======================================================================c
c
c     determines the basis in spherical oscillators for Dirac solution 
c
c----------------------------------------------------------------------c
      include 'dis.par'
c
      implicit real*8 (a-h,o-z)
      logical lpr
c
      character*1 tp,tl,tis
      character*2 nucnam
      character*10 txtfor
      character*8 tb,tit
      character*25 txb
c
      common /baspar/ hom,hb0,b0
      common /dimens/ n0f,n0b,nrm,nlm
      common /bloblo/ nb,ijb(nbx),ilb(nbx),
     &                id(nbx),idq(nbx),ia(nbx),iaq(nbx)
      common /eeeeee/ eqp(ntx,2),ee(ntx,2),v2(ntx,2),mu(ntx)
      common /nucnuc/ amas,nama,nneu,npro,jmax
      common /quaqua/ nt,nr(ntx),nl(ntx),nj(ntx)
      common /tapes / l6,lin,lou,lwin,lwou,lplo,laka,lvpp,lqrpa
      common /texblo/ tb(ntx),txb(nbx)
      common /textex/ nucnam,tp(2),tis(2),tit(2),tl(0:20),txtfor
      common /ugugug/ itbl(2),jbl(2),ipbl(2),nbl(2),nrbl(2)
c
      if (lpr)
     &write(l6,*) ' ****** BEGIN BASE *********************************'
c
      write(6,*) 'n0f,n0fx',n0f,n0fx
      if (n0f.gt.n0fx) stop ' in BASE: n0f too large'
      je = min0(n0f+1,jmax)
c
      ib     = 0
      ilauf  = 0
      nrm    = 0
      nlm    = 0
      nbl(1) = 0
      nbl(2) = 0
c
c---- loop over j-quantum number
      do 10 j = 1,je
c
c---- loop over parity
      do 10 ip = 1,2
         l = j - mod(j+ip+1,2)   
         nlm = max0(nlm,l)
c
c        write(l6,'(/,a,i3,a,a1)') ' j = ',j+j-1,'/2',tp(ip)
         ne = (n0f+1-l)/2 + 1
         jlauf = ilauf
         do 20 ir = 1,ne
            ilauf  = ilauf + 1
            if (ilauf.gt.ntx) stop ' in BASE: ntx too small'
            nr(ilauf) = ir
            nl(ilauf) = l
            nj(ilauf) = j
            mu(ilauf) = j
            write(tb(ilauf),'(i2,a1,i3,2h/2)') ir,tl(l),j+j-1
            nn        = 2*(ir-1)+l
c           write(l6,'(i4,a,i2,a,i2,a,i2)') 
c    &           ilauf,'  N = ',nn,'   n = ',ir,'   l = ',l
            nrm = max0(nrm,ir)
   20    continue
c          
         if (ilauf.gt.jlauf) then
            ib = ib + 1
            if (ib.gt.nbx)  stop ' in BASE: nbx too small'
            ia(ib)  = jlauf 
            id(ib)  = ilauf-jlauf
            if (id(ib).gt.ndx) stop ' in BASE: ndx too small'
            ijb(ib) = j
            ilb(ib) = l
            write(txb(ib),'(i3,a,i2,a,a1)') 
     &            ib,'. block:  j = ',j+j-1,'/2',tp(ip)
c
c           determination of blocked level
            do it = 1,2
               if ( itbl(it).eq.1  .and. jbl(it).eq.j .and. 
     &              ipbl(it).eq.ip ) nbl(it)=ib
            enddo
         endif
c
   10 continue
      nb  = ib 
      nt  = ilauf
      if (nrm.gt.nrx) stop 'in BASE: nrx too small '
      if (nlm.gt.nlx) stop 'in BASE: nlx too small '
c
c---- determination of the corresponding small components quantum numbers
      do ib = 1,nb
         ibq = ib - 1 + 2*mod(ib,2)
         idq(ib) = id(ibq)
         iaq(ib) = ia(ibq)
      enddo
c
c---- printout
      if (lpr) then
         do 40 ib = 1,nb
            j  = ijb(ib)
            ip = mod(ilb(ib),2)+1
            i1 = ia(ib)+1
            i2 = ia(ib)+id(ib)
            write(l6,'(/,i3,a,i3,a,a1)') 
     &                ib,'. block:  j = ',j+j-1,'/2',tp(ip)
            do i = i1,i2
               n = nr(i)
               l = nl(i)
               nn = 2*(n-1)+l
               write(l6,'(i4,a,i2,a,i2,a,i2,3x,a)') 
     &               i,'  N = ',nn,'   n = ',n,'   l = ',l,tb(i)
            enddo
            i1 = iaq(ib)+1
            i2 = iaq(ib)+idq(ib)
            do i = i1,i2
               n = nr(i)
               l = nl(i)
               nn = 2*(n-1)+l
               write(l6,'(i4,a,i2,a,i2,a,i2,3x,a)') 
     &               i,'  N = ',nn,'   n = ',n,'   l = ',l,tb(i)
            enddo
   40    continue
         write(l6,'(/,a,2i4)') ' Number of blocks: nb  = ',nb,nbx
         write(l6,100) ' Number of levels  nt  = ',nt,ntx 
         write(l6,100) ' Maximal n:        nrm = ',nrm,nrx
         write(l6,100) ' Maximal l:        nlm = ',nlm,nlx
         write(l6,100) ' Blocked levels:   nrbl= ',nrbl
  100    format(a,2i4)
      endif
c    
      if (lpr)
     &write(l6,*) ' ****** END BASE ***********************************'
      return
c-end-BASE
      end
