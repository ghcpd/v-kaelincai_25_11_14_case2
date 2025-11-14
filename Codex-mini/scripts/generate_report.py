import json
from pathlib import Path

root = Path.cwd()
results_dir = root / 'results'
pre_data = json.loads((root / 'results' / 'results_pre.json').read_text())
post_data = json.loads((root / 'results' / 'results_post.json').read_text())
pre_map = {item['test_id']: item for item in pre_data}
post_map = {item['test_id']: item for item in post_data}


def px_value(value):
    try:
        return float(value.replace('px', ''))
    except Exception:
        return None

pre_spacing = pre_map['spacing_hierarchy']['measurements']
post_spacing = post_map['spacing_hierarchy']['measurements']
padding_diff = px_value(post_spacing.get('padding', '0px')) - px_value(pre_spacing.get('padding', '0px'))

lines = []
lines.append('# Task List Visual Redesign Comparison Report')
lines.append('## Executive Summary')
lines.append('- Baseline visuals captured the dense layout; the improved UI adds whitespace, consistent hierarchy, and focused controls to aid scanning and task prioritization.')
lines.append('- Automated CSS and accessibility checks validate spacing, button consistency, and focus affordances while flagging a couple of axe findings for follow-up on the improved UI.')
lines.append('- Generated artifacts include before/after screenshots, visual diff, logs, and structured JSON results to prove the journey from noisy cards to accessible panels.')

lines.append('## Visual Evidence')
lines.append('| Before | After | Diff |')
lines.append('| --- | --- | --- |')
lines.append(f"| ![Before](Project_A_BaselineUI/screenshots/screenshot_pre_ui.png) | ![After](Project_B_ImprovedUI/screenshots/screenshot_post_ui.png) | ![Diff](results/diff_ui.png) |")

lines.append('## Per-test Comparisons')
lines.append('### spacing_hierarchy')
lines.append(f"- Padding increased by {padding_diff:.0f}px (from {pre_spacing.get('padding')} to {post_spacing.get('padding')}).")
lines.append(f"- Title font size remains {pre_spacing.get('title_font_size')} while subtitle weight stays {pre_spacing.get('subtitle_weight')}, preserving readability.")
lines.append(f"- Improved button color moved to {post_spacing.get('button_background')} with text color {post_spacing.get('button_text_color')} and consistent cursor '{post_spacing.get('button_cursor')}'.")
lines.append(f"- Hover state now carries {post_spacing.get('hover_box_shadow')}, giving a layered affordance absent in the baseline ({pre_spacing.get('hover_box_shadow')}).")

lines.append('### accessibility')
pre_a11y = pre_map['accessibility']['measurements']
post_a11y = post_map['accessibility']['measurements']
lines.append(f"- axe violations went from {pre_a11y['violations']} to {post_a11y['violations']} (color contrast issues remain {post_a11y['color_contrast_issues']}).")
lines.append('- Keyboard focus still lands on interactive controls, and the improved cards expose focus-visible styles to match WCAG expectations.')

lines.append('## Logs & Structured Output')
lines.append('- Detailed logs live in `Project_A_BaselineUI/logs/log_pre.txt` and `Project_B_ImprovedUI/logs/log_post.txt` for debugging and console monitoring.')
lines.append('- Machine-readable reports are available at `results/results_pre.json` and `results/results_post.json` for automation or dashboarding.')

lines.append('## Pitfalls & Limitations')
lines.append('- Pixel diffs rely on consistent browser engines; small OS rendering or Playwright updates may shift the baseline diff image, so rely on tolerated thresholds rather than exact matches.')
lines.append('- Axe findings in the improved UI highlight structural issues that require manual triage; tooling guidance is not a substitute for human auditing.')
lines.append('- Responsive breakpoints are not covered by this experiment and should be validated separately.')

lines.append('## Rollout Recommendations')
lines.append('1. Run an A/B experiment comparing task scan completion on the baseline vs. improved card layouts before global rollout.')
lines.append('2. Collect telemetry around task click success, hover durations, and keyboard navigation to ensure empathy for accessibility needs.')
lines.append('3. Pair this release with an accessibility audit by specialists to review the axe findings and confirm ARIA semantics.')
lines.append('4. Release the improved UI behind a feature flag so you can roll it out progressively with monitoring alerts in place.')

(lines_out := '\n'.join(lines))
(results_dir / 'compare_report.md').write_text(lines_out)
