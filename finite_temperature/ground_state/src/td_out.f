c=====================================================================c

      subroutine td_out

c=====================================================================c
C
C     prepares plot of specific wafefunctions f(r) and g(r)
c     it = 1 for neutrons,  it = 2 for protons
c     ib number of block
c     k  number of specific wavefunction in this block
C
c---------------------------------------------------------------------c
      include 'paramet'
c
      implicit real*8 (a-h,o-z)
      logical lpr
c
c
      dimension nstate(2),l(2)
      common /baspar/ hom,hb0,b0
      common /gaussh/ xh(ngh),wh(ngh),ph(ngh)
      common /mathco/ zero,one,two,half,third,pi
      common /optopt/ icm,icou,it1,it2,ncut
      common /tapes / l6,lin,lou,lwin,lwou,lplo
      common /bloblo/ nb,ijb(nbx),ilb(nbx),
     &                id(nbx),idq(nbx),ia(nbx),iaq(nbx) 
      common /physco/ amu,hqc,alphi,r0
      common /eeeeee/ ee(ntx,2),vv(ntx,2),vv1(ntx,2),mu(ntx)
                      

c     number of points for the plot
      mxpl = 300
c
c     plot step in (fm)
      stpl = 0.05

c
c     plot for wavefunctions:
c----------------------------
      open(lplo,file='read3D.m',status='unknown')
      do it=it1,it2
          nstate(it)=0
          do ib=1,nb 
             nf  = id(ib)
             imf = ia(ib)
	     do n=1,nf
	        if(vv(imf+n,it).gt.0.5) nstate(it)=nstate(it)+1
             enddo
	  enddo
      enddo
      write(lplo,*) mxpl
      write(lplo,*) nstate(2)
      write(lplo,*) nstate(1)	     	         
      do it=it2,it1,-1
         do ib=1,nb
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
	    ip = mod(ilb(ib),2)+1
            if (ip.eq.1) then 
               ip=1
            else
               ip=-1
            endif
	    do n=1,nf   !loop over states in block
	       if (vv(imf+n,it).lt.0.5) goto 10
	       write(lplo,*) n
	       rj=j*one-half
	       write(lplo,*) rj
	       write(lplo,*) l(1)
	       write(lplo,*) l(2)
	       write(lplo,*) ip
	       write(lplo,*) ee(imf+n,it)+amu	    
               if (ip.eq.-1) then 
                  fac=-one
               else 
                  fac = one
               endif
               r = zero
               do ist = 0,mxpl-1
                  call rwave(it,ib,n,r,f,g)
                  write(lplo,100) r,r*f,fac*r*g
100      format(f10.3,2f15.6) 
                  r = r + stpl
               enddo
10          enddo   !end loop over states in block
         enddo
      enddo
      close(lplo)
c
      return
C-end-PLOT
      end
