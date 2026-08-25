# Fix Log: Mobile & Accessibility Pass

Audited at three real widths (375px / phone, 768px / tablet, 1280px / desktop)
using rendered screenshots at each width, plus direct measurement of CSS
values (font sizes, tap-target dimensions, contrast ratios) rather than
eyeballing.

## Fixed

**1. Form inputs would trigger iOS Safari's auto-zoom-on-focus bug**
- Found: `input`/`textarea` font-size was 15px. iOS Safari automatically
  zooms the whole page in when a visitor taps into any form field smaller
  than 16px — a well-known, easy-to-miss mobile bug that makes a form feel
  broken on a real phone even though it looks fine in a resized browser
  window.
- Fixed: bumped to 16px, the minimum that keeps Safari from zooming.

**2. Nav links and the submit button had tap targets under the ~44px minimum**
- Found: nav links had only 3px of bottom padding and no horizontal padding
  — the actual clickable area was just the text's line height, well under
  a comfortable thumb target. The submit button measured ~40px tall
  (11px padding + text), just under the 44px guideline.
- Fixed: added real padding around each nav link (and a matching negative
  margin on the container so visual alignment didn't shift), and increased
  button padding with an explicit `min-height: 44px`.

**3. (Side effect of fix #2) Nav links visually indented after adding padding**
- Found: once links got padding for tap-target size, "LinkedIn" no longer
  lined up with the heading text above it — looked like a layout bug I'd
  introduced.
- Fixed: negative left margin on the nav container to cancel the new
  padding's visual offset while keeping the larger clickable area. Verified
  with a re-render that alignment matched the original.

## Checked, genuinely fine — no fix needed

- **Text contrast**: computed (not eyeballed) via the WCAG relative-luminance
  formula for every text color actually used, including ones added since
  the last identity-kit check: muted label text on background = 4.83:1,
  error message red on background = 5.47:1, success message green on
  background = 4.78:1. All clear the 4.5:1 AA minimum.
- **Horizontal overflow**: none at 375px, 768px, or 1280px — content stays
  within its max-width container at every size, confirmed by screenshot.
- **Viewport meta tag**: present and correct.
- **Work-image crispness/compression**: not yet applicable — the Work
  section doesn't have real case-study screenshots embedded on the live
  site yet (case study content is currently text-only, "coming soon").
  This check needs to be re-run once real images are added.

## Not fixed — blocks the "click every link" pass criterion

- **LinkedIn, GitHub, CV, and "Book a call" links are literally
  placeholder text right now** (`[your-linkedin]`, `[your-github]`, etc.),
  not real URLs. These are currently broken links on the live site. This
  is the single biggest remaining item before this page can honestly pass
  a "click every link" check — I can't fill in real profile URLs on
  someone else's behalf, so this is flagged here rather than glossed over.

## Before / after (phone width, 375px)

Before: nav links cramped together with no tap padding, form inputs at
15px risking iOS auto-zoom, submit button under 44px tall.

After: same visual density and alignment, but every interactive element
now meets real mobile tap-target and zoom-prevention thresholds.

(See `mobile_after_final.png` for the corrected render. A true device
screenshot — not a resized-browser or headless render — is still the one
piece of evidence only a real phone can provide; take that after
redeploying.)
