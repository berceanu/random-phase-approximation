import pandas as pd
import signac
from mypackage.util import match_split, frac_to_html


def np_to_html(n_or_p):
    np_mapping = {1: "&nu;", 2: "&pi;"}
    return np_mapping[n_or_p]


def state_to_html(state):
    state_orbital, state_frac = match_split(state)
    state_frac_html = frac_to_html(state_frac)
    return state_orbital + state_frac_html


def row_to_html(row):
    np_html = np_to_html(row["n_or_p"])

    from_state_html = state_to_html(row["from_state"])
    to_state_html = state_to_html(row["to_state"])

    return f"{np_html}{from_state_html}&rarr;{np_html}{to_state_html}"


def transitions_table(fname):
    dip_conf = pd.read_csv(
        fname,
        sep=r"\s+",
        header=None,
        usecols=[0, 1, 3, 4, 6, 7],
        names=[
            "n_or_p",
            "hole_energy",
            "particle_energy",
            "from_state",
            "to_state",
            "amplitude",
        ],
        dtype={"n_or_p": pd.Int64Dtype()},
        # TODO pandas 1.0 , "from_state": pd.StringDtype(), "to_state": pd.StringDtype()}
    )
    # TODO remove
    # drop inf values
    # with pd.option_context("mode.use_inf_as_null", True):
    #     dip_conf = dip_conf.dropna()

    filtered_conf = dip_conf[dip_conf.amplitude > 1]

    df = filtered_conf.sort_values(by=["n_or_p", "amplitude"], ascending=[False, False])

    df["transition"] = df.apply(row_to_html, axis=1)

    return df.loc[:, ["transition", "amplitude"]]


def big_df(job):
    appended_data = []

    for id, v in job.doc.rpa_jobs.items():
        fname = id + "_dipole_transitions.txt"
        transition_energy = v["transition_energy"]
        print(fname, transition_energy)

        df = transitions_table(fname).set_index("transition")
        df2 = pd.concat([df], keys=[transition_energy], names=["transition_energy"])
        appended_data.append(df2)

    return pd.concat(appended_data)


def main():
    # df = transitions_table("b2a98e75404b2f2551dd82435e6bf0b0_dipole_transitions.txt")

    pr = signac.get_project()
    job = pr.open_job(id="9818e422162d9c46822bac85dba288c7")

    bdf = big_df(job)
    bdf = pd.read_hdf("dipole_transitions.h5", key="dipole_transitions")

    print(
        bdf.to_html(
            index=True,
            float_format="%.2f",
            classes="table is-bordered is-striped is-narrow is-hoverable is-fullwidth",
            escape=False,
        )
    )


# TODO remove file
if __name__ == "__main__":
    main()
