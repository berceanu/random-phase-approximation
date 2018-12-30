c=====================================================================c

      subroutine prigh(is,ff,f,text)

c=====================================================================c
C
c     is=0  prints gauss-meshpoints * b0  (b0 = f)
c        1  prints f*ff(x) at gauss-meshpoints 
c        2  prints f*ff(x)/(wh(ih)*xh(i)**2)
c
c---------------------------------------------------------------------c
      include 'dis.par'
c     
      implicit real*8 (a-h,o-z)
      character text*(*)
c
      dimension ff(ngh)
c
      common /gaussh/ xh(ngh),wh(ngh),ph(ngh)
      common /mathco/ zero,one,two,half,third,pi
      common /tapes / l6,lin,lou,lwin,lwou,lplo,laka,lvpp,lqrpa
c
      data ix/6/
c
      if (is.eq.0) then
         write(l6,100) text,(f*xh(ih),ih=1,ix)
  100    format(/,1x,a6,12f10.4) 
      elseif (is.eq.1) then  
         write(l6,101) text,(f*ff(ih),ih=1,ix)
  101    format(1x,a6,12f10.4)
      elseif (is.eq.2) then  
         write(l6,101) text,(f*ff(ih)/(wh(ih)*xh(ih)**2),ih=1,ix)
      endif
c
      return
c-end-PRIGH
      end
