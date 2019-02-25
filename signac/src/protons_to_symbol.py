def atomic_symbol_for_Z(Z):
    """Determine the symbol for a given proton number Z.

    >>> atomic_symbol_for_Z(1)
    ' H'
    >>> atomic_symbol_for_Z(118)
    'OG'
    >>> atomic_symbol_for_Z(53)
    ' I'
    """

    MAXZ = 118
    assert 0 < Z <= MAXZ, "Wrong number of protons!"

    periodic_table = ('   HHELIBE B C N O FNENAMGALSI P SCLAR K'
                      'CASCTI VCRMNFECONICUZNGAGEASSEBRKRRBSR Y'
                      'ZRNBMOTCRURHPDAGCDINSNSBTE IXECSBALACEPR'
                      'NDPMSMEUGDTBDYHOERTMYBLUHFTA WREOSIRPTAU'
                      'HGTLPBBIPOATRNFRRAACTHPA UNPPUAMCMBKCFES'
                      'FMMDNOLRRFDBSGBHHSMTDSRGCNNHFLMCLVTSOG')
    assert len(periodic_table) == 2*MAXZ+2, "Error in periodic table!"

    atomic_symbol = periodic_table[2*Z:2*Z+2] # 3:4
    assert len(atomic_symbol) == 2, "Error in atomic symbol selection!"

    return atomic_symbol

def main():
    symbol = atomic_symbol_for_Z(50)
    print(symbol)

if __name__ == "__main__":
    import doctest
    doctest.testmod()    
    main()