# streamlit_app.py
import json
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="A/B Test Decision Dashboard", layout="wide")
st.title("A/B Test Decision Dashboard")

# Where the notebook saved results & images
res_path = Path("report/results.json")
img_ci   = Path("report/revenue_ci.png")
img_dist = Path("report/revenue_dist.png")

# Guard: ask user to generate results first if missing
if not res_path.exists():
    st.error("File not found: report/results.json. Run your notebook cells that save results.json and images to the 'report' folder first.")
    st.stop()

data = json.loads(res_path.read_text())

primary   = data.get("primary", {})
secondary = data.get("secondary", {})

# ---- Primary KPI (retention_7) ----
st.subheader("Primary KPI: retention_7")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("pA", f'{primary.get("pA", 0):.3f}')
with col2:
    st.metric("pB", f'{primary.get("pB", 0):.3f}')
with col3:
    st.metric("p-value", f'{primary.get("pvalue", 1):.4f}')

# ---- Secondary KPI (revenue) ----
st.subheader("Secondary KPI: revenue")
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("mean(A)", f'{secondary.get("meanA", 0):.3f}')
    st.metric("Welch CI low",  f'{secondary.get("ci_low_welch", 0):.3f}')
with c2:
    st.metric("mean(B)", f'{secondary.get("meanB", 0):.3f}')
    st.metric("Welch CI high", f'{secondary.get("ci_high_welch", 0):.3f}')
with c3:
    st.metric("Δ = mean(B) - mean(A)", f'{secondary.get("delta", 0):.3f}')
    st.metric("Permutation p", f'{secondary.get("p_perm", 1):.4f}')

st.write(
    f"Bootstrap 95% CI: [{secondary.get('boot_low', 0):.3f}, {secondary.get('boot_high', 0):.3f}]"
)

st.divider()
st.subheader("Visuals")

cols = st.columns(2)
with cols[0]:
    if img_ci.exists():
        st.image(str(img_ci), caption="Group means with bootstrap 95% CI", use_container_width=True)
    else:
        st.info("Missing image: report/revenue_ci.png")

with cols[1]:
    if img_dist.exists():
        st.image(str(img_dist), caption="Revenue distribution by variant", use_container_width=True)
    else:
        st.info("Missing image: report/revenue_dist.png")
