# Manager Gender and Technology Adoption in Peruvian Firms, 2010–2023

Code for my final project in KAN-CEAPV2505U Econometric Analysis of Firm Data (Copenhagen Business School).

`peru_gender_technology_panel.Rmd` contains the full analysis: it links three waves of the World Bank Enterprise Surveys for Peru (2010, 2017, 2023) into an unbalanced firm panel, estimates linear probability models by pooled OLS, random effects and fixed effects, runs a probit check, the Mundlak test, selection tests for unbalanced panels and robustness checks (common sample, separate 2017 gap), and writes every table and figure used in the paper. `peru_gender_technology_panel.html` is the rendered output.

## Data
The survey files are not included because the World Bank's terms do not allow redistribution. Register at https://www.enterprisesurveys.org, download

- Peru 2006–2017 panel (`Peru_2006_2010_2017.dta`)
- Peru 2017–2023 panel (`Peru_2017_2023.dta`)

and place them in `data/`.

## Running
Requires R with `haven`, `dplyr`, `tidyr`, `plm`, `sandwich`, `lmtest`, `ggplot2`, `scales`, `knitr` and `rmarkdown` installed (`tidyr` and `scales` are called with `::`, so they are not attached but must be installed).

```r
rmarkdown::render("peru_gender_technology_panel.Rmd")
```

The notebook writes `tables/tab1_desc.tex`–`tab4_robust.tex` and `figures/fig1_outcomes.pdf`. The LaTeX paper reads them from `paper/tables/` and `paper/figures/`, so copy both folders there after rendering:

```bash
cp tables/* ../paper/tables/ && cp figures/* ../paper/figures/
```
