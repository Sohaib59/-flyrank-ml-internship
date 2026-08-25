# Build Log -- Content-Refresh Priority Agent (Checkpoint 1 / MVP)

## Spec, as scoped for this checkpoint
Narrowest version of the core job: given the real FlyRank dataset, produce
one client's ranked content-refresh priority queue, end to end, with real
tool calls (not a hardcoded script) doing the work.

## What I built first
Three pure Python functions (`load_dataset`, `flag_candidates`,
`rank_queue`) plus a `write_report` step, with no MCP dependency yet --
tested the actual business logic before wrapping it in any protocol, so a
bug in scoring wouldn't get confused with a bug in the wiring.

## Bug #1 -- global ranking silently favored one client
First version of `rank_queue` ranked across all 30,000 rows / 32 clients at
once. First real run: the entire top-50 queue was a single client
(`client_19581e27de`), because that client alone had 4,871 flagged rows
against a median of a few hundred per client -- any global top-K sort was
always going to fill up with whichever client had the most volume, not
whichever pages were most urgent.

**This is a correctness bug, not a style choice.** A reviewer works one
client's queue at a time; a cross-client "top 50" isn't a real work item for
anyone. Fixed by making `client_id` a required argument, not an optional
filter, and cutting cross-client ranking from this checkpoint's scope
entirely. Added a `list_clients` tool so the agent (or a person) can see the
real distribution before picking one.

## Bug #2 -- even per-client, the queue was mostly ties
After the fix, re-ran for the top client: `priority_score` standard
deviation was 0.0 across the top 20 rows. Root cause: the score was just
`2*flagA + 1*flagB + tiny_freshness_fraction`, and within one client, most
flagged rows had *both* flags true and similar ages -- so almost everything
tied at the same score, and the "ranking" was really just whatever order
pandas happened to return ties in.

**A queue where the top 20 are indistinguishable isn't a queue.** Fixed by
replacing the freshness fraction with the actual *magnitude* of the problem:
how far below the CTR threshold a page's real CTR sits, and how severe its
real `trend_pct` decline is (clipped to +/-100 after finding one outlier row
at +3458%, which is its own data-quality flag for a future week, not fixed
here). Re-tested across three different clients after the fix; spread was
real and non-zero in every case (0.03-0.06 std, meaningful given the score's
0-5 range).

## What I checked and did NOT have to fix
Every row in the top client's queue was `content_type == "keyword article"`
-- looked like a possible bug (same pattern as Bug #1), but checking the
client's full data showed 100% of their content actually is keyword
articles. Real data, not a bug. Worth being suspicious of "everything looks
the same" results, but not every one of them is broken.

## What I cut from this checkpoint's spec, and why
- **No trained model** -- the ranking score is the same transparent
  rule-based baseline validated in the FL-01/FL-02 notebooks (0.240
  precision@50), not a trained classifier. The agent upgrade this checkpoint
  demonstrates is *tool orchestration* (the model deciding which tool to
  call, on which client, in what order), not a smarter scoring function.
  Swapping in a trained model is a separate, later piece of work.
- **No cross-client summary view** -- cut alongside Bug #1's fix. Only a
  single-client queue is in scope for the MVP.
- **MCP protocol layer is untested in the build environment** -- no network
  access in the sandbox this was built in, so `pip install mcp` wasn't
  possible there. Every function the server wraps was fully tested against
  the real dataset first (see above); the protocol layer itself needs one
  local smoke test (`smoke_test.py`, included) before the first real agent
  run. This is a documented gap, not a hidden one.

## Real vs. planned deviation from FL-06
FL-06 discussed connecting *a* live tool/connector as a proof of concept
(GitHub or Google Drive, whichever was available). This checkpoint instead
builds a *custom* MCP server specific to the actual core job, because the
brief for this checkpoint asks for the agent's core job to run end to end,
not just any tool call -- a generic file-listing connector wouldn't
demonstrate the actual capstone task. The underlying protocol and
connection pattern (local MCP server, wired into Claude Desktop's config)
is the same skill either way.
