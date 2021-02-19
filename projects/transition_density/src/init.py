"""Initialize the project's data space."""
import logging

from decimal import Decimal
import signac
import mypackage.util as util

# Runtime is approx 30 mins

nuclei = {"50": (76, 86, 96), "58": (82,)}


def main():
    """Main entry point."""
    project = signac.init_project("transition_density", workspace="workspace")

    for proton_number, neutron_numbers in nuclei.items():
        for neutron_number in neutron_numbers:
            statepoint = dict(
                # atomic number Z
                proton_number=int(proton_number),  # fixed atomic number
                # neutron number N
                neutron_number=int(neutron_number),
                # nucleus angular momentum
                angular_momentum=1,  #
                # nucleus parity
                parity="-",  #
                # system temperature in MeV
                temperature=0.0,
                # transition energy in MeV
                transition_energy=str(round(Decimal(0.42), 2)),  # 0.42 is random
            )
            project.open_job(statepoint).init()

    for job in project:
        job.doc.setdefault(
            "nucleus",
            util.get_nucleus(
                proton_number=job.sp.proton_number, neutron_number=job.sp.neutron_number
            ),
        )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
