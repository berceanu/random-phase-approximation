      subroutine cmcn
      include 'paramet'
      implicit real*8(a-h,o-z)

      dimension la(2),lb(2)
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
      partn = 0.0
      nggh = ngh+ngh
      do it = it1,it2 !loop over protons and neutrons

         do iba=1,nb   !loop over block a
            ibga = iba - 1 + 2*mod(iba,2)
            nfa  = id(iba)
            nga  = id(ibga)
            imfa = ia(iba)
            la(1)  = ilb(iba)
            la(2)  = ilb(ibga)
            ma   = iba + (it-1)*nbx
	    ja = ijb(iba)
	    do ibb=1,nb   !loop over block b
               ibgb = ibb - 1 + 2*mod(ibb,2)
               nfb  = id(ibb)
               imfb = ia(ibb)
               lb(1)  = ilb(ibb)
               lb(2)  = ilb(ibgb)
               mb   = ibb + (it-1)*nbx
	       jb = ijb(ibb)
               do naa=1,nfa
               do nbb=1,nfb   ! loop over states in block
		  va = sqrt(vv1(imfa+naa,it))
	          vb = sqrt(vv1(imfb+nbb,it))
	          ua = sqrt(1.-va**2)
		  ub = sqrt(1.-vb**2)
	          fac2 = va*vb*(va*vb+ua*ub)
                  sum=0.0
                  do ifg=1,2  !loop over large and small components
                     lla=la(ifg)
                     llb=lb(ifg)
                     if(abs(lla-llb).ne. 1) goto 10
                     if((ja-lla) .eq. (jb-llb)) then
                       sixfcu = (lla+jb+2.)*(lla+jb-1.)/
     &                     ((2*lla+1.)*(2*llb+1.))
                       sixfcu = sqrt(sixfcu)
                     else
                       sixfcu = (jb-lla+1.)*(lla-jb+2.)/
     &                     ((2*lla+1.)*(2*llb+1.))
                       sixfcu=sqrt(sixfcu)
                       sixfcu=(2*jb-2*llb-1)*sixfcu 
                     endif
                     if (lla .gt. llb) then
                        dla=lla
                        facdru = sqrt(dla)
                        facctu = -lla
                     else
                        dlb = llb
                        facdru = -sqrt(dlb)
                        facctu = llb
                     endif
                     rint=0.0
                     do ih=1,ngh  
                        ihg=ih+(ifg-1)*ngh                              
                        wx = wdcor(ih)
                        rrb = fgc(ihg+(nbb-1)*nggh,mb)
                        rra = dfgc(ihg+(naa-1)*nggh,ma)-(facctu-1.)
     &                          *fgc(ihg+(naa-1)*nggh,ma)/rb(ih)
                        rint = rint+rrb*rra*wx*iv(ifg-1)
                     enddo
                     sum = sum + sixfcu*facdru*rint
                  enddo ! end loop over large and small components
                  partn = partn +fac2*sum**2
               enddo
               enddo  !end loop over states in blocks
10             continue
            enddo  !end loop over block b
        enddo    ! end loop over block a             
      enddo  ! end loop over protons and neutrons
      partn = fac*partn
      ecm = partd+partn
      return
      end

