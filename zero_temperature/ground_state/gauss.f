c======================================================================c

      blockdata gauss

c======================================================================c
c
c     24 Meshpoints 
c     ph  =  wh * exp(-xh)
c     pl  =  wl * exp(-xl)
c
c     \int_0^\infty  f(z) exp(-z^2) dz   =   \sum_i f(xh(i)) ph(i)
c     \int_0^\infty  f(z) dz             =   \sum_i f(xh(i)) wh(i) 
c
c----------------------------------------------------------------------c
      include 'dis.par'
      implicit double precision (a-h,o-z)
c
      common /gaussh/ xh(ngh),wh(ngh),ph(ngh)
c
      DATA XH  /
     1  0.14280123870E+00,   0.42850006422E+00,   0.71448878167E+00,
     2  0.10009634996E+01,   0.12881246749E+01,   0.15761790120E+01,
     3  0.18653415312E+01,   0.21558378712E+01,   0.24479069023E+01,
     4  0.27418037481E+01,   0.30378033382E+01,   0.33362046535E+01,
     5  0.36373358762E+01,   0.39415607339E+01,   0.42492864360E+01,
     6  0.45609737579E+01,   0.48771500775E+01,   0.51984265346E+01,
     7  0.55255210861E+01,   0.58592901964E+01,   0.62007735580E+01,
     8  0.65512591671E+01,   0.69123815322E+01,   0.72862765944E+01,
     9  0.76758399375E+01,   0.80851886542E+01,   0.85205692841E+01,
     &  0.89923980014E+01,   0.95209036770E+01,   0.10159109246E+02/
      DATA WH  /  
     1  0.28561852135E+00,   0.28581135848E+00,   0.28619873156E+00,
     2  0.28678408219E+00,   0.28757268483E+00,   0.28857178792E+00,
     3  0.28979081369E+00,   0.29124162795E+00,   0.29293889597E+00,
     4  0.29490054693E+00,   0.29714837836E+00,   0.29970884449E+00,
     5  0.30261409110E+00,   0.30590332637E+00,   0.30962465909E+00,
     6  0.31383759920E+00,   0.31861651858E+00,   0.32405553693E+00,
     7  0.33027558141E+00,   0.33743486518E+00,   0.34574493918E+00,
     8  0.35549621580E+00,   0.36710041249E+00,   0.38116510200E+00,
     9  0.39863393572E+00,   0.42107475306E+00,   0.45134627625E+00,
     &  0.49542706484E+00,   0.56898437464E+00,   0.73724102025E+00/
      DATA PH  /  
     1  0.27985311752E+00,   0.23786890496E+00,   0.17177615692E+00,
     2  0.10529876370E+00,   0.54718970932E-01,   0.24061272766E-01,
     3  0.89321783603E-02,   0.27913248290E-02,   0.73177355697E-03,
     4  0.16027733468E-03,   0.29187419042E-04,   0.43942869363E-05,
     5  0.54335161342E-06,   0.54755546193E-07,   0.44568227752E-08,
     6  0.28993590128E-09,   0.14889573491E-10,   0.59484305161E-12,
     7  0.18166245763E-13,   0.41524441097E-15,   0.69232479096E-17,
     8  0.81536404730E-19,   0.65125672575E-21,   0.33457569558E-23,
     9  0.10294059972E-25,   0.17155731477E-28,   0.13325596118E-31,
     &  0.37716267271E-35,   0.24397475881E-39,   0.11095872480E-44/
c
c-end BLOCKDATA GAUSS
      end
