# Hardening Checkpoint — sohaibshahzadflyrank.netlify.app

Tested: Aug 25, 2026, live fetch against the deployed site.

## Where it breaks

| # | Finding | Status | Evidence |
|---|---------|--------|----------|
| 1 | LinkedIn link points to literal placeholder `linkedin.com/in/[your-linkedin]` | **Fix-now** | Link text unfilled in source |
| 2 | GitHub link points to literal placeholder `github.com/[your-github]` | **Fix-now** | Link text unfilled in source |
| 3 | "CV" link → `/[link-to-your-cv.pdf]` | **Fix-now** | Fetched directly → 404 |
| 4 | "Book a call" link → `/[your-booking-link]` | **Fix-now** | Fetched directly → 404 |
| 5 | No `og:image` meta tag | **Fix-now** | Head has og:title/description/type, no image |
| 6 | Site not indexed / doesn't appear searching own name | **Known limitation** | Web search for "Sohaib Shahzad FlyRank ML Engineer" returns nothing for this site — expected for a brand-new subdomain with no backlinks yet |
| 7 | No contact form on page | **Known limitation** | N/A by design — noting explicitly rather than skipping the "test empty form" step silently |
| 8 | Custom 404 page behavior unverified | **Known limitation** | Couldn't probe an arbitrary non-existent path with available tooling — check manually in a browser |
| 9 | No measured PageSpeed score yet | **Known limitation** | Requires running pagespeed.web.dev interactively — do this yourself and record the real number |

## Fixes for the fix-nows

All four links are broken because the bracketed placeholder text was never replaced. Swap these in your source (replace `YOUR_...` with your real values):

```
[LinkedIn ↗](https://linkedin.com/in/YOUR_LINKEDIN_USERNAME)
[GitHub ↗](https://github.com/YOUR_GITHUB_USERNAME)
[CV ↗](https://sohaibshahzadflyrank.netlify.app/cv.pdf)
[Book a call ↗](https://calendly.com/YOUR_CALENDLY_USERNAME)
```
(Upload the actual `cv.pdf` to your site root so that link resolves — a link to a file that doesn't exist yet is the same bug as a bracket placeholder.)

Add an OG image tag to the frontmatter/head:
```
meta-og:image: https://sohaibshahzadflyrank.netlify.app/preview.png
```
(Needs a real 1200×630 image uploaded at that path — a solid-color card with your name and title is enough to unblock this.)

## Still needed from you before this checkpoint is truly done
- Your real LinkedIn/GitHub URLs, an actual hosted CV file, and a real booking link (or remove the button if not ready)
- A preview image for `og:image`
- Run pagespeed.web.dev on the live URL and record the actual score
- Open the site in a browser you haven't used yet (different device/browser) and click every link yourself
- Check what the Netlify 404 page shows when you visit a made-up path
