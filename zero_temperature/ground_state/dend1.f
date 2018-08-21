      subroutine dend1(lpr)
      
      implicit real*8(a-h,o-z)
      include 'dis.par'
      
      logical lpr
      
      dimension rho(ngh)
      common /mespar/ amsig,amome,amrho,gsigs,gomes,grhos
      common /coupl/  gsig(ngh),gome(ngh),grho(ngh) 
      common /cpara/ a_s,b_s,c_s,d_s,a_v,b_v,c_v,d_v,a_tv,dsat          
      common /rhorho/ rs(ngh,2),rv(ngh,2),dro(ngh)      
      common /tapes / l6,lin,lou,lwin,lwou,lplo 
      common /para/ ipara    
      common /gaucor/ rb(ngh),wdcor(ngh)        
      
      if (lpr)
     &          write(l6,*) '********** BEGIN DEND1 *********'
      
      do ih = 1,ngh
         rho(ih) = (rv(ih,1)+rv(ih,2))/dsat
      enddo
      do ih = 1,ngh
         densv = rv(ih,1)+rv(ih,2)
	 if (ipara.eq.0) then
            gsig(ih) = gsigs*(dip1(rho(ih),a_s,b_s,c_s,d_s))
	    gome(ih) = gomes*(dip1(rho(ih),a_v,b_v,c_v,d_v))
	 elseif(ipara.eq.1) then
            gsig(ih) = gsigs*(dip2(rho(ih),a_s,b_s,0.,0.))
	    gome(ih) = gomes*(dip2(rho(ih),a_v,b_v,0.,0.))
	 elseif(ipara.eq.2) then
            gsig(ih) = gsigs*(dip3(rho(ih),a_s,0.,0.,0.))
	    gome(ih) = gomes*(dip3(rho(ih),a_v,0.,0.,0.))
	 endif	    	    
	 grho(ih) = grhos*(dip3(rho(ih),a_tv,0.,0.,0.))

	 write(l6,100) rb(ih),gsig(ih),gome(ih),grho(ih)
      enddo
100   format (4f12.7)      
      if (lpr)
     &          write(l6,*) '********** END DEND1 *********'      
     
      return
      end
      
