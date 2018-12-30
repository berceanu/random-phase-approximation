c======================================================================c

      subroutine vpair(lpr)

c======================================================================c
c
c     calculates the pairing matrixelements with Gogny force
c
c     <n1,l1,j1; n2,l2,j2 | Vpp | n3,l3,j3; n4,l4,j4 >
c
c     the result are essentially matrix elements coupled to angular
c     momentum 0, i.e. the are nonvanishing only for
c     j1 = j2 = j  and j3 = j4 = j'
c
c     there is only one small modification:
c     the factor sqrt(2j+1)*sqrt(2j'+1), which arises from the normali-
c     zation of the Clebsch-Gordan coeffitients is taken out.
c 
c     
c----------------------------------------------------------------------c
      include 'dis.par'
c
      implicit real*8 (a-h,o-z)
c
      logical lpr
      character*8 tb
      character*25 txb
      character*10 txpair,txpair1
c
      dimension ap1(2),ap2(2),smu(2)
c
      common /baspar/ hom,hb0,b0
      common /bloosc/ ia(nbx,2),id(nbx,2)
      common /bloqua/ ijb(nbx),ilb(nbx,2),ipb(nbx),ikb(nbx)
      common /dimens/ n0f,n0b,nrm,nlm,nrbm,nb,nt,no
      common /gfviv / iv(0:igfv) 
      common /gogny / gw(2),gb(2),gh(2),gm(2),gr(2),gt3,gwls,txpair
      common /mathco/ zero,one,two,half,third,pi
      common /tapes / l6,lin,lou,lwin,lwou,lplo,laka,lvpp,lqrpa
      common /vvvppp/ vpp(mvx,mvx),ipos(nbx),ivpair
      common /parfac/ vfac
      common /texblo/ tb(ntx),txb(nbx)
c
      ik(i,k,n) = i + (k-1)*(2*n-k)/2
c
c
      write(l6,*) ' ****** BEGIN VPAIR ********************************'
c
      do i = 1,2
         ap1(i) = gw(i) + gb(i) - gh(i) - gm(i)
         ap2(i) =       - gb(i)         + gm(i)
         smu(i) = gr(i)/b0
      enddo
c
c---- determination of the positions
      mv = 0
      do ib = 1,nb
         nf  = id(ib,1)
         ipos(ib) = mv
         mv = mv + nf*(nf+1)/2
      enddo
      write(l6,*)' Total number of pairing matrix elements',mv,mv*mv,mvx
c      write(6,*) ' Total number of pairing matrix elements',mv,mv*mv,mvx
      if (mv.gt.mvx) stop 'in VPP: mvx too small'
c
c
c---- calculation of pairing matrix elements:
      if (ivpair.ne.0) then
c
c-----loop over the different j-blocks of the second index
      do ib34 = 1,nb
c         write(6,*) ' jb34 =',ib34
         j3    = ijb(ib34)
         l3    = ilb(ib34,1)
         l4    = l3
         nf34  = id(ib34,1)
         ipb34 = ipos(ib34)
c
c---- loop over the n-quantum numbers of the first index
      do n4 =  1,nf34
c         write(6,*) '   n4 =',n4
         m4  = n4 - 1
         n04 = 2*m4+l4
      do n3 =  n4,nf34
         m3  = n3 -1
         n03 = 2*m3+l3
         i34 = ipb34 + ik(n3,n4,nf34)
c
c------- loop over the different j-blocks of the first index
         do ib12 = ib34,nb
            j1    = ijb(ib12)
            l1    = ilb(ib12,1)
            l2    = l1
            nf12  = id(ib12,1)
            ipb12 = ipos(ib12)
c
c------- loop over the n-quantum numbers of the first index
         do n2 = 1,nf12
            m2  = n2 - 1
            n02 = 2*m2+l2
         do n1 = n2,nf12
            m1  = n1 - 1
            n01 = 2*m1+l1
            i12 = ipb12 + ik(n1,n2,nf12)
c  
c
c---------- sum over K
            s = zero
            do k = iabs(l1-l3),l1+l3,2
               s6 = (2*l1+1)*(2*l3+1)*racslj(k,l1,l3,j3,j1)**2
c
               sn = zero
               do n14 = max(0,(iabs(n01-n04)-k)/2),(n01+n04-k)/2 
                  sn1 = zero
                  do n23 = max(0,(iabs(n02-n03)-k)/2),(n02+n03-k)/2
                     si = zero
                     do i = 1,2
                        si = si + (ap1(i)*s6+ap2(i))*
     &                            gintmu(k,n14,n23,smu(i))
c           write(6,'(a,4i3,f20.10)') ' j6       ',l1,j1,l3,j3,s6
c           write(6,*) ' i,apc*j  ',i,(ap1(i)*s6+ap2(i))
c           write(6,*) ' i,gintmu ',i,gintmu(k,n14,n23,smu(i))
c           write(6,*) ' i,apsums ',i,si
                     enddo
                     sn1 = sn1 + si*talman(m2,l2,m3,l3,n23,k)
c           write(6,*) ' t2       ',talman(m2,l2,m3,l3,n23,k)
c           write(6,*) ' apsum2   ',sn1
                  enddo
                  sn = sn + sn1*talman(m1,l1,m4,l4,n14,k)
c           write(6,*) ' t1       ',talman(m1,l1,m4,l4,n14,k)
c           write(6,*) ' apsum1   ',sn
               enddo
               wk = iv(k)*(2*k+1)*wiglll(l1,k,l3)**2   
c           write(6,'(a,3i3,f20.10)') ' j3       ',l1,k,l3,wk
                s = s + wk*sn
c           write(6,*) ' s  =         ',s
c
c---------- end K-loop
            enddo
c
            v = s/(2*pi)
c
c---------- matrix elements coupled to J = 0 are obtained by multiplication
c           with sqrt( 2*j1 + 1 )*sqrt( 2 j3 + 1 )
c           v = v * sq(2*j1)*sq(2*j3)
c
            vpp(i12,i34) = v
            vpp(i34,i12) = v
c
            if (lpr) then
               jj1 = 2*j1 - 1
               jj3 = 2*j3 - 1
c              write(6,100) n1,l1,jj1,n2,l2,jj1,
c    &                      n3,l3,jj3,n4,l3,jj3,vpp(i12,i34)
c              write(l6,100) n1,l1,jj1,n2,l2,jj1,
c    &                       n3,l3,jj3,n4,l3,jj3,vpp(i12,i34)
               write(6,100)  m1,l1,jj1,m3,l3,jj3,
     &                       m2,l1,jj1,m4,l3,jj3,vpp(i12,i34)
               write(l6,100) m1,l1,jj1,m3,l3,jj3,
     &                       m2,l1,jj1,m4,l3,jj3,vpp(i12,i34)
  100          format(' <',2(i3,i2,i3,'/2 '),'| VPP |',
     &                    2(i3,i2,i3,'/2 '),'> =',f15.10)
c               write(6,*) i12,i34,ik(i12,i34)
c               read(*,*)
            endif
c
c------- end first index loops (12)
   32    enddo
   31    enddo
   30    enddo
c
c---- end second index loops (34)
   22 enddo
   21 enddo
   20 enddo
c
      endif
c
c
c---- writing and reading of pairing matrix elements
      open(lvpp,file='dis.vpp',form='unformatted',status='unknown')
      if (ivpair.eq.0) then
         read(lvpp)  txpair1,mv1
         if (txpair1.ne.txpair) stop ' in VPAIR: force is wrong'
         if (mv1.ne.mv) stop ' in VPAIR: configuration space wrong'
      else
         write(lvpp)  txpair,mv
      endif
c
c
c-----loop over the different j-blocks of the second index
      nme = 0 
      do ib34 = 1,nb
         nf34  = id(ib34,1)
         ipb34 = ipos(ib34)
         n34   = nf34*(nf34+1)/2
c
c---- loop over the n-quantum numbers of the first index
      do i34 =  1,n34
c
c------- loop over the different j-blocks of the first index
         do ib12 = ib34,nb
            nf12  = id(ib12,1)
            ipb12 = ipos(ib12)
            n12   = nf12*(nf12+1)/2
            nme   = nme + n12
c
c------- loop over the n-quantum numbers of the first index
            if (ivpair.eq.0) then
               read(lvpp) (vpp(ipb12+i12,ipb34+i34),i12=1,n12) 
               do i12 = 1,n12
                  vpp(ipb34+i34,ipb12+i12) = vpp(ipb12+i12,ipb34+i34)
               enddo
            else
               write(lvpp) (vpp(ipb12+i12,ipb34+i34),i12=1,n12) 
            endif
c
c------- end first index loops (12)
         enddo
c
c---- end second index loops (34)
      enddo
      enddo
         
      close(lvpp)
      if (ivpair.eq.0) then
         write(l6,101) 
     &   '  pairing matrix elements read from tape   dis.vpp:',nme
  101    format(a,i14)
      elseif (ivpair.eq.1) then
         write(l6,101) 
     &   '  pairing matrix elements written on tape  dis.vpp:',nme
      elseif (ivpair.eq.2) then
         stop ' in VPAIR: all matr.elem. calculated'
      endif
c
c
c---- renormalizing of the force
c
      write(l6,*) ' VPAIR MULTIPICATION:',vfac
      do i = 1,mv
      do k = 1,mv
         vpp(i,k) = vfac*vpp(i,k)
      enddo
      enddo
c
      write(l6,*) ' ****** END VPAIR **********************************'
      return
C-end-VPAIR
      end
