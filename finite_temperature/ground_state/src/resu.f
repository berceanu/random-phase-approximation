c======================================================================c

      subroutine resu(lpr)

c======================================================================c
      include 'paramet'
c
      implicit real*8 (a-h,o-z)
c
      character*1 tp,tl,tis
      character*2 nucnam
      character*10 txtfor
      character*4 filename
      logical lpr
      dimension jpar(50),npar(50),lpar(50)
      dimension jhol(50),nhol(50),lhol(50)
      
      dimension eeord(nt,2), vvord(nt,2), vvnor(nt,2)
      dimension nrord(nt,2), nlord(nt,2), jord(nt,2)
c
      common /mespar/ amsig,amome,amrho,gsigs,gomes,grhos
      common /baspar/ hom,hb0,b0
      common /bloblo/ nb,ijb(nbx),ilb(nbx),
     &                id(nbx),idq(nbx),ia(nbx),iaq(nbx)
      common /eeeeee/ ee(ntx,2),vv(ntx,2),vv1(ntx,2),mu(ntx)
      common /fields/ sig(ngh),ome(ngh),rho(ngh),cou(ngh)
      common /mathco/ zero,one,two,half,third,pi
      common /physco/ amu,hqc,alphi,r0
      common /rhorho/ rs(ngh,2),rv(ngh,2),dro(ngh)
      common /tapes / l6,lin,lou,lwin,lwou,lplo
      common /textex/ nucnam,tp(2),tis(2),tl(0:20),txtfor
      common /rearen/ er,rear(ngh) 
      common /gaucor/ rb(ngh),wdcor(ngh)
       common /coupl/  gsig(ngh),gome(ngh),grho(ngh)
       
      common /quaqua/ nt,nr(ntx),nl(ntx),nj(ntx)
      common /fermi / ala(2),tz(2)
      common /file/ filename
c
      open(17,file='skys_' // filename//'occup_n.txt',status='unknown')
      open(18,file='skys_' // filename//'occup_p.txt',status='unknown')
      write(l6,*) ' ****** BEGIN RESU *********************************'
c
c---- single particle energies
      write(l6,100) 
  100 format(//,' Single-particle Energies',/,1x,24(1h-),/,
     $20x,'neutrons',35x,'protons')
      en0 = ee(1,1)
      ep0 = ee(1,2)
      do ib = 1,nb
         nf  = id(ib)
         im  = ia(ib)+1
         j2  = 2*ijb(ib)-1
         ip  = 2-mod(ib,2)
c
         ie = im+nf-1
         do 20 i = im,ie 
            if (ee(i,1).gt.20.0.and.ee(i,2).gt.20.0) goto 20
            if (i.eq.im) write(l6,*)
            write(l6,101) i,j2,tp(ip),ee(i,1),ee(i,1)-en0,vv(i,1),
     &                               ee(i,2),ee(i,2)-ep0,vv(i,2)
 101        format(i3,' j =',i2,'/2',a1,2f10.3,f8.3,8x,2f10.3,f8.3)
            
  20     continue
      enddo
  102 format(//,' Energies',/,1x,24(1h-),/,
     $20x,'particle',35x,'hole')
c
c----print out occupation ni versus ei
c
      do it=1,2
       do i=1,nt
        vvnor(i,it)=vv(i,it)/mu(i)
        eeord(i,it)=ee(i,it)
        vvord(i,it)=vvnor(i,it)
           
        nrord(i,it) = nr(i)
        nlord(i,it) = nl(i)
        jord(i,it) = nj(i)
       enddo
          
       call ordi2(nt, eeord(1,it), vvord(1,it),
     $ nrord(1,it),nlord(1,it),jord(1,it))
      enddo
      
      do 30 i=1,nt
        if (eeord(i,1).gt.20.0.and.eeord(i,2).gt.20.0) goto 30
        write(17,*)eeord(i,1), vvord(i,1),
     $   nrord(i,1), nlord(i,1),jord(i,1)
        write(18,*)eeord(i,2),vvord(i,2),
     $   nrord(i,2), nlord(i,2),jord(i,2)
  30  continue
       write(17,*)ala(1)
       write(18,*)ala(2)
      close(17)
      close(18)
c
c      if (lpr) then
c---- particle energies, hole energies
c---- neutrons
c      open(unit=17,file='skys_' // 'PB208.n',status='old',form='formatted')
c      read (17,*) epexp,ehexp   ! experimental values
c      read (17,*) nump
c      do j=1,nump
c         read(17,*) npar(j),lpar(j),jpar(j)
c      enddo
c      read (17,*) numh 
c      do j=1,numh
c         read(17,*) nhol(j),lhol(j),jhol(j)
c      enddo
c      close(17) 
c      ep=0.0
c      pnorm=0.0 
c      do j=1,nump
c         iparity=(-1)**lpar(j) 
c         if (jpar(j) .eq. lpar(j)+1) ibase=2*lpar(j)+1
c         if (jpar(j) .eq. lpar(j)) ibase=2*lpar(j)-1
c         if (iparity .eq. -1) ibase=ibase+1
c         ep=ep+2*jpar(j)*ee(ia(ibase)+npar(j),1)
c         pnorm=pnorm+2*jpar(j)
c      enddo
c      eh=0.0
c      hnorm=0.0 
c      do j=1,numh
c         iparity=(-1)**lhol(j)
c         if (jhol(j) .eq. lhol(j)+1) ibase=2*lhol(j)+1
c         if (jhol(j) .eq. lhol(j)) ibase=2*lhol(j)-1
c         if (iparity. eq. -1) ibase=ibase+1
c         eh=eh+2*jhol(j)*ee(ia(ibase)+nhol(j),1)
c         hnorm=hnorm+2*jhol(j)
c      enddo
c      write(l6,103) ep/pnorm 
c      write(l6,104) eh/hnorm
103   format('particles:',1x,f10.6)      
104   format('holes:',1x,f10.6)
c-----protons
c      open(unit=18,file='skys_' // 'PB208.p',status='old',form='formatted')
c      read (18,*) epexp,ehexp   ! experimental values
c      read (18,*) nump
c      do j=1,nump
c         read(18,*) npar(j),lpar(j),jpar(j)
c      enddo
c      read (18,*) numh 
c      do j=1,numh
c         read(18,*) nhol(j),lhol(j),jhol(j)
c      enddo
c      close(18) 
c      ep=0.0
c      pnorm=0.0 
c      do j=1,nump
c         iparity=(-1)**lpar(j) 
c         if (jpar(j) .eq. lpar(j)+1) ibase=2*lpar(j)+1
c         if (jpar(j) .eq. lpar(j)) ibase=2*lpar(j)-1
c         if (iparity .eq. -1) ibase=ibase+1
c         ep=ep+2*jpar(j)*ee(ia(ibase)+npar(j),2)
c         pnorm=pnorm+2*jpar(j)
c      enddo
c      eh=0.0
c      hnorm=0.0 
c      do j=1,numh
c         iparity=(-1)**lhol(j)
c         if (jhol(j) .eq. lhol(j)+1) ibase=2*lhol(j)+1
c         if (jhol(j) .eq. lhol(j)) ibase=2*lhol(j)-1
c         if (iparity. eq. -1) ibase=ibase+1
c         eh=eh+2*jhol(j)*ee(ia(ibase)+nhol(j),2)
c         hnorm=hnorm+2*jhol(j)
c      enddo
c      write(l6,103) ep/pnorm 
c      write(l6,104) eh/hnorm 
c      endif !lpr                  
c	
c---- cm correction
      call wavec
      call cmcd
      call cmcn
      call expect(.true.)
c
      write(l6,*) ' ****** END RESU ***********************************'
      return
c-end-RESU
      end 


c=======================================================================
  
      subroutine ordi2(n,e,emu,nr,nl,nj)
  
c=======================================================================
c     
C     orders a set of numbers according to their size
c
c-----------------------------------------------------------------------
      implicit double precision (a-h,o-z)
C
      dimension e(n),emu(n)
      dimension nr(n), nl(n), nj(n)
c  
      do 10 i = 1,n
         k  = i 
         p  = e(i)
         if (i.lt.n) then
            do 20 j = i+1,n 
               if (e(j).lt.p) then 
                  k = j 
                  p = e(j)
               endif
   20       continue
            if (k.ne.i) then
               e(k)  = e(i)
               e(i)  = p
               emk    = emu(k)
               emu(k) = emu(i)
               emu(i) = emk
               nrk = nr(k)
               nr(k) = nr(i)
               nr(i) = nrk
               nlk = nl(k)
               nl(k) = nl(i)
               nl(i) = nlk
               njk = nj(k)
               nj(k) = nj(i)
               nj(i) = njk
            endif
         endif
   10 continue
c 
      return
c-end-ORDI
      end 
