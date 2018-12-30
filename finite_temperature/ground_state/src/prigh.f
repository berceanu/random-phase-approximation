c=====================================================================c

      subroutine prigh(is,ff,f,text)

c=====================================================================c
C
c     is=0  prints gauss-meshpoints * b0
c        1  prints f*ff(x) at gauss-meshpoints * b0
c
c---------------------------------------------------------------------c
      include 'paramet'
c     
      implicit real*8 (a-h,o-z)
      character text*(*)
c
      dimension ff(ngh)
c
      common /baspar/ hom,hb0,b0
      common /gaussh/ xh(ngh),wh(ngh),ph(ngh)
      common /mathco/ zero,one,two,half,third,pi
      common /tapes / l6,lin,lou,lwin,lwou,lplo
c
      data ix/12/
c
      if (is.eq.0) then
         write(l6,100) text,(xh(ih)*b0,ih=1,ix)
  100    format(/,1x,a6,12f10.3) 
      endif
      if (is.eq.1) then  
         write(l6,101) text,(f*ff(ih),ih=1,ix)
  101    format(1x,a6,12f10.4)
      endif
c
      return
c-end-PRIGH
      end

