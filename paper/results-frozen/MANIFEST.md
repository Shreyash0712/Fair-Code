# Frozen results provenance

This snapshot is what a paper should cite. `results/` at the repo root keeps changing as
contributors add audits or rerun the harness; this folder does not - regenerate it with
`scripts/freeze_paper_results.py` only when you are ready to move the citation forward.

## Provenance

- **Git commit:** `00dbb38b2ff467ff2985848404fe3d10a66cf001` (WORKING TREE HAD UNCOMMITTED CHANGES AT FREEZE TIME)
- **Git branch:** `main`
- **Python:** 3.13.2
- **scikit-learn:** 1.8.0
- **fairlearn:** 0.14.0
- **pandas:** 3.0.2
- **numpy:** 2.4.4
- **Full environment:** `requirements-lock.txt` in this folder

## Audits included (7 domains)

The exact, reproducible set of manifests this snapshot covers - not "whatever was in the
repo that week":

- `AI Fair Recruitment/audit.yaml`
- `Benefits Denial/audit.yaml`
- `COMPAS/audit.yaml`
- `German Credit Lending/audit.yaml`
- `Healthcare Readmission/audit.yaml`
- `Insurance Denial/audit.yaml`
- `Tenant Screening/audit.yaml`

## Reproducing this snapshot

```bash
git checkout 00dbb38b2ff467ff2985848404fe3d10a66cf001
pip install -r requirements-lock.txt
pip install -e ".[benchmark]"
faircode benchmark --out results/
python3 scripts/freeze_paper_results.py
```

## Tag

This snapshot corresponds to the intended tag `v1.0-paper` - not yet created. Run manually:

```bash
git tag -a v1.0-paper -m "Results frozen for paper citation"
git push origin v1.0-paper
```
