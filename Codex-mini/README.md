# Task List Visual Redesign Experiment

This repository contains two parallel projects for the **UI/UX improvement** experiment: the "before" baseline (`Project_A_BaselineUI`) and the "after" redesigned layout (`Project_B_ImprovedUI`). Every requirement¡ªfrom static assets to automated visual assertions, accessibility checks, logs, and a unified comparison report¡ªis satisfied locally without paid services.

## Test Scenario & Description
- **Scenario:** Load the dense task-list UI (baseline) and the refreshed redesign (improved) to verify visual clarity, spacing, hierarchy, control affordance (buttons/hover states), consistent iconography, and accessibility (contrast/focus/ARIA).
- **Test Input Format (JSON):** Tests are defined in `test_data.json` (and duplicated under each project¡¯s `data/` folder) as arrays of objects containing `test_id`, `description`, `steps`, `selector`, `action`, `expected`, `screenshot`, and `pass_rule`. The automation reads these definitions to plan navigation, CSS queries, hover/focus actions, and screenshot expectations.
- **Expected Output Format:** Each test writes entries into `results_pre.json` / `results_post.json` containing `test_id`, `status`, `screenshots`, `measurements` (CSS values like padding/font-size/color), and full-context `details`. Accessibility checks append violation counts and focus targets.
- **Acceptance Criteria Examples:** Primary buttons share `btn.primary` color/hovers, card padding ¡Ý 16px, title font size ¡Ý 20px, subtitle weight lighter, icons uniform, focus outline present, contrast ratio ¡Ý 4.5:1 for body text (flagged via axe and recorded in the results JSON).

## Setup
Each project provides a `setup.sh` helper that creates a venv and installs the dependencies (`flask`, `playwright`, `pytest`, `pillow` plus Playwright browsers). Run it from a Unix-like shell (Git Bash, WSL, or similar) with:

```bash
./Project_A_BaselineUI/setup.sh
./Project_B_ImprovedUI/setup.sh
```

On Windows PowerShell you can replicate the logic manually:
1. `python -m venv Project_X_YYY/.venv`
2. `Project_X_YYY/.venv/Scripts/pip install -r Project_X_YYY/requirements.txt`
3. `Project_X_YYY/.venv/Scripts/python -m playwright install`

## Running Tests
- Baseline (Pre UI):
  ```bash
  ./Project_A_BaselineUI/run_tests.sh
  ```
- Improved (Post UI):
  ```bash
  ./Project_B_ImprovedUI/run_tests.sh
  ```
Each script starts the Flask server, runs the Playwright-based visual/CSS/a11y suites, stores logs under `logs/`, snapshots under `screenshots/`, and results under `results/`.

- Combined workflow:
  ```bash
  ./run_all.sh
  ```
  This master script executes both suites, copies aggregated artifacts into `results/`, generates the visual diff via `scripts/generate_diff.py`, rebuilds `results/compare_report.md`, and syncs the root `compare_report.md`.

## Artifacts
- `Project_*_UI/screenshots/`: baseline/improved UI snapshots (`screenshot_*_ui.png`, per-test captures). Respective `logs/` and `results/` hold console logs, structured JSON results (`results_pre.json`, `results_post.json`).
- `results/`: aggregated `results_pre.json`, `results_post.json`, the visual diff (`diff_ui.png`), and before/after UI copies plus the latest `compare_report.md`.
- `compare_report.md`: Executive summary, embedded thumbnails, CSS deltas, a11y summary, pitfalls, and rollout recommendations.

## Testing Approach
1. **Visual capture:** `test_*_visual.py` opens the page, waits for network idle, takes full/fragment screenshots (`screenshot_pre_ui.png`, `screenshot_post_ui.png`, per-test snapshots), and records page height.
2. **CSS assertions:** `test_*_css_assertions.py` measures card padding, border radius, button colors, box shadows, hover states, and cursor affordances, saving results and per-test screenshots.
3. **Accessibility checks:** `test_*_a11y.py` injects `axe-core` (`tests/axe.min.js`), runs `axe.run()`, records violation counts, color-contrast stats, and keyboard focus targets.

Each test writes to the project-specific `results/results_(pre|post).json` (JSON objects with CSS & a11y metrics) and logs JS console output to `logs/log_(pre|post).txt`. Screenshots are referenced using consistent names so automated diffs and reports can locate them.

## Data & Expectations
- Canonical test vectors live in `test_data.json` (mirrored inside `Project_*/data`). Five test cases cover baseline visual capture, spacing/hierarchy, button consistency, icon alignment, and accessibility. Each entry includes `steps` (page load, hover, focus), `selector`, `action`, `expected` DOM/CSS assertions, screenshot name, and pass/fail rule (`exact` or `threshold`).
- The improved project also ships `data/expected_post.json` with target CSS/property ranges (padding ¡Ý 20px, primary button color `#0d47a1`, contrast ¡Ý 4.5, etc.) for reference when tuning the UI.

## Pitfalls & Limitations
- Pixel-level diffs are brittle: rendering may change per OS, browser release, or installed fonts. The automation tolerates such variance via measurement logging instead of strict screenshots.
- Axe findings for the improved UI (two violations noted) should be reviewed manually; axe provides guidance but not final decisions.
- Responsive breakpoints are not validated here; consider adding separate suites for mobile/responsive widths.

## Rollout Recommendations
1. Run an A/B test comparing task completion speed and scan success between baseline and improved cards before a full rollout.
2. Instrument telemetry for hover duration, button activation, keyboard navigation, and focus timing to confirm the improved UI is more readable.
3. Pair the release with an accessibility audit so specialists can evaluate the axe findings and confirm ARIA semantics.
4. Gate the new experience behind a feature flag to allow gradual rollout and quick rollback if other regressions appear.
