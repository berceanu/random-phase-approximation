"""Initialize the project's data space."""
import logging

import signac
import mypackage.util as util

# Runtime is approx 30 mins


def main():
    """Main entry point."""
    project = signac.init_project("transition_density", workspace="workspace")

    for neutron_number in (76, 86, 96):
        statepoint = dict(
            # atomic number Z
            proton_number=50,  # fixed atomic number
            # neutron number N
            neutron_number=neutron_number,
            # nucleus angular momentum
            angular_momentum=1,  #
            # nucleus parity
            parity="-",  #
            # system temperature in MeV
            temperature=0.0,
            # transition energy in MeV
            transition_energy=0.42,  # 0.42 is random
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
