"""
02_descriptives_lpm_probit.py
Econometric Analysis of Firm Data – final project (Peru, Enterprise Surveys 2017 & 2023)

Input : peru_pooled.csv   (from 01_clean_peru.py)
Output: output/table1_summary_by_gender.csv     summary statistics, female- vs male-led firms
        output/table2_raw_did.csv               outcome means by wave x manager gender + raw DiD
        output/table3_lpm_probit_logit.csv      LPM vs probit vs logit (average partial effects)
        output/fig1_outcomes_by_gender_wave.png

Model (for each binary innovation outcome y):
    y_it = b0 + b1*female_mgr + b2*post + b3*female_mgr*post + controls + sector FE + region FE + u_it

b3 is the difference-in-differences term: did the gap between female- and male-led
firms change between 2017 and 2023 (the COVID period)?

Standard errors are clustered by firm (panelid), because the 358 panel firms
appear twice and their errors are likely correlated across waves.
"""

import os
import warnings
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")
os.makedirs("output", exist_ok=True)
df = pd.read_csv("peru_pooled.csv")

OUTCOMES = {
    "new_product":   "New product/service",
    "process_innov": "Process innovation",
    "rd":            "R&D spending",
    "website":       "Own website",
    "quality_cert":  "Quality certification",
}
CONTROLS = "ln_emp + ln_age + mgr_exp + exporter + foreign_owned + multi_estab + C(sector) + C(region)"
RHS = "female_mgr + post + female_mgr_x_post + " + CONTROLS


# =====================================================================
# TABLE 1 – summary statistics by manager gender (pooled 2017 + 2023)
# =====================================================================
summary_vars = {
    **OUTCOMES,
    "employees": "Employees (permanent full-time)",
    "firm_age": "Firm age (years)",
    "mgr_exp": "Manager experience (years)",
    "exporter": "Exporter (>=10% of sales)",
    "foreign_owned": "Foreign owned (>=10%)",
    "multi_estab": "Part of larger firm",
    "manufacturing": "Manufacturing",
    "female_worker_share": "Female share of workforce",
    "female_own_any": "Any female owner",
}
rows = []
for var, label in summary_vars.items():
    m = df.loc[df.female_mgr == 0, var].dropna()
    f = df.loc[df.female_mgr == 1, var].dropna()
    t, p = stats.ttest_ind(f, m, equal_var=False)          # Welch t-test
    rows.append({"Variable": label,
                 "Male-led mean": m.mean(), "Male-led sd": m.std(),
                 "Female-led mean": f.mean(), "Female-led sd": f.std(),
                 "Difference (F-M)": f.mean() - m.mean(), "p-value": p})
table1 = pd.DataFrame(rows).round(3)
n_m, n_f = (df.female_mgr == 0).sum(), (df.female_mgr == 1).sum()
table1.to_csv("output/table1_summary_by_gender.csv", index=False)
print(f"TABLE 1 – Summary statistics (male-led N={n_m}, female-led N={n_f})")
print(table1.to_string(index=False), "\n")


# =====================================================================
# TABLE 2 – raw difference-in-differences in means
# =====================================================================
means = df.groupby(["female_mgr", "post"])[list(OUTCOMES)].mean()
rows = []
for var, label in OUTCOMES.items():
    m17, m23 = means.loc[(0, 0), var], means.loc[(0, 1), var]
    f17, f23 = means.loc[(1, 0), var], means.loc[(1, 1), var]
    rows.append({"Outcome": label,
                 "Male 2017": m17, "Male 2023": m23,
                 "Female 2017": f17, "Female 2023": f23,
                 "Gap 2017 (F-M)": f17 - m17, "Gap 2023 (F-M)": f23 - m23,
                 "Raw DiD": (f23 - f17) - (m23 - m17)})
table2 = pd.DataFrame(rows).round(3)
table2.to_csv("output/table2_raw_did.csv", index=False)
print("TABLE 2 – Outcome means by wave and manager gender (unweighted)")
print(table2.to_string(index=False), "\n")


# =====================================================================
# FIGURE 1 – outcome shares by manager gender and wave
# =====================================================================
BLUE, ORANGE = "#2a78d6", "#eb6834"          # male-led, female-led
INK, MUTED, SURFACE = "#0b0b0b", "#52514e", "#fcfcfb"

fig, axes = plt.subplots(1, len(OUTCOMES), figsize=(13, 3.6), sharey=True, facecolor=SURFACE)
x = np.array([0, 1])
w = 0.36
for ax, (var, label) in zip(axes, OUTCOMES.items()):
    ax.set_facecolor(SURFACE)
    male = [means.loc[(0, 0), var], means.loc[(0, 1), var]]
    fem = [means.loc[(1, 0), var], means.loc[(1, 1), var]]
    b1 = ax.bar(x - w/2 - 0.01, male, w, color=BLUE, label="Male top manager")
    b2 = ax.bar(x + w/2 + 0.01, fem, w, color=ORANGE, label="Female top manager")
    for bars in (b1, b2):
        for b in bars:
            ax.text(b.get_x() + b.get_width()/2, b.get_height() + 0.015,
                    f"{b.get_height():.0%}", ha="center", va="bottom", fontsize=8, color=MUTED)
    ax.set_title(label, fontsize=10, color=INK)
    ax.set_xticks(x, ["2017", "2023"], color=MUTED)
    ax.set_ylim(0, 1)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
    ax.tick_params(colors=MUTED, length=0)
    ax.grid(axis="y", color="#e6e5e1", linewidth=0.6)
    ax.set_axisbelow(True)
    for s in ax.spines.values():
        s.set_visible(False)
axes[0].set_ylabel("Share of firms", color=MUTED)
fig.legend(handles=[b1, b2], loc="upper center", ncol=2, frameon=False, fontsize=9,
           bbox_to_anchor=(0.5, 1.02))
fig.suptitle("Innovation and technology adoption by top manager gender, Peru 2017 vs 2023",
             y=1.09, fontsize=11, color=INK)
fig.text(0.01, -0.04, "Source: World Bank Enterprise Surveys, Peru 2017 and 2023 (formal sector). "
         "Unweighted shares.", fontsize=8, color=MUTED)
fig.savefig("output/fig1_outcomes_by_gender_wave.png", dpi=200, bbox_inches="tight", facecolor=SURFACE)
plt.close(fig)


# =====================================================================
# TABLE 3 – LPM vs probit vs logit
# =====================================================================
def did_effect(res, data):
    """Interaction effect on the probability scale for a nonlinear model.

    In probit/logit the coefficient on female_mgr_x_post is NOT the interaction effect
    (Ai & Norton, 2003). We compute it directly as a double difference in predicted
    probabilities, averaged over the sample:
        [P(F=1,post=1) - P(F=1,post=0)] - [P(F=0,post=1) - P(F=0,post=0)]
    """
    def pred(f, p):
        d = data.copy()
        d["female_mgr"], d["post"], d["female_mgr_x_post"] = f, p, f * p
        return res.predict(d).mean()
    return (pred(1, 1) - pred(1, 0)) - (pred(0, 1) - pred(0, 0))


def female_ape(res, data):
    """Average partial effect of female_mgr in 2017 (post = 0), discrete change 0 -> 1.
    This is the probability-scale counterpart of the LPM coefficient on female_mgr,
    which (with the interaction in the model) is the pre-COVID gap."""
    d1, d0 = data.copy(), data.copy()
    for d in (d1, d0):
        d["post"], d["female_mgr_x_post"] = 0, 0
    d1["female_mgr"], d0["female_mgr"] = 1, 0
    return (res.predict(d1) - res.predict(d0)).mean()


def both_effects(res, data):
    return np.array([female_ape(res, data), did_effect(res, data)])


REPS = 199   # bootstrap replications; lower to e.g. 49 while experimenting


def cluster_bootstrap_se(fit_fn, stat_fn, data, reps=REPS, seed=1):
    """Firm-cluster bootstrap SEs: resample whole firms, refit, recompute the statistic(s)."""
    rng = np.random.default_rng(seed)
    ids = data["panelid"].unique()
    groups = {i: g for i, g in data.groupby("panelid")}
    draws = []
    for _ in range(reps):
        sample = pd.concat([groups[i] for i in rng.choice(ids, len(ids), replace=True)],
                           ignore_index=True)
        try:
            r = fit_fn(sample)
            draws.append(stat_fn(r, sample))
        except Exception:
            continue
    return np.std(np.array(draws), axis=0, ddof=1)


def stars(p):
    return "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.10 else ""


results = []
lpm_out_of_range = {}
for var, label in OUTCOMES.items():
    cols = [var, "female_mgr", "post", "female_mgr_x_post", "ln_emp", "ln_age", "mgr_exp",
            "exporter", "foreign_owned", "multi_estab", "sector", "region", "panelid"]
    d = df[cols].dropna().reset_index(drop=True)
    formula = f"{var} ~ {RHS}"
    cl = {"groups": d["panelid"]}

    # --- LPM: OLS with firm-clustered SEs (heteroskedasticity is built into the LPM)
    lpm = smf.ols(formula, d).fit(cov_type="cluster", cov_kwds=cl)
    fitted = lpm.fittedvalues
    lpm_out_of_range[label] = int(((fitted < 0) | (fitted > 1)).sum())
    for term, name in [("female_mgr", "Female manager"), ("female_mgr_x_post", "Female x Post")]:
        results.append({"Outcome": label, "Model": "LPM", "Effect": name,
                        "Estimate": lpm.params[term], "SE": lpm.bse[term], "p": lpm.pvalues[term], "N": int(lpm.nobs)})

    # --- Probit and logit, effects on the probability scale
    for model_name, fn in [("Probit", smf.probit), ("Logit", smf.logit)]:
        fit = lambda data, fn=fn: fn(formula, data).fit(disp=0, cov_type="cluster",
                                                        cov_kwds={"groups": data["panelid"]})
        res = fit(d)
        ests = both_effects(res, d)
        ses = cluster_bootstrap_se(fit, both_effects, d)
        for name, est, se in zip(["Female manager", "Female x Post"], ests, ses):
            p = 2 * (1 - stats.norm.cdf(abs(est / se)))
            results.append({"Outcome": label, "Model": model_name, "Effect": name,
                            "Estimate": est, "SE": se, "p": p, "N": int(res.nobs)})

table3 = pd.DataFrame(results)
table3["Cell"] = table3.apply(lambda r: f"{r.Estimate:.3f}{stars(r.p)} ({r.SE:.3f})", axis=1)
table3.round(4).to_csv("output/table3_lpm_probit_logit.csv", index=False)

wide = table3.pivot_table(index=["Outcome", "Effect"], columns="Model", values="Cell", aggfunc="first")
wide = wide[["LPM", "Probit", "Logit"]]
print("TABLE 3 – Effect on probability of each outcome (average partial effects)")
print("Firm-clustered SEs in parentheses (probit/logit: cluster bootstrap, 199 reps). *** p<.01 ** p<.05 * p<.10")
print("Controls: log employees, log firm age, manager experience, exporter, foreign owned,")
print("multi-establishment, sector FE, region FE, post-2023 dummy.\n")
print(wide.to_string(), "\n")
print("LPM fitted values outside [0,1]:", lpm_out_of_range)
