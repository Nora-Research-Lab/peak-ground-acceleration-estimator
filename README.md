![NORA logo](https://i.ibb.co/0VJCC9Gf/IMG-20260114-WA0008.jpg)
 
# Peak Ground Acceleration Estimator
 
*For seismologists and earthquake engineers: enter earthquake magnitude, distance, and site soil class to instantly estimate peak ground acceleration (PGA) using a standard attenuation relationship.*
 
[![GitHub](https://img.shields.io/badge/GitHub-Nora--Research--Lab-181717?logo=github)](https://github.com/Nora-Research-Lab) [![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-NoraResearchLab-yellow)](https://huggingface.co/NoraResearchLab) [![LinkedIn](https://img.shields.io/badge/LinkedIn-NORA%20Research%20Lab-0A66C2?logo=linkedin)](https://www.linkedin.com/company/nora-research-lab) [![X](https://img.shields.io/badge/X-@noraresearchlab-000000?logo=x)](https://x.com/noraresearchlab) [![NORA Research Lab](https://img.shields.io/badge/Website-noraresearchlab.site-2ea44f)](https://noraresearchlab.site) [![NORA Earth Intelligence](https://img.shields.io/badge/Platform-noraearth.xyz-2ea44f)](https://noraearth.xyz)
 

## Overview
 
**Industry:** Earthquake / Hazard Analysis
 
The tool provides a PGA estimate from a user-specified earthquake scenario using the Joyner & Boore (1981) attenuation relation with simplified site and faulting-style adjustments.

Inputs:
- Magnitude (M, float, range 3.0–9.0, step 0.1): moment magnitude.
- Distance (R, float, range 0.1–500 km, step 0.1): closest distance to fault rupture (km).
- Site soil class (dropdown): 'Rock (Vs30 > 760 m/s)', 'Stiff soil (360–760 m/s)', 'Soft soil (<360 m/s)'. Corresponding site factors: 1.0, 1.2, 1.5.
- Faulting style (dropdown): 'Strike-slip' (default), 'Reverse', 'Normal'. Style factors (applied to final PGA): strike-slip = 1.0, reverse = 1.1, normal = 0.9.

Core calculation (step by step):
1. Compute log10 PGA (cm/s²) using Joyner & Boore (1981):
   log10(PGA_cm_s2) = 0.249 + 0.298 * (M - 6) - 0.00188 * R - 0.00046 * M * R
2. PGA_cm_s2 = 10^(log10(PGA_cm_s2)).
3. Apply site factor: PGA_cm_s2_site = PGA_cm_s2 * site_factor.
4. Apply faulting style factor: PGA_cm_s2_final = PGA_cm_s2_site * fault_factor.
5. Convert to g: PGA_g = PGA_cm_s2_final / 980.
6. Classification thresholds (PGA_g): <0.1 → 'Weak'; 0.1–0.299 → 'Moderate'; 0.3–0.599 → 'Strong'; 0.6–0.999 → 'Very Strong'; ≥1.0 → 'Extreme'.

Gradio UI layout:
- Left column: two number inputs (M, R) with sliders; two dropdowns (site class, faulting style); a 'Compute PGA' button.
- Right column: output display with PGA in g (3 decimals) and in cm/s² (integer) in bold; classification text with color (green/amber/red); a matplotlib horizontal bar chart (width = PGA_g, with vertical dashed lines at 0.1, 0.3, 0.6, 1.0).

No AI/ML component; all logic is formula-based.
 
## Run it
 
```bash
docker build -t peak-ground-acceleration-estimator .
docker run -p 7860:7860 peak-ground-acceleration-estimator
```
 
Then open http://localhost:7860 in your browser.
 
## About
 
This tool was generated and published automatically by the **NORA Earth Intelligence**
tool factory, an autonomous pipeline maintained by **NORA Research Lab** that turns
one idea per run into a small, working geoscience tool — end to end, with an
LLM writing and Docker-testing the code, and another model generating the
banner above.
 
- Platform: [https://noraearth.xyz](https://noraearth.xyz)
- Parent lab: [https://noraresearchlab.site](https://noraresearchlab.site)
 
Built 2026-09-23.
 
---
 
### Maintainer
 
**NORA Research Lab**
[![GitHub](https://img.shields.io/badge/GitHub-Nora--Research--Lab-181717?logo=github)](https://github.com/Nora-Research-Lab) [![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-NoraResearchLab-yellow)](https://huggingface.co/NoraResearchLab) [![LinkedIn](https://img.shields.io/badge/LinkedIn-NORA%20Research%20Lab-0A66C2?logo=linkedin)](https://www.linkedin.com/company/nora-research-lab) [![X](https://img.shields.io/badge/X-@noraresearchlab-000000?logo=x)](https://x.com/noraresearchlab) [![NORA Research Lab](https://img.shields.io/badge/Website-noraresearchlab.site-2ea44f)](https://noraresearchlab.site) [![NORA Earth Intelligence](https://img.shields.io/badge/Platform-noraearth.xyz-2ea44f)](https://noraearth.xyz)
