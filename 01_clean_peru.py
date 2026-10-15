"""
01_clean_peru.py
Econometric Analysis of Firm Data (KAN-CEAPV2505U) – final project
Gender, innovation and technology adoption in Peruvian formal firms, 2017 vs 2023

Input : Peru_2017_2023.dta  (World Bank Enterprise Surveys panel file, formal sector)
Output: peru_pooled.csv     all firms, both waves (pooled cross-sections, N≈1,990)
        peru_panel.csv      only firms interviewed in BOTH waves (358 firms x 2)

Coding conventions in the raw data
  - Yes/No questions: 1 = Yes, 2 = No
  - Negative values are non-responses: -9 = don't know, -7 = refused, -6 = not applicable
"""

import numpy as np
import pandas as pd

RAW = "Peru_2017_2023.dta"          # adjust the path if needed

raw = pd.read_stata(RAW, convert_categoricals=False)


# ---------------------------------------------------------------- helpers
def yesno(s):
    """1 = Yes -> 1, 2 = No -> 0, anything else (negative codes) -> NaN."""
    return s.map({1: 1, 2: 0}).astype("float")


def clean_num(s):
    """Numeric variable with negative non-response codes -> NaN."""
    s = s.astype("float")
    return s.where(s >= 0)


df = pd.DataFrame(index=raw.index)

# ---------------------------------------------------------------- identifiers & design
df["panelid"] = raw["panelid"].astype(int)          # same ID for a firm across waves
df["year"] = raw["year"].astype(int)
df["post"] = (df["year"] == 2023).astype(int)       # post-COVID wave
df["in_panel"] = (raw["panel"] == 3).astype(int)    # interviewed in both 2017 and 2023
df["weight"] = raw["wmedian"]                       # sampling weight (cross-sectional, NOT a panel weight)
df["strata"] = raw["strata"]

# ---------------------------------------------------------------- gender variables
df["female_mgr"] = yesno(raw["b7a"])                # top manager is female
df["female_own_any"] = yesno(raw["b4"])             # any female owner
# % owned by women: only asked if b4 == Yes, so set to 0 when there is no female owner
own = clean_num(raw["b4a"])
df["female_own_share"] = np.where(df["female_own_any"] == 0, 0, own)
df["female_own_major"] = (df["female_own_share"] > 50).astype(float).where(df["female_own_share"].notna())

# Female share of the permanent full-time workforce.
# Services firms answer l5 (total female); manufacturing firms answer l5a + l5b (production + non-production)
l1 = clean_num(raw["l1"])
fem_workers = clean_num(raw["l5"]).fillna(clean_num(raw["l5a"]) + clean_num(raw["l5b"]))
df["female_worker_share"] = (fem_workers / l1).where(lambda x: x <= 1)

# ---------------------------------------------------------------- outcomes: innovation & technology
df["new_product"] = yesno(raw["h1"])                # new product/service, last 3 years
df["process_innov"] = yesno(raw["h5"])              # new/improved process, last 3 years
df["rd"] = yesno(raw["h8"])                         # spent on R&D last fiscal year
df["website"] = yesno(raw["c22b"])                  # own website
df["quality_cert"] = yesno(raw["b8"])               # internationally recognised quality certificate
df["foreign_tech"] = yesno(raw["e6"])               # foreign-licensed technology (manufacturing only)
df["training"] = yesno(raw["l10"])                  # formal training programme

# ---------------------------------------------------------------- controls
df["employees"] = l1
df["ln_emp"] = np.log(l1)
df["size"] = raw["a6a"].map({1: "small", 2: "medium", 3: "large"})   # sampling size (5-19, 20-99, 100+)

start = clean_num(raw["b5"])
df["firm_age"] = (df["year"] - start).where(lambda x: x >= 0)
df["ln_age"] = np.log1p(df["firm_age"])
df["mgr_exp"] = clean_num(raw["b7"])                # top manager's years of sector experience (proxy for ability)

df["exporter"] = (clean_num(raw["d3c"]) >= 10).astype(float)        # direct exports >= 10% of sales
df["foreign_owned"] = (clean_num(raw["b2b"]) >= 10).astype(float).where(clean_num(raw["b2b"]).notna())
df["multi_estab"] = yesno(raw["a7"])                # part of a larger firm
df["credit"] = yesno(raw["k8"])                     # has a credit line / loan

# Sector: harmonised across waves in the panel file (a4a, 7 categories)
sector_map = {1: "food", 2: "textiles", 3: "garments", 4: "other_manuf",
              5: "retail", 6: "hotels", 7: "other_services"}
df["sector"] = raw["a4a"].map(sector_map)
df["manufacturing"] = raw["a4a"].isin([1, 2, 3, 4]).astype(int)

region_map = {1: "Lima", 2: "Arequipa", 3: "Chiclayo", 4: "Trujillo", 5: "Piura"}
df["region"] = raw["a2"].map(region_map)

# Sales growth over the previous 3 years (d2 = sales last FY, n3 = sales 3 years ago).
# In the 2023 wave this window covers the COVID years, so it can serve as a firm-level shock measure.
d2, n3 = clean_num(raw["d2"]), clean_num(raw["n3"])
df["sales_growth_3y"] = np.log(d2) - np.log(n3)

# ---------------------------------------------------------------- interaction for H2
df["female_mgr_x_post"] = df["female_mgr"] * df["post"]

# ---------------------------------------------------------------- save
df.to_csv("peru_pooled.csv", index=False)
panel = df[df["in_panel"] == 1].sort_values(["panelid", "year"])
panel.to_csv("peru_panel.csv", index=False)

# ---------------------------------------------------------------- quick checks
print(f"Pooled: {len(df)} obs  |  Panel: {panel['panelid'].nunique()} firms x 2 waves")
print("\nMissing values in key variables:")
print(df[["female_mgr", "new_product", "process_innov", "rd", "website",
          "ln_emp", "firm_age", "mgr_exp", "female_worker_share"]].isna().sum())

outcomes = ["new_product", "process_innov", "rd", "website", "quality_cert", "training"]
print("\nShare of firms (unweighted), by wave and manager gender:")
print(df.groupby(["year", "female_mgr"])[outcomes].mean().round(3))

# Firms whose top manager's gender changes between waves identify the
# female_mgr coefficient in a fixed-effects regression
w = panel.pivot(index="panelid", columns="year", values="female_mgr")
print("\nPanel firms switching manager gender:", int((w[2017] != w[2023]).sum()))
