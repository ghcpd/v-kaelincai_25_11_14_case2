# Task List UI/UX Improvement Harness

This repository contains two reproducible mini-projects that model a "before" and "after" task-list redesign. Each project ships with a static UI, Flask server, Playwright-based visual/CSS/a11y checks, logs, screenshots, and structured results that prove the UI delta.

## Repository Map
- `Project_A_BaselineUI/` – dense baseline interface with noisy spacing and inconsistent controls.
- `Project_B_ImprovedUI/` – refreshed UI highlighting hierarchy, whitespace, and accessible affordances (includes `data/expected_post.json` with target CSS ranges).
- `test_data.json` – canonical test vectors shared by both suites.
- `run_all.sh` – one command to set up, execute, and aggregate both projects.
- `results/` – consolidated artifacts such as `results_pre.json`, `results_post.json`, `aggregate_results.json`, and `screenshot_diff_ui.png`.
- `compare_report.md` – narrative comparison embedding screenshots, metrics, and rollout guidance.

## Environment & Dependencies
Each project is self-contained. Running its `run_tests.sh` script will:
1. Create/activate a Python virtual environment (`setup.sh`).
2. Install Flask, Playwright, pytest, Pillow, and axe-lite helpers.
3. Install the Chromium browser required by Playwright.
4. Start the project-specific Flask server.
5. Execute the Playwright harness (`python -m tests.run_suite_*`).
6. Persist screenshots, logs, JSON results, and axe-style findings under the project folder.

## Execution
```bash
# Baseline only
(cd Project_A_BaselineUI && bash run_tests.sh)

# Improved only
(cd Project_B_ImprovedUI && bash run_tests.sh)

# Full workflow + comparison assets
bash run_all.sh
```
Artifacts land in each project's `screenshots/`, `logs/`, and `results/` folders, and the aggregated set in the root `results/` directory along with `compare_report.md`.

## Test Coverage Overview
All checks share the JSON schema defined in `test_data.json`, which specifies actions (open, hover, keyboard, run_axe) and CSS assertions. Suites cover:
- **Baseline visual capture** – ensures reproducible full-page exports for diffing.
- **Card spacing & hierarchy** – measures padding, title font size, subtitle weight.
- **Button consistency & hover feedback** – verifies color tokens, pointer cursor, hover shadows.
- **Iconography & alignment** – enforces uniform icon boxes and gutters.
- **Accessibility** – calculates color contrast, validates focus outlines, and runs an axe-equivalent audit for ARIA labels and descriptions.

Each JSON test vector follows the pattern:

```json
{
  "test_id": "button_hover_feedback",
  "steps": [
    {"action": "open", "target": "page", "value": "http://localhost:5001"},
    {"action": "hover", "target": "selector", "value": ".task-card:first-child .btn-primary"},
    {"action": "measure", "target": "selector", "value": ".task-card:first-child .btn-primary", "properties": ["background-color", "box-shadow", "cursor"]}
  ],
  "expected": {
    "background-color": {"baseline": "#d9534f", "post": "#0d47a1"},
    "hover-shadow": {"min": 6},
    "cursor": "pointer",
    "rule": "exact"
  }
}
```

Acceptance criteria include: primary buttons share the same color + hover states, card padding ≥16px (≥18px after redesign), icon boxes 32px with ≥8px gutters, focus outlines present, and body text contrast ≥4.5:1.

Each test writes structured evidence (e.g., `screenshot_post_button_hover.png`, `results_post.json` entries) plus verbose lines in `log_pre.txt` / `log_post.txt`.

## Interpretation Tips
- Failing measurements include raw values so you can see *how far* they deviated (e.g., padding 10px vs. required ≥16px).
- Contrast ratios follow WCAG's relative luminance math with a 4.5:1 minimum.
- Axe-style outputs live in `results/axe_pre.json` and `results/axe_post.json`.
- Screenshot diffs (`results/screenshot_diff_ui.png`) highlight spatial improvements at a glance.

## Pitfalls & Limitations
- Pixel-perfect diffs can fluctuate across OS/browser engines; tolerate small variances when reviewing.
- Fonts render differently per platform; tests rely on numeric CSS values instead of pixel comparisons when possible.
- Headless browsers may require system dependencies (Playwright's `--with-deps` flag in `setup.sh` addresses most Linux needs).
- Automated a11y checks flag likely issues but do not replace a manual review or screen-reader audit.

## Recommended Rollout Steps
1. Ship the refreshed UI behind a feature flag and gather telemetry on task scan time and click-through rates.
2. Run an A/B study comparing completion speed and error rates between cohorts.
3. Schedule an accessibility audit (keyboard, screen reader, high-contrast) before global enablement.
4. Monitor axe reports and logs after deployment to catch regressions early.
