#!/usr/bin/env python3
import signac


def main():
    rpa_proj = signac.get_project()

    for job in rpa_proj:
        if "talys_input" in job.doc:
            job.doc["z_file"] = job.doc.pop("talys_input")

    # check no jobs with old key are left
    for doc_key_exists, jobs in rpa_proj.groupbydoc(lambda doc: "talys_input" in doc):
        if doc_key_exists:
            for job in jobs:
                print(job.get_id())


if __name__ == "__main__":
    main()
