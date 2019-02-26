"""This module contains functions for generating the code parameter files."""
import os
from jinja2 import Environment, FileSystemLoader
# pass folder containing the templates
file_loader = FileSystemLoader('src/templates')
env = Environment(loader=file_loader)
import logging
logger = logging.getLogger(__name__)


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


class NameMapping:
    """Mapping from executable names to what they represent."""

    def __init__(self, prefix={
                                'zero' : {
                                    'ground' : 'dish',
                                    'excited' : 'ztes'
                                },
                                'finite' : {
                                    'ground' : 'skys',
                                    'excited' : 'ftes' 
                                }
                            }, 
                       input_suffix={'ground': "_dis.dat",
                                     'excited': "_start.dat"},
                       wel_suffix={'zero': "_qrpa.wel",
                                   'finite': "_rpa.wel"},
                       bins_suffix=('_arpa.bin', '_brpa.bin', '_xrpa.bin',
                                     '_yrpa.bin' ,'_erpa.bin' ,'_c_erpa.bin'),
                       out_suffix={'isoscalar' : {'excitation': '_excskal.out', 'lorentzian': '_lorskal.out'},
                                   'isovector' : {'excitation': '_excvec.out', 'lorentzian': '_lorvec.out'}}
                       ):

        self._prefix = prefix
        self._input_suffix = input_suffix
        self._wel_suffix = wel_suffix
        self._bins_suffix = bins_suffix
        self._out_suffix = out_suffix

    def exec_file(self, temp, state):
        return self._prefix[temp][state]
    
    def mock_exec_file(self, temp, state):
        return self._prefix[temp][state] + '.sh'

    def input_file(self, temp, state):
        return self.input_files(temp, state)[0]

    def input_files(self, temp=None, state=None):
        files = []
        if temp and state:
            files.append(self._prefix[temp][state] + self._input_suffix[state])
        elif temp and not state:
            # loop of state
            for s in ('ground', 'excited'):
                files.append(self._prefix[temp][s] + self._input_suffix[s])
        elif state and not temp:
            # loop over temp
            for t in ('zero', 'finite'):
                files.append(self._prefix[t][state] + self._input_suffix[state])
        else:
            # loop over both
            for t in ('zero', 'finite'):
                for s in ('ground', 'excited'):
                    files.append(self._prefix[t][s] + self._input_suffix[s])
        return tuple(files)

    def bin_files(self, temp=None):
        """List of .bin files containing matrix elements."""
        files = []
        if temp:
            for suffix in self._bins_suffix:
                files.append(self._prefix[temp]['excited'] + suffix)
        else:
            for t in ('zero', 'finite'):
                for suffix in self._bins_suffix:
                    files.append(self._prefix[t]['excited'] + suffix)
        return tuple(files)

    def out_file(self, temp, skalvec, lorexc):
        return self._prefix[temp]['excited'] + self._out_suffix[skalvec][lorexc]

    def out_files(self, temp):
        files = []
        for skalvec in 'isoscalar', 'isovector':
            for lorexc in 'excitation', 'lorentzian':
                files.append(self.out_file(temp, skalvec, lorexc))
        return tuple(files)



    def stdout_file(self, temp, state):
        return self._prefix[temp][state] + '_stdout.txt'

    def stderr_file(self, temp, state):
        return self._prefix[temp][state] + '_stderr.txt'
    
    def wel_file(self, temp):
        """Return corresponding .wel file."""
        return self._prefix[temp]['ground'] + self._wel_suffix[temp]




class GenerateInputs:
    """Generates input files dish_dis.dat, skys_dis.dat and (z|f)tes_start.dat."""

    def __init__(self, nucleus="NI62", angular_momentum=1, parity="-", temperature=2.0, transition_energy=9.78,
                    out_path=os.getcwd(), load_matrix=False, mapping=NameMapping()):
        """Args:
            nucleus: nucleus under consideration, eg. NI56, NI60, NI62, NI68, ZR90, SN132, PB208
            angular_momentum: 0 or 1
            parity: + or -
            temperature: eg. 2.0 (in MeV)
            transition_energy: eg. 9.78 (in MeV)
            load_matrix: flag that controls the matrix elements calculation, default is to perform the calculation
            out_path: path of folder to write files to"""

        PARITY = {"-" : 0, "+": 1} # map to the parity as it is defined in the input files

        self._param = { # dictionary containing parameters for template substitution
            'transerg': transition_energy,
            'calc': int(not load_matrix), # do not calculate matrix when you load
            'xyprint': int(not load_matrix),
            'xyread': int(load_matrix),
            'xyprobe': int(load_matrix),
            'j': angular_momentum,
            'parity': PARITY[parity],
            'temp': temperature,
            'XA': nucleus}

        self._mapping = mapping
        self._out_path = out_path
        self._contents = self._fname_to_contents()

    def _fname_to_contents(self):
        """Mapping from input fname to contents"""
        contents = dict()
        for t in ('zero', 'finite'):
            for s in ('ground', 'excited'):
                fn = self._mapping.input_file(temp=t, state=s)
                contents[fn] = env.get_template(f"{t}_{s}.dat").render(param=self._param)
        return contents

    def write_param_files(self, temp=None, state=None):
        """Writes files to out_path (current folder by default)."""
        for fn in self._mapping.input_files(temp, state):
            fnpath = os.path.join(self._out_path, fn)
            with open(fnpath, "w") as f:
                f.write(self._contents[fn])
            logger.info("Wrote %s." % fnpath)


def main():
    logging.basicConfig(level=logging.INFO)

    code = NameMapping()
    print(code.input_file(temp='zero', state='excited'))
    print(code.input_files(state='ground'))
    print(code.isovec_file(temp='zero'))

    my_inputs = GenerateInputs(nucleus="NI62", angular_momentum=1, parity="-", temperature=2.0, transition_energy=9.78, mapping=code)
    my_inputs.write_param_files()



if __name__ == '__main__':
    main()