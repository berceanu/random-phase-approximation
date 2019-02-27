def atomic_symbol_for_Z(atomic_number):
    """Determine the symbol for a given proton (atomic) number Z.

    >>> atomic_symbol_for_Z(1)
    ' H'
    >>> atomic_symbol_for_Z(118)
    'OG'
    >>> atomic_symbol_for_Z(53)
    ' I'
    """

    MAXZ = 118
    assert 0 < atomic_number <= MAXZ, "Wrong number of protons!"

    periodic_table = ('   HHELIBE B C N O FNENAMGALSI P SCLAR K'
                      'CASCTI VCRMNFECONICUZNGAGEASSEBRKRRBSR Y'
                      'ZRNBMOTCRURHPDAGCDINSNSBTE IXECSBALACEPR'
                      'NDPMSMEUGDTBDYHOERTMYBLUHFTA WREOSIRPTAU'
                      'HGTLPBBIPOATRNFRRAACTHPA UNPPUAMCMBKCFES'
                      'FMMDNOLRRFDBSGBHHSMTDSRGCNNHFLMCLVTSOG')
    assert len(periodic_table) == 2*MAXZ+2, "Error in periodic table!"

    atomic_symbol = periodic_table[2*atomic_number:2*atomic_number+2]
    assert len(atomic_symbol) == 2, "Error in atomic symbol selection!"

    return atomic_symbol


def get_nucleus(proton_number, neutron_number):
    """Return nuclide symbol, given the proton and neutron numbers.

    >>> get_nucleus(proton_number=50, neutron_number=82)
    'SN132'
    """

    atomic_symbol = atomic_symbol_for_Z(proton_number)
    mass_number = proton_number + neutron_number # A = Z + N
    return f'{atomic_symbol}{mass_number}'


def split_element_mass(job):
    mass_number = job.sp.proton_number + job.sp.neutron_number
    element = atomic_symbol_for_Z(job.sp.proton_number)
    element = element.title() # capitalize first letter only
    return element, mass_number


