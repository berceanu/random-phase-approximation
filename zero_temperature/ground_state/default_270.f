c======================================================================c

      blockdata default

c======================================================================c
c
c     Default for Relativistic Mean Field spherical
c     with Gogny-Force for pairing
c
c----------------------------------------------------------------------c
c
      implicit real*8 (a-h,o-z)
      include 'dis.par'
c
      character*1 tp,tl,tis
      character*2 nucnam
      character*8 tit
      character*10 txtfor,txpair
c
      common /baspar/ hom,hb0,b0
      common /dimens/ n0f,n0b,nrm,nlm,nrbm,nb,nt,no
      common /fermi / ala(2),tz(2)
      common /fields/ sig(ngh),ome(ngh),rho(ngh),cou(ngh)
      common /fixocc/ ioc(nbx,2)
      common /gogny / gw(2),gb(2),gh(2),gm(2),gr(2),gt3,gwls,txpair
      common /initia/ vin,rin,ain,inin,inink
      common /iterat/ si,siold,epsi,xmix,xmix0,xmax,maxi,ii,inxt,iaut
      common /mespar/ amsig,amome,amrho,gsigs,gomes,grhos
      common /mathco/ zero,one,two,half,third,pi
      common /nucnuc/ amas,nama,nneu,npro,jmax
      common /optopt/ icm,icou,it1,it2,ncut
      common /pair  / ga(2),gg(2),del(2),spk(2),spk0(2),dec(2),pwi
      common /physco/ amu,hqc,alphi,r0
      common /tapes / l6,lin,lou,lwin,lwou,lplo,laka,lvpp,lqrpa
      common /textex/ nucnam,tp(2),tis(2),tit(2),tl(0:20),txtfor
      common /ugugug/ itbl(2),jbl(2),ipbl(2),nbl(2),nrbl(2)
      common /woodsa/ v0,akv,vso(2),r0v(2),av(2),rso(2),aso(2)
      common /cpara/ a_s,b_s,c_s,d_s,a_v,b_v,c_v,d_v,a_tv,dsat 
c
c
c---- nucleus
      data nucnam/' O'/,nama/16/
      data jmax/9/
c
c---- blocking structure (for neutrons and protons)
c     itbl = 0: no blockung    = 1: one orbit is blocked
c     jbl, ipbl, nrbl: quantum numbers j,ip,nr of the blocked level
c      putting itbl 0 no blocking
c      jbl : refers to j 
c      ipbl: refers to parity 1 (+) 2 (-)
c      nrbl: refers to the radial quantum number
c      example: for neutrons (first numbers) 3 1 1 ---> 1d5/2        
c      data itbl/0,0/,jbl/0,0/,ipbl/0,0/,nrbl/0,0/
c     data itbl/1,0/,jbl/1,0/,ipbl/2,0/,nrbl/1,0/
c
c---- options
c     center of mass:
      data icm/0/
c     protons or neutrons of both
      data it1/1/,it2/2/
c
c---- iteration
      data maxi/500/,si/1.0d0/,epsi/0.000001/
      data iaut/0/,inxt/3/
      data xmix0/0.1d0/,xmix/0.1d0/,xmax/1.1d0/
c---- force parameters
c---------------------------------------------------------------
c      data txtfor/'DD-ME1'/
c      data amu/939.0/
c      data amsig/549.5255/,amome/783.000/,amrho/763.0/
c      data gsigs/10.4434/,gomes/12.8939/,grhos/3.8053/
c      data b_s/0.9781/,c_s/1.5342/
c      data b_v/0.8525/,c_v/1.3566/
c      data a_tv/0.5008/
c      data dsat/0.152/
c---------------------------------------------------------------
c      data txtfor/'a4=30'/
      data amu/939.0/
      data amsig/550.1394/,amome/783.000/,amrho/763.0/
      data gsigs/10.4898/,gomes/12.9441/,grhos/3.3822/
      data b_s/1.1073/,c_s/1.5949/
      data b_v/0.9023/,c_v/1.2961/
      data a_tv/0.8904/
      data dsat/0.152/
c---------------------------------------------------------------
c      data txtfor/'a4=32'/
c      data amu/939.0/
c      data amsig/550.1096/,amome/783.000/,amrho/763.0/
c      data gsigs/10.4906/,gomes/12.9459/,grhos/3.6722/
c      data b_s/1.1084/,c_s/1.5916/
c      data b_v/0.9058/,c_v/1.2952/
c      data a_tv/0.6449/
c      data dsat/0.152/
c---------------------------------------------------------------
c      data txtfor/'a4=34'/
c      data amu/939.0/
c      data amsig/549.9681/,amome/783.000/,amrho/763.0/
c      data gsigs/10.4902/,gomes/12.9492/,grhos/3.9511/
c      data b_s/1.1099/,c_s/1.5866/
c      data b_v/0.9091/,c_v/1.2917/
c      data a_tv/0.4252/
c      data dsat/0.152/
c---------------------------------------------------------------
c      data txtfor/'a4=36'/
c      data amu/939.0/
c      data amsig/550.0609/,amome/783.000/,amrho/763.0/
c      data gsigs/10.4911/,gomes/12.9483/,grhos/4.2165/
c      data b_s/1.1342/,c_s/1.6111/
c      data b_v/0.9235/,c_v/1.3006/
c      data a_tv/0.2110/
c      data dsat/0.152/
c---------------------------------------------------------------
c      data txtfor/'a4=38'/
c      data amu/939.0/
c      data amsig/549.1997/,amome/783.000/,amrho/763.0/
c      data gsigs/10.4859/,gomes/12.9631/,grhos/4.4638/
c      data b_s/1.1154/,c_s/1.6079/
c      data b_v/0.9452/,c_v/1.3560/
c      data a_tv/0.0741/
c      data dsat/0.152/
c---------------------------------------------------------------
c      data txtfor/'a4=36'/
c      data amu/939.0/
c      data amsig/549.5255/,amome/783.000/,amrho/763.0/
c      data gsigs/10.4453/,gomes/12.8957/,grhos/4.1714/
c      data b_s/0.9793/,c_s/1.5294/
c      data b_v/0.8615/,c_v/1.3635/
c      data a_tv/0.2291/
c      data dsat/0.152/
c---------------------------------------------------------------
c      data txtfor/'0.93'/
c      data amu/939.0/
c      data amsig/550.0/,amome/783.000/,amrho/763.0/
c      data gsigs/10.3657/,gomes/12.7809/,grhos/3.7023/
c      data b_s/2.4763/,c_s/3.2562/
c      data b_v/1.0974/,c_v/1.3419/
c      data a_tv/0.5467/
c      data dsat/0.152/
c---------------------------------------------------------------
c      data txtfor/'0.95'/
c      data amu/939.0/
c      data amsig/550.0/,amome/783.000/,amrho/763.0/
c      data gsigs/10.3839/,gomes/12.8028/,grhos/3.7154/
c      data b_s/1.7576/,c_s/2.2680/
c      data b_v/0.7375/,c_v/0.9040/
c      data a_tv/0.5499/
c      data dsat/0.152/
c---------------------------------------------------------------
c      data txtfor/'0.97'/
c      data amu/939.0/
c      data amsig/550.0/,amome/783.000/,amrho/763.0/
c      data gsigs/10.3730/,gomes/12.7828/,grhos/3.7337/
c      data b_s/1.2614/,c_s/1.6829/
c      data b_v/0.7052/,c_v/0.9126/
c      data a_tv/0.5500/
c      data dsat/0.152/
c---------------------------------------------------------------
c      data txtfor/'0.99'/
c      data amu/939.0/
c      data amsig/550.0/,amome/783.000/,amrho/763.0/
c      data gsigs/10.3859/,gomes/12.8000/,grhos/3.7300/
c      data b_s/1.1785/,c_s/1.7127/
c      data b_v/0.9210/,c_v/1.3251/
c      data a_tv/0.5500/
c      data dsat/0.152/
c---------------------------------------------------------------
c      data txtfor/'1.01'/
c      data amu/939.0/
c      data amsig/550.0/,amome/783.000/,amrho/763.0/
c      data gsigs/10.4275/,gomes/12.8585/,grhos/3.7323/
c      data b_s/1.1174/,c_s/1.7403/
c      data b_v/0.9892/,c_v/1.5560/
c      data a_tv/0.5500/
c      data dsat/0.152/
c---------------------------------------------------------------
c
c---- Coulomb-field: not at all (0), direct term (1), plus exchange (2)
      data icou/1/
c---------------------------------------------------------------
c
c
c---- Gogny D1
c     data txpair/'Gogny D1'/
c     data gr/0.7d0,1.2d0/,gw/-402.4d0,-21.3d0/,gb/-100.d0,-11.77d0/ 
c     data gh/-496.2d0,37.27d0/,gm/-23.56,-68.81/
c     data gwls/-115.d0/,gt3/1350.d0/
c---------------------------------------------------------------
c
c
c---- Gogny DSA1
      data txpair/'Gogny DSA1'/
      data gr/0.7d0,1.2d0/,gw/-1720.30d0, 103.639d0/,
     &                     gb/ 1300.00d0,-163.483d0/,
     &                     gh/-1813.53d0, 162.812d0/,
     &                     gm/ 1397.60d0,-223.934d0/
      data gwls/-130.d0/,gt3/1350.d0/
c---------------------------------------------------------------
c
c---- pairing
      data dec/0.d0,0.d0/,spk0/0.d0,0.d0/
      data del/6.d0,6.d0/
      data ala/-7.d0,-7.d0/
c     data ga/22.,27./
      data ga/0.0,0.0/
c
c
c---- parameters of the initial potentials
c     inin = 0: fields read, 1: saxon-wood,
      data inin/1/
c     inink = 0: kappa read, 1: constant delta
      data inink/1/
c
c     Saxon-Woods parameter von Koepf und Ring, Z.Phys. (1991)
      data v0/-71.28/,akv/0.4616/
      data r0v/1.2334,1.2496/,av/0.615,0.6124/
      data vso/11.1175,8.9698/
      data rso/1.1443,1.1401/,aso/0.6476,0.6469/
c---- Saxon-Woods parameter for test without Coulomb
c      data v0/-71.28/,akv/0.4616/
c      data r0v/1.2334,1.2334/,av/0.6150,0.6150/
c      data vso/11.1175,11.1175/
c      data rso/1.1443,1.1443/,aso/0.6476,0.6476/
c
c     data vin/-55.0/,rin/1.0/,qin/1.3/,ain/0.6/
c     Woods-Saxon Potential Dudek
c     data wsv0/-49.6/,wsv1/0.86/,wsr/1.347,1.275/,wsa/0.7/
c
c---- basis parameters:
c     number of major oscillator shells 
      data n0f/2/,n0b/20/
c     oscillator length b0f (is calcuated for b0f <= 0)
      data b0/-2.320/
c
c
c---- tapes
      data l6/10/,lin/3/,lou/6/,lwin/1/,lwou/2/
      data lplo/11/,laka/12/,lvpp/13/
      data lqrpa/14/
c
c---- fixed texts
      data tp/'+','-'/,tis/'n','p'/,tit/'Neutron:','Proton: '/
      data tl/'s','p','d','f','g','h','i','j','k','l','m',
     &            'n','o','P','q','r','S','t','u','v','w'/
c
c
c---- physical constants
      data hqc/197.328284d0/,r0/1.2/,alphi/137.03602/
c
c---- mathemathical constants
c     are determined in GFV
c      data zero/0.0d0/,one/1.d0/,two/2.d0/
c      data half/0.5d0/,third/0.333333333333333333d0/
c      data pi/3.141592653589793d0/
c
c
c---- fixed occupation patterns
c     O-16
c     data ioc/1,1,0,1,0,0,0,0,0,0, 32*0,
c    &         1,1,0,1,0,0,0,0,0,0, 32*0/
c
c     Pb-208
c     data ioc/3,3,2,3,2,2,1,2,1,1, 0,1,1,29*0,
c    &         3,2,2,2,2,1,1,1,1,0, 0,1,0,29*0/
c
c     GG-298
c     data ioc/4,3,3,3,3,2,2,2,2,1, 1,1,1,0,0,1,26*0,
c    &         3,2,2,3,2,2,1,2,1,0, 0,1,1,0,0,0,26*0/
c
c---- fields O-16 for NL1, ngh = 12
c     data sig/0.d0,
c    1 -.197896732795d+00, -.203336593050d+00, -.175178199706d+00,
c    2 -.110773903644d+00, -.492821497342d-01, -.155056088258d-01,
c    3 -.370467731601d-02, -.752571143561d-03, -.128392213020d-03,
c    4 -.178840524301d-04, -.123043868927d-06, -.138401023191d-05/
c     data ome/0.d0,
c    1  .122884775525d+00,  .128313360162d+00,  .111273919274d+00,
c    2  .678286964552d-01,  .271388311726d-01,  .717766421530d-02,
c    3  .140426026681d-02,  .243999373057d-03,  .378195438601d-04,
c    4  .312885710667d-05,  .507556868833d-06, -.331104601547d-06/
c     data rho/0.d0,
c    1 -.402717077863d-03, -.401598408644d-03, -.327222122144d-03,
c    2 -.134890782160d-03,  .226171401831d-04,  .537452482103d-04,
c    3  .302903348538d-04,  .103608532225d-04,  .228698677638d-05,
c    4  .197570927351d-06,  .514723017016d-07, -.380613801692d-07/
c     data cou/0.d0,
c    1  .280242732120d-01,  .268490299578d-01,  .243582917371d-01,
c    2  .209044213183d-01,  .173601945696d-01,  .143915626933d-01,
c    3  .121166187436d-01,  .103808124163d-01,  .901598395252d-02,
c    4  .790128300969d-02,  .694924512594d-02,  .607533630278d-02/
c
c-end-DEFAULT
      end
c
