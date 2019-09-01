# def my_pivot(df):
#     return pd.pivot_table(
#         df,
#         index=["model", "temperature", "excitation_energy"],
#         values=["strength_function_fm", "strength_function_mb"],
#         columns=["proton_number", "neutron_number", "mass_number"],
#     )
#
# idx = pd.IndexSlice
# tiny = df.loc[idx[50, 76, 50 + 76, 0.0, 0.90:1.10], ("strength_function_fm_yifei", "strength_function_fm_talys")]
#
# def core(df, α=.05):
#     mask = (df > df.quantile(α)).all(1) & (df < df.quantile(1 - α)).all(1)
#     return df[mask]
#
# (df.select_dtypes(include=[np.number])
#    .pipe(core)
#
#  ax.scatter(x='carat', y='depth', data=df, c='k', alpha=.15)
