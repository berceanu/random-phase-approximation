#!/usr/bin/env python3
import pandas as pd
import re
import logging
logger = logging.getLogger(__name__)
from jinja2 import Environment, FileSystemLoader
# pass folder containing the templates
file_loader = FileSystemLoader('.')
env = Environment(loader=file_loader)

def extract_transitions(stdoutfn):
    first_marker = "1=n/2=p       E/hole      E/particle  XX-YY/%"
    last_marker = "Sum XX-YY after normalization *"
    #
    infn = stdoutfn
    outfn = 'dipole_transitions.txt'
    #
    with open(infn, 'r') as infile, open(outfn, 'w') as outfile:
        copy = False
        for line in infile:
            if first_marker in line.strip():
                copy = True
            elif last_marker in line.strip():
                copy = False
            elif copy:
                outfile.write(line)
    logger.info('Wrote %s' % outfn)

def get_table(txtfn):
    dip_conf = pd.read_csv('dipole_transitions.txt', sep=r'\s+', header=None,
         usecols=[0, 1, 3, 4, 6, 7], 
                                names=['n_or_p', 'hole_energy', 'particle_energy', 'from_state', 'to_state', 'transition_amplitude'])

    with pd.option_context('mode.use_inf_as_null', True):
        dip_conf = dip_conf.dropna()
    
    # filtered_conf = dip_conf[dip_conf.transition_amplitude > 1]

    sorted_conf = dip_conf.sort_values(by=['n_or_p', 'transition_amplitude'], ascending=[False, False])
    # dropped_conf = sorted_conf.drop(sorted_conf.columns[[1, 2]], axis=1)
    df = sorted_conf.replace({'n_or_p' : {1: '\u03BD', 2: '\u03C0'}})

    def match_split(orbital_frac):
        regex = re.compile(r'(?P<orbital>\d+[a-z]+)(?P<frac>\d+\/\d+)')
        m = regex.search(orbital_frac)
        return m.group('orbital'), m.group('frac')

    def frac_to_html(frac):
        numerator, denominator = frac.split('/')
        return f"<sub>{numerator}&frasl;{denominator}</sub>"

    table = []
    for idx in df.index:
        np_mapping = {'\u03BD': '&nu;', '\u03C0': '&pi;'}
        np = np_mapping[df.loc[idx, 'n_or_p']]

        from_state = df.loc[idx, 'from_state']
        from_state_orbital, from_state_frac = match_split(from_state)
        from_state_frac_html = frac_to_html(from_state_frac)

        to_state = df.loc[idx, 'to_state']
        to_state_orbital, to_state_frac = match_split(to_state)
        to_state_frac_html = frac_to_html(to_state_frac)    

        transition_amplitude = df.loc[idx, 'transition_amplitude']

        row = {'transition': f"{np}{from_state_orbital}{from_state_frac_html}&rarr;{np}{to_state_orbital}{to_state_frac_html}",
                'amplitude': f"{transition_amplitude:.2f}"}
        table.append(row)

    return table


def main():
    logging.basicConfig(level=logging.INFO)

    extract_transitions('ztes_stdout.txt') # 'ftes_stdout.txt'
    table = get_table('dipole_transitions.txt')
    
    output = env.get_template("dipole_transitions.html").render(title='Dipole transition amplitudes', table=table)

    with open('final_table.html', 'w') as f:
        f.write(output)
    
    logger.info('Wrote %s' % 'final_table.html')

if __name__ == '__main__':
    main()