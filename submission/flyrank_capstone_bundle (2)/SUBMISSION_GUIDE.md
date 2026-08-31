# SUBMISSION_GUIDE.md — From These Files To A Graded Deliverable

This bundle contains everything drafted for you. It does **not** contain real query results — I
never had your `HF_TOKEN` or repo access, so every notebook needs one real run in Colab, and the
paper has 23 tagged spots that need real numbers pasted in. This guide is the exact path from
"files on your computer" to "submitted and gradeable."

## What's in this bundle

```
work/notebooks/w03_data_contract.ipynb
work/notebooks/w04_baseline_score.ipynb
work/notebooks/w05_model.ipynb
work/notebooks/w06_validation_audit.ipynb
work/notebooks/w07_action_playbook.ipynb
docs/index.html                  <- your deployed research paper (GitHub Pages source)
submission/paper_url.txt         <- placeholder; you'll overwrite with your real Pages URL
```

`work/figures/` and `work/outputs/` aren't included because they don't exist yet — your notebooks
create them the first time you run them.

---

## Step 1 — Get your repo locally

If you already have a repo from earlier weeks, skip to 1b.

**1a. First time — clone your existing internship repo:**
```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>
```

**1b. Already have it locally:** open a terminal in that folder and pull the latest:
```bash
cd path/to/<your-repo-name>
git pull
```

## Step 2 — Drop these files into place

Copy this bundle's folders into your repo, merging with (not replacing) whatever's already there:

```bash
# from inside your repo root
cp -r /path/to/this-bundle/work/notebooks/*.ipynb work/notebooks/
cp -r /path/to/this-bundle/docs docs
cp -r /path/to/this-bundle/submission submission
```

If `work/notebooks/w03_data_contract.ipynb` (etc.) already exist in your repo as empty skeletons,
this **overwrites** them with the filled-in versions — that's intended.

## Step 3 — Run every notebook for real, in order

Open each one in Colab (upload it, or open directly from your repo if it's connected), with your
`HF_TOKEN` set as a Colab Secret, and **Run All**:

1. `work/notebooks/w03_data_contract.ipynb`
2. `work/notebooks/w04_baseline_score.ipynb`
3. `work/notebooks/w05_model.ipynb`
4. `work/notebooks/w06_validation_audit.ipynb` — also do the manual paper-reading step in §1 here;
   nothing can fill that in for you.
5. `work/notebooks/w07_action_playbook.ipynb` — this one writes
   `work/outputs/action_playbook_queue.csv`, `work/outputs/w07_action_playbook_metrics.json`, and
   `work/figures/w07_archetype_counts.png`.

After each run, download the executed `.ipynb` from Colab (File → Download → Download .ipynb) and
overwrite the copy in `work/notebooks/` in your local repo, so the committed version shows real
outputs, not blank cells.

Also copy the generated files back into your repo if Colab ran in its own sandbox rather than
directly on your cloned repo:
```bash
cp action_playbook_queue.csv path/to/repo/work/outputs/     # this one you will NOT commit — see Step 5
cp w07_action_playbook_metrics.json path/to/repo/work/outputs/
cp w07_archetype_counts.png path/to/repo/work/figures/
```

## Step 4 — Fill in the paper

Open `docs/index.html` in a text editor. Search for the word `fill` — **23 tagged spots** in
total (some are `class="fill"`, some are `class="value fill"` or `class="num fill"` on table
cells — search for just `fill`, not the exact string `class="fill"`, so you catch all of them).

| What's tagged | Pull the real value from |
|---|---|
| Masthead status | your own draft/final label + today's date |
| Abstract result sentence (2 spots) | `work/outputs/w05_model_metrics.json` |
| Signal verdicts in Methodology (2 spots) | `w04_baseline_score.ipynb` §1 output |
| Results metric cards (3) + table (9) | `work/outputs/w05_model_metrics.json` |
| Honest split before/after paragraph | `w06_validation_audit.ipynb` §2 output |
| Error interpretation paragraph | `w05_model.ipynb` §4 / `w06` §3 |
| Archetype row counts (3 spots) | `work/outputs/w07_action_playbook_metrics.json` |
| Repo URL link | your actual GitHub repo URL |

Once a spot has a real value, remove the `fill` (or `value fill` / `num fill`) class so the yellow
highlight goes away — don't ship the page with the literal word `FILL` still visible anywhere.

Then bring in the real chart:
```bash
cp work/figures/w07_archetype_counts.png docs/figures/w07_archetype_counts.png
```

## Step 5 — Commit (mind the leak-guard)

```bash
git add work/notebooks/*.ipynb
git add work/outputs/*.json
git add work/figures/*.png
git add docs/
git status
```

Check the `git status` output before committing: `work/outputs/action_playbook_queue.csv` (and any
other queue CSV) should **not** appear as staged — those are data files the CI leak-guard blocks
and your notebooks regenerate every run. If your repo already has a `.gitignore` covering
`work/outputs/*.csv`, it won't show up at all; if not, just don't `git add` it.

```bash
git commit -m "Complete w03-w07, deploy capstone paper"
git push
```

## Step 6 — Turn on GitHub Pages

1. On GitHub, open your repo → **Settings** → **Pages**.
2. Under "Build and deployment" → **Source**, choose "Deploy from a branch".
3. **Branch:** your default branch (usually `main`) → **Folder:** `/docs`.
4. Save. GitHub shows a URL shortly after, in the form:
   `https://<your-username>.github.io/<your-repo-name>/`
5. Wait 1-2 minutes, then open that URL in a private/incognito window and confirm:
   - the page loads with no `FILL` text visible anywhere,
   - the archetype chart image actually renders (not a broken-image icon),
   - every nav link at the top jumps to the right section.

## Step 7 — Point your repo at the live paper

```bash
echo "https://<your-username>.github.io/<your-repo-name>/" > submission/paper_url.txt
git add submission/paper_url.txt
git commit -m "Point paper_url.txt at deployed capstone"
git push
```

Open `submission/paper_url.txt` on GitHub afterward and confirm it holds **exactly one line** —
the direct URL, nothing else, no trailing extra lines.

## Step 8 — Final pre-submit checklist

- [ ] All 23 `fill`-tagged values in `docs/index.html` replaced with real numbers; no literal
      `FILL` text remains anywhere on the live page.
- [ ] `docs/figures/w07_archetype_counts.png` present and rendering on the live page.
- [ ] Live paper URL opens correctly in a private/incognito browser window.
- [ ] `submission/paper_url.txt` at repo root, one line, exact deployed URL.
- [ ] `work/notebooks/w03`–`w07` all show **executed** outputs (real tables, real numbers) when
      viewed on GitHub — not blank/unrun cells.
- [ ] `work/outputs/*.json` metrics files committed; `work/outputs/*.csv` queue files are **not**
      committed.
- [ ] No client name, domain, URL, raw query, or content title anywhere in the paper or repo.
- [ ] No sentence anywhere claims to "prove," "cause," or "guarantee" an outcome — only observed /
      measured / directional / decision-support language.

## Step 9 — Submit

On the capstone card in your portal, submit **your repo URL only**:
```
https://github.com/<your-username>/<your-repo-name>
```
That's the single thing graders need — they find your live paper through `submission/paper_url.txt`
and your executed notebooks through `work/notebooks/`.
