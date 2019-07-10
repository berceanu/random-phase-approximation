#!/usr/bin/env python3
"""Custom dashboard module for rendering a card containing dipole transition amplitudes."""
from signac_dashboard.module import Module
from flask import render_template
import pandas as pd
import re
import logging

logger = logging.getLogger(__name__)


class DipoleTransitions(Module):
    def __init__(
        self,
        name="Dipole Transitions",
        context="JobContext",
        # ~/anaconda3/lib/python3.6/site-packages/signac_dashboard/templates/cards/
        template="cards/dipole_transitions.j2",
        **kwargs,
    ):
        super().__init__(name=name, context=context, template=template, **kwargs)

    def get_cards(self, job):
        """Returns a list of cards to show"""
        table = DipoleTransitions.get_table(job)
        if table is None:
            return []  # no card shown
        else:
            return [
                {
                    "name": self.name,
                    "content": render_template(self.template, table=table),
                }
            ]

    @staticmethod
    def get_table(job):
        def match_split(orbital_frac):
            regex = re.compile(r"(?P<orbital>\d+[a-z]+)(?P<frac>\d+\/\d+)")
            m = regex.search(orbital_frac)
            return m.group("orbital"), m.group("frac")

        def frac_to_html(frac):
            numerator, denominator = frac.split("/")
            return f"<sub>{numerator}&frasl;{denominator}</sub>"

        dip_conf_fn = "dipole_transitions.txt"
        if not job.isfile(dip_conf_fn):
            return None
        else:
            dip_conf = pd.read_csv(
                job.fn(dip_conf_fn),
                sep=r"\s+",
                header=None,
                usecols=[0, 1, 3, 4, 6, 7],
                names=[
                    "n_or_p",
                    "hole_energy",
                    "particle_energy",
                    "from_state",
                    "to_state",
                    "transition_amplitude",
                ],
            )
            with pd.option_context("mode.use_inf_as_null", True):
                dip_conf = dip_conf.dropna()  # drop inf values

            filtered_conf = dip_conf[dip_conf.transition_amplitude > 1]
            df = filtered_conf.sort_values(
                by=["n_or_p", "transition_amplitude"], ascending=[False, False]
            )

            table = []
            for idx in df.index:
                np_mapping = {1: "&nu;", 2: "&pi;"}
                neutron_proton = np_mapping[df.loc[idx, "n_or_p"]]

                from_state = df.loc[idx, "from_state"]
                from_state_orbital, from_state_frac = match_split(from_state)
                from_state_frac_html = frac_to_html(from_state_frac)

                to_state = df.loc[idx, "to_state"]
                to_state_orbital, to_state_frac = match_split(to_state)
                to_state_frac_html = frac_to_html(to_state_frac)

                transition_amplitude = df.loc[idx, "transition_amplitude"]

                row = {
                    "transition": (
                        f"{neutron_proton}{from_state_orbital}{from_state_frac_html}&rarr;"
                        f"{neutron_proton}{to_state_orbital}{to_state_frac_html}"
                    ),
                    "amplitude": f"{transition_amplitude:.2f}",
                }
                table.append(row)

            return table


def main():
    logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    main()
