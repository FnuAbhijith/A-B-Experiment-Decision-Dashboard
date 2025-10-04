
# A/B Experiment Decision Dashboard 

Analyze a real A/B test end-to-end and make a ship/no-ship call with **classical statistics** (two-proportion test, Welch’s t-test), **bootstrap CIs**, **permutation tests**, an **executive memo**, and a **Streamlit** dashboard.

---

## Problem Statement
Mobile games often run A/B tests (e.g., moving a level gate) and need a **defensible decision**: did the change improve retention and engagement or not? This project turns raw experiment data into **decision-ready** outputs for stakeholders.

**Goal:** Evaluate the Cookie Cats experiment with sound inference and deliver a dashboard + memo that a PM can read in minutes.

---

## Dataset
- **Source:** Cookie Cats A/B dataset (public)
- **Key columns:**  
  `variant` (`A`/`B`), `retention_7` (0/1), `sum_gamerounds` (numeric)
- **Mapping used:** original labels like `gate_30` → `A`, `gate_40` → `B`
https://www.kaggle.com/datasets/mursideyarkin/mobile-games-ab-testing-cookie-cats?utm_source=chatgpt.com

---

## Approach
1. **Data prep**
   - Map variants to `A`/`B`, cast KPI types, basic sanity checks (missing values, ranges).
2. **Primary KPI (binary):** `retention_7`
   - Two-sample proportion test → report **Δ (B–A)**, **95% CI**, **p-value**.
3. **Secondary KPI (continuous):** `sum_gamerounds`
   - **Welch’s t-test** for Δ (B–A) with unequal variances.
   - **Bootstrap 95% CI** (unpaired; resample A & B separately).
   - **Permutation test** (2-sided) for mean difference robustness.
4. **Visuals**
   - Distribution by variant.
   - Means with **bootstrap 95% CI** error bars.
5. **Artifacts**
   - `report/results.json` (machine-readable summary)
   - `report/memo.html` (executive memo with figures)
6. **App**
   - `streamlit_app.py` — upload CSV → view KPIs, CIs, p-values, charts → download memo/JSON.

---

## Results (fill with your run)
These values come from `report/results.json` after running the notebook.

**Primary – `retention_7`**
- A: `pA = 0.____` &nbsp;&nbsp; B: `pB = 0.____`  
- Δ (B–A): `____` &nbsp; 95% CI `[ ____, ____ ]` &nbsp; p-value `____`

**Secondary – `sum_gamerounds`**
- A: `meanA = ____` &nbsp;&nbsp; B: `meanB = ____`  
- Δ (B–A): `____`  
  - Welch 95% CI `[ ____, ____ ]`  
  - Bootstrap 95% CI `[ ____, ____ ]`  
  - Permutation p-value `____`

> Example from one run on Cookie Cats: Welch CI crossed 0; bootstrap CI also crossed 0; permutation p ≈ 0.38 → **not significant** on engagement; base the decision on the primary KPI.

---

## Business Insights
- **Decide on the primary KPI** (retention). Secondary engagement is supportive, not decisive.
- Report **effect sizes with uncertainty**, not just p-values.
- Use **bootstrap + permutation** to validate assumptions for skewed metrics.

---

## Tech Stack
- **Python:** pandas, numpy, scipy/statsmodels, matplotlib/plotly  
- **Inference:** two-proportion test, Welch’s t-test, unpaired bootstrap, permutation test  
- **App:** Streamlit (dashboard)  
- **Artifacts:** HTML memo, JSON results, PNG figures

---

---

## How to Run

### 1) Environment
**Windows (PowerShell)**
```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

Launch dashboard
streamlit run streamlit_app.py

