# sobtidentalcare.com

Main website of Dr Sobti's Dental Care, J 12/26, First Floor, Rajouri Garden, New Delhi 110027.

- `python3 build.py` builds the site into `_site/` (no dependencies).
- Clinic name, address, phones and hours are in the `CLINIC` block at the top of `build.py`. Keep them identical to the Google Business Profile.
- Implant pages live on dentalimplantsdelhi.com and other treatment pages on drparulssobti.com; this site is the clinic hub and links to them.
- Every push to `main` deploys to GitHub Pages (`.github/workflows/deploy.yml`) at https://www.sobtidentalcare.com.
