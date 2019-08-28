# def main():
#     proj = signac.init_project("proj", root=proj_root)
#     logger.info("current project: %s" % proj.workspace())

#     talys_proj = signac.get_project(root="../")
#     logger.info("talys project: %s" % talys_proj.workspace())

#     hfb_qrpa_proj = signac.get_project(root="../hfb_qrpa/")
#     logger.info("hfb+qrpa project: %s" % hfb_qrpa_proj.workspace())

#     # cross section vs energy @ aggregated mass number, for each temperature
#     for temperature, talys_jobs in talys_proj.find_jobs(
#         {"proton_number": 50, "astro": "n"}
#     ).groupby("temperature"):

#         job = proj.open_job({"proton_number": 50, "temperature": temperature}).init()

#         fig = Figure(figsize=(12.8, 6.4))
#         fig.suptitle(fr"$T_9$={temperature} MeV")
#         canvas = FigureCanvas(fig)
#         ax = fig.add_subplot(121)
#         ax_hfb = fig.add_subplot(122)

#         for talys_job in sorted(talys_jobs, key=lambda jb: jb.sp.neutron_number):
#             cross_section = data.read_cross_section(
#                 talys_job.fn(talys_api.cross_section_fn)
#             )

#             plotting.plot_cross_section(
#                 ax,
#                 cross_section["energy"],
#                 cross_section["compound"],
#                 color=STYLE[str(talys_job.sp.neutron_number)]["color"],
#                 linestyle=STYLE[str(talys_job.sp.neutron_number)]["linestyle"],
#                 label=f"{50 + talys_job.sp.neutron_number - 1}",
#                 title=fr"T-dep. RPA",
#                 legend=False,
#             )

#             # add HFB+QRPA data
#             hfb_qrpa_job = next(
#                 iter(
#                     hfb_qrpa_proj.find_jobs(
#                         filter=dict(
#                             astro="n",
#                             neutron_number=talys_job.sp.neutron_number,
#                             proton_number=50,
#                         )
#                     )
#                 )
#             )

#             cross_section = data.read_cross_section(
#                 hfb_qrpa_job.fn(talys_api.cross_section_fn)
#             )

#             plotting.plot_cross_section(
#                 ax_hfb,
#                 cross_section["energy"],
#                 cross_section["compound"],
#                 color=STYLE[str(talys_job.sp.neutron_number)]["color"],
#                 linestyle=STYLE[str(talys_job.sp.neutron_number)]["linestyle"],
#                 label=f"{50 + talys_job.sp.neutron_number - 1}",
#                 title=fr"HFB-QRPA",
#                 legend=False,
#             )

#         props = dict(facecolor="white", alpha=0.8, edgecolor="white")
#         labelLines(ax.get_lines(), align=False, fontsize=7, bbox=props)
#         labelLines(ax_hfb.get_lines(), align=False, fontsize=7, bbox=props)

#         png_fn = "cross_section_all_isotopes.png"
#         canvas.print_png(job.fn(png_fn))
#         logger.info("Saved %s" % job.fn(png_fn))

#     # neutron capture rate vs mass number (for each temperature)
#     for temperature, talys_jobs in talys_proj.find_jobs(
#         {"proton_number": 50, "astro": "y"}
#     ).groupby("temperature"):

#         job = next(
#             iter(proj.find_jobs(filter=dict(temperature=temperature, proton_number=50)))
#         )

#         cols = ["mass_number", "capture_rate"]
#         rate_df = pd.DataFrame(columns=cols)
#         rate_hfb_df = pd.DataFrame(columns=cols)

#         for talys_job in sorted(talys_jobs, key=lambda jb: jb.sp.neutron_number):
#             df = talys_api.read_neutron_capture_rate(talys_job)
#             #  find closest temperature to the job's temperature
#             closest_df = df.iloc[(df["T9"] - temperature).abs().argsort()[:1]]
#             row = {
#                 "mass_number": talys_job.sp.proton_number
#                 + talys_job.sp.neutron_number
#                 - 1,
#                 "capture_rate": closest_df.iloc[0, 1],
#             }
#             rate_df.loc[len(rate_df)] = row

#             # add HFB+QRPA data
#             hfb_qrpa_job = next(
#                 iter(
#                     hfb_qrpa_proj.find_jobs(
#                         filter=dict(
#                             astro="y",
#                             neutron_number=talys_job.sp.neutron_number,
#                             proton_number=50,
#                         )
#                     )
#                 )
#             )
#             df = talys_api.read_neutron_capture_rate(hfb_qrpa_job)
#             #  find closest temperature to the job's temperature
#             closest_df = df.iloc[(df["T9"] - temperature).abs().argsort()[:1]]
#             row = {
#                 "mass_number": 50 + talys_job.sp.neutron_number - 1,
#                 "capture_rate": closest_df.iloc[0, 1],
#             }
#             rate_hfb_df.loc[len(rate_df)] = row

#         fig = Figure(figsize=(6.4, 6.4))
#         canvas = FigureCanvas(fig)
#         ax = fig.add_subplot(111)

#         plotting.plot_capture_rate_vs_mass(
#             ax,
#             rate_df.iloc[:, 0],
#             rate_df.iloc[:, 1],
#             label="T-dep. RPA",
#             color="C0",
#             title=fr"$T_9$={temperature} MeV",
#         )
#         plotting.plot_capture_rate_vs_mass(
#             ax,
#             rate_hfb_df.iloc[:, 0],
#             rate_hfb_df.iloc[:, 1],
#             label="HFB+QRPA",
#             color="black",
#         )

#         png_fn = "capture_rate_v_mass.png"
#         canvas.print_png(job.fn(png_fn))
#         logger.info("Saved %s" % job.fn(png_fn))


# def main():
#     proj = signac.init_project("proj", root=proj_root)
#     logger.info("current project: %s" % proj.workspace())

#     talys_proj = signac.get_project(root="../")
#     logger.info("talys project: %s" % talys_proj.workspace())

#     hfb_qrpa_proj = signac.get_project(root="../hfb_qrpa/")
#     logger.info("hfb+qrpa project: %s" % hfb_qrpa_proj.workspace())

#     # cross section vs energy @ fixed mass number
#     for neutron_number, talys_jobs in talys_proj.find_jobs(
#         {"proton_number": 50, "astro": "n"}
#     ).groupby("neutron_number"):

#         job = proj.open_job(
#             {"proton_number": 50, "neutron_number": neutron_number}
#         ).init()

#         atomic_symbol, mass_number = util.get_nucleus(50, neutron_number, joined=False)
#         text = r"${}^{%d}$%s(n,$\gamma$)${}^{%d}$%s" % (
#             mass_number - 1,
#             atomic_symbol,
#             mass_number,
#             atomic_symbol,
#         )

#         fig = Figure(figsize=(6.4, 6.4))
#         fig.suptitle(text)
#         canvas = FigureCanvas(fig)
#         ax = fig.add_subplot(111)

#         for talys_job in sorted(talys_jobs, key=lambda jb: jb.sp.temperature):
#             cross_section = data.read_cross_section(
#                 talys_job.fn(talys_api.cross_section_fn)
#             )

#             plotting.plot_cross_section(
#                 ax,
#                 cross_section["energy"],
#                 cross_section["compound"],
#                 color=STYLE[str(talys_job.sp.temperature)]["color"],
#                 linestyle=STYLE[str(talys_job.sp.temperature)]["linestyle"],
#                 label=f"T={talys_job.sp.temperature}",
#             )

#         # add HFB+QRPA data
#         hfb_qrpa_job = next(
#             iter(
#                 hfb_qrpa_proj.find_jobs(
#                     filter=dict(
#                         astro="n", neutron_number=neutron_number, proton_number=50
#                     )
#                 )
#             )
#         )

#         cross_section = data.read_cross_section(
#             hfb_qrpa_job.fn(talys_api.cross_section_fn)
#         )

#         plotting.plot_cross_section(
#             ax,
#             cross_section["energy"],
#             cross_section["compound"],
#             color="black",
#             linestyle="-",
#             label=f"HFB-QRPA",
#         )

#         png_fn = "cross_section_all_T.png"
#         canvas.print_png(job.fn(png_fn))
#         logger.info("Saved %s" % job.fn(png_fn))

#     # neutron capture rate vs temperature @ fixed mass number
#     for neutron_number, talys_jobs in talys_proj.find_jobs(
#         {"proton_number": 50, "astro": "y"}
#     ).groupby("neutron_number"):

#         job = next(
#             iter(
#                 proj.find_jobs(
#                     filter=dict(neutron_number=neutron_number, proton_number=50)
#                 )
#             )
#         )

#         atomic_symbol, mass_number = util.get_nucleus(50, neutron_number, joined=False)
#         text = r"${}^{%d}$%s(n,$\gamma$)${}^{%d}$%s" % (
#             mass_number - 1,
#             atomic_symbol,
#             mass_number,
#             atomic_symbol,
#         )

#         rate_df = pd.DataFrame()

#         for talys_job in sorted(talys_jobs, key=lambda jb: jb.sp.temperature):
#             df = talys_api.read_neutron_capture_rate(talys_job)
#             #  find closest temperature to the job's temperature
#             closest_df = df.iloc[
#                 (df["T9"] - talys_job.sp.temperature).abs().argsort()[:1]
#             ]
#             rate_df = rate_df.append(closest_df)

#         # add HFB+QRPA data
#         hfb_qrpa_job = next(
#             iter(
#                 hfb_qrpa_proj.find_jobs(
#                     filter=dict(
#                         astro="y", neutron_number=neutron_number, proton_number=50
#                     )
#                 )
#             )
#         )
#         df = talys_api.read_neutron_capture_rate(hfb_qrpa_job)
#         rate_hfb_df = df[df.index.isin(rate_df.index)]

#         fig = Figure(figsize=(6.4, 6.4))
#         canvas = FigureCanvas(fig)
#         ax = fig.add_subplot(111)

#         plotting.plot_capture_rate_vs_temp(
#             ax,
#             rate_df.iloc[:, 0],
#             rate_df.iloc[:, 1],
#             label="T-dep. RPA",
#             color="C0",
#             title=text,
#         )
#         plotting.plot_capture_rate_vs_temp(
#             ax,
#             rate_hfb_df.iloc[:, 0],
#             rate_hfb_df.iloc[:, 1],
#             label="HFB+QRPA",
#             color="black",
#         )

#         png_fn = "capture_rate_v_T.png"
#         canvas.print_png(job.fn(png_fn))
#         logger.info("Saved %s" % job.fn(png_fn))


# @Project.pre(lambda job: job.isfile(talys_api.cross_section_fn(job)))

#     cross_section = data.read_cross_section(job.fn(talys_api.cross_section_fn(job)))


#     atomic_symbol, mass_number = util.get_nucleus(
#         job.sp.proton_number, job.sp.neutron_number, joined=False
#     )
#     text = r"${}^{%d}$%s(n,$\gamma$)${}^{%d}$%s" % (
#         mass_number - 1,
#         atomic_symbol,
#         mass_number,
#         atomic_symbol,
#     )

#     plotting.plot_cross_section(
#         ax,
#         cross_section["energy"],
#         cross_section["xs"],
#         color="black",
#         label=f"HFB-QRPA",
#         title=text,
#     )
