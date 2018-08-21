c=====================================================================
      subroutine wavec
c      generates wave functions in coordinate space
c=====================================================================

      include 'paramet'
      implicit real*8(a-h,o-z)

      common /baspar/ hom,hb0,b0      
      common /bloblo/ nb,ijb(nbx),ilb(nbx),
     &                id(nbx),idq(nbx),ia(nbx),iaq(nbx)
      common /mathco/ zero,one,two,half,third,pi
      common /optopt/ icm,icou,it1,it2,ncut
      common /radosc/ rnl(1:nrx,0:nlx,ngh),rnl1(1:nrx,0:nlx,ngh)
      common /wavefg/ fg(nq2x,nb2x)
      common /gaussh/ xh(ngh),wh(ngh),ph(ngh)
      common /wfc/ fgc(2*ngx,nb2x),dfgc(2*ngx,nb2x)

c------- loop over protons and neutrons 
      do it = it1,it2

c------- loop over the different j-blocks
         do ib = 1,nb
            ibg = ib - 1 + 2*mod(ib,2)
            nf  = id(ib)
            ng  = id(ibg)
            nd  = nf + ng
            imf = ia(ib)
            img = ia(ibg)
            lf  = ilb(ib)
            lg  = ilb(ibg)
            m   = ib + (it-1)*nbx
            nggh = ngh+ngh
         
c------- loop over states in block
            do i = 1, nf
               do ih = 1,ngh
                  wx = xh(ih)*sqrt(wh(ih))*b0**(3./2.)*sqrt(4*pi)
                  wx1= wx*b0
                  s = 0.0
                  s1 = 0.0
                  do j = 1, nf
                     s = s + fg(j+ (i-1)*nd,m)*rnl(j,lf,ih)
                     s1 = s1 + fg(j+ (i-1)*nd,m)*rnl1(j,lf,ih)
                  enddo
                  fgc(ih+(i-1)*nggh,m) = s/wx
                  dfgc(ih + (i-1)*nggh,m) = s1/wx1
                  s = 0.0
                  s1 = 0.0
                  do j = 1, ng
                     s = s + fg(j+nf + (i-1)*nd,m)*rnl(j,lg,ih)
                     s1 = s1 + fg(j+nf + (i-1)*nd,m)*rnl1(j,lg,ih)
                  enddo
                  fgc(ngh+ih+(i-1)*nggh,m) = s/wx
                  dfgc(ngh+ih + (i-1)*nggh,m) = s1/wx1
               enddo
            enddo
         enddo
      enddo
c      do ih=1,ngh
c         write(31,*) xh(ih)*b0,fgc(ih,1),dfgc(ih,1)
c      enddo
      return
      end          
