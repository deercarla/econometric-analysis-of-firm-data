
# Manager Gender, Innovation and Technology Adoption in Peruvian Firms

**Econometric Analysis of Firm Data · Copenhagen Business School · October 2026**

This repository accompanies the research project **“Manager Gender, Innovation and Technology Adoption in Peruvian Formal Firms Before and After COVID-19.”** It investigates differences in innovation and technology adoption between firms with female and male top managers, and whether these differences changed between 2017 and 2023.

The analysis uses World Bank Enterprise Survey data for Peru and combines cross-sectional regressions, a two-wave firm panel, and an Oaxaca–Blinder decomposition. The aim is to distinguish descriptive gender gaps from associations with observable firm characteristics—not to claim that manager gender or the COVID-19 pandemic has been causally identified as the source of these differences.

## Research questions

1. Are firms with a female top manager less likely to innovate or adopt technology, conditional on observable firm characteristics?
2. Did the female–male gap change between 2017 and 2023, particularly for website adoption?
3. How much of the observed gap can be statistically accounted for by differences in firm characteristics?

## Data

The project uses the **World Bank Enterprise Surveys for Peru**:

- **2017 and 2023 surveys:** 1,990 firm-year observations (1,003 in 2017; 987 in 2023), representing 1,632 distinct firms.
- **2017–2023 matched panel:** 358 firms interviewed in both waves.
- **2010–2017 comparison panel:** 374 firms interviewed in both years, used for a pre-pandemic placebo analysis. An additional placebo check uses 143 firms present across the two panel periods.

The surveys cover formal, non-agricultural private firms with at least five employees. Outcomes are indicators for:

- New product or service introduction
- Process innovation
- Research and development (R&D) expenditure
- Ownership of a website
- Internationally recognized quality certification

The main explanatory variable is whether the firm has a **female top manager**. Controls include firm size, age, manager experience, exporter status, foreign ownership, membership in a larger firm, sector, region, and survey wave, as applicable to each model.

**Official data sources:**

- [Peru Enterprise Survey 2006–2017 panel](https://doi.org/10.48529/em87-8m38)
- [World Bank Enterprise Surveys portal](https://www.enterprisesurveys.org/) — Peru 2023 survey and harmonized panel materials

Data availability and reuse are subject to the World Bank's applicable access terms. The analysis requires the relevant survey files; their presence in this repository has not been verified.

## Methods

The empirical analysis proceeds through complementary specifications:

| Method | Purpose |
| --- | --- |
| Linear probability model (OLS) | Estimate conditional gender gaps and changes across survey waves |
| Probit and logit | Check sensitivity to nonlinear binary-outcome models, using average partial effects |
| Firm fixed effects and first differences | Account for time-invariant unobserved firm characteristics in the matched panel |
| Baseline-gender difference-in-differences | Compare 2017–2023 changes across firms grouped by 2017 manager gender |
| Pre-pandemic placebo and sensitivity analyses | Examine the plausibility of differential-trend interpretations |
| Oaxaca–Blinder decomposition | Attribute portions of raw gaps statistically to observed firm characteristics and a residual component |
| Sampling-weighted models and subgroup analyses | Explore population-oriented estimates and heterogeneity by firm size |
| Proxy and instrumental-variable exercises | Investigate identification limitations; **not** used to support causal conclusions |

Inference generally uses firm-clustered standard errors; some nonlinear effects and decomposition estimates use firm-cluster bootstrapping. The study also reports multiple-testing adjustments, specification diagnostics, and checks related to firm survival and survey weighting.

## Main findings

- **Raw differences:** Female-led firms are approximately **5–11 percentage points** less likely to report several outcomes, including new products, R&D, websites, and quality certification, in the unweighted sample.
- **Observable characteristics:** Differences in measured firm characteristics statistically account for approximately **62–71%** of the raw gaps in R&D expenditure, website ownership, and certification. **Firm size** contributes substantially. This is a decomposition, not a causal explanation.
- **Certification:** Quality certification retains a statistically significant unexplained component of approximately **4.1 percentage points**. A separate heterogeneity analysis finds the conditional certification gap concentrated among medium and large firms.
- **Website adoption:** In the matched panel, website adoption increased **12.7 percentage points more** among firms with a female top manager in 2017. However, this result is sensitive to baseline-specific trends, does not survive Holm multiple-testing correction, and cannot rule out pre-existing differential trends. It is **suggestive, not causal**, evidence.
- **Population weighting:** Weighted estimates suggest larger conditional gaps for new-product innovation and certification than the principal unweighted estimates; inference is less precise and the survey design warrants care.

The overall conclusion is that observable composition explains a substantial portion of several sample gender gaps, but neither the absence of statistically significant conditional gaps nor the decomposition rules out gender-related constraints.

## Code and reproducibility

The paper identifies the following analysis files:

```text
01_clean_peru.py
peru_gender_innovation_analysis.ipynb
```

- **`01_clean_peru.py`** — cleans and prepares the Peru survey data.
- **`peru_gender_innovation_analysis.ipynb`** — conducts the econometric analysis and generates the tables reported in the paper.

The analysis is written in **Python 3**, using **`statsmodels`** and **`linearmodels`**. Other required packages, exact versions, input paths, and execution settings should be determined from the actual code; they have not been verified from the paper alone.

### Reproducing the analysis

1. Obtain the relevant Peru survey and panel files from the World Bank Enterprise Surveys portal.
2. Place the input files in the locations expected by `01_clean_peru.py` (check the script for those paths).
3. Set up a Python 3 environment with the dependencies imported by the script and notebook.
4. Run `01_clean_peru.py` to prepare the analysis data.
5. Run `peru_gender_innovation_analysis.ipynb` in order to reproduce the analyses and reported tables.

> **Reproducibility note:** These steps reflect the workflow described in the paper. File paths, environment setup, data access, and end-to-end execution must be checked against the repository before describing the project as fully reproducible.

## Interpretation and limitations

This is an **observational study**. Manager gender is not randomly assigned, and the instrumental-variable candidates do not provide a credible basis for causal identification. The panel comparison removes time-invariant firm heterogeneity but does not establish the counterfactual trends needed to attribute differential changes to the pandemic. The matched panel is also restricted to surviving, re-interviewed firms, while the binary outcomes measure adoption or occurrence rather than innovation intensity or quality.

## Selected references

- Ai, C., & Norton, E. C. (2003). Interaction terms in logit and probit models. *Economics Letters, 80*(1), 123–129.
- Fortin, N., Lemieux, T., & Firpo, S. (2011). Decomposition methods in economics. In *Handbook of Labor Economics* (Vol. 4A, pp. 1–102).
- Hyland, M., Karalashvili, N., Muzi, S., & Viganola, D. (2021). *Female-owned firms during the COVID-19 crisis*. World Bank Global Indicators Brief No. 2.
- Jann, B. (2008). The Blinder–Oaxaca decomposition for linear regression models. *The Stata Journal, 8*(4), 453–479.
- Mundlak, Y. (1978). On the pooling of time series and cross section data. *Econometrica, 46*(1), 69–85.
- Wooldridge, J. M. (2025). *Introductory Econometrics: A Modern Approach* (8th ed.). Cengage.

See the accompanying paper for the complete bibliography and detailed estimates.

## Author

Carla de Erausquin  
Copenhagen Business School  
Course: Econometric Analysis of Firm Data (KAN-CEAPV2505U)
