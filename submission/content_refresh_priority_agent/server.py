"""
Content-Refresh Priority Agent -- MCP server.

Exposes the core job (build a per-client refresh priority queue from the
FlyRank content dataset) as MCP tools, so an agent (Claude Desktop, or any
MCP client) can call them dynamically based on what it finds along the way,
instead of running a hardcoded script.

BUILD NOTE: this file could not be run inside the sandbox this was built in
(no network access there, so `pip install mcp` was not possible). Every
function in core_logic.py was fully tested against the real dataset before
being wrapped here (see build_log.md) -- this file adds the MCP protocol
layer on top of already-verified logic, and needs to be smoke-tested once on
a machine with the `mcp` package installed (see README's first-run check).

Run locally with:  pip install mcp pandas  &&  python server.py
Then point Claude Desktop's config at this file (see claude_desktop_config
snippet in README.md).
"""
from mcp.server.fastmcp import FastMCP
import core_logic as core

DATASET_PATH = "content_refresh_anonymized.csv"  # place next to this file, or edit the path

mcp = FastMCP("content-refresh-priority-agent")

# Module-level cache so we don't re-read the CSV on every single tool call
# within one agent run.
_state = {"df": None}


def _get_flagged_df():
    if _state["df"] is None:
        df = core.load_dataset(DATASET_PATH)
        df = core.flag_candidates(df)
        _state["df"] = df
    return _state["df"]


@mcp.tool()
def load_and_flag_dataset() -> str:
    """
    Load the content-refresh dataset and compute the two reason-code flags
    (declining_with_demand, low_ctr_visible) on every row. Call this first,
    before list_clients or build_priority_queue -- they depend on it.
    Returns a short summary so the agent knows the load succeeded and how
    big the flagged pool is before deciding what to do next.
    """
    df = _get_flagged_df()
    return (
        f"Loaded {len(df):,} rows after filters (impressions_90d > 0, "
        f"content_age_days >= 90, deduplicated by content_id). "
        f"{int(df['any_flag'].sum()):,} rows carry at least one flag."
    )


@mcp.tool()
def list_clients() -> str:
    """
    List every client that has at least one flagged candidate, with a count,
    sorted highest-volume first. Call this before build_priority_queue if you
    don't already know which client_id to build a queue for.
    """
    df = _get_flagged_df()
    counts = core.list_clients(df)
    lines = [f"{r.client_id}: {r.flagged_count} flagged pages" for r in counts.itertuples()]
    return "\n".join(lines[:15]) + (f"\n...and {len(lines)-15} more clients" if len(lines) > 15 else "")


@mcp.tool()
def build_priority_queue(client_id: str, top_k: int = 20) -> str:
    """
    Build a ranked content-refresh priority queue for ONE client.
    Returns the top_k pages as a readable table (content_id, why it was
    flagged, and the key numbers a reviewer would want to see), and writes
    the full result to priority_queue_<client_id>.csv in the working
    directory. Requires load_and_flag_dataset to have been called first.
    """
    df = _get_flagged_df()
    queue = core.rank_queue(df, client_id=client_id, top_k=top_k)
    out_path = f"priority_queue_{client_id}.csv"
    core.write_report(queue, out_path)

    lines = [f"Wrote {len(queue)} rows to {out_path}\n"]
    lines.append(f"{'content_id':<24} {'score':>6}  {'declining':>9}  {'low_ctr':>7}  ctr    pos")
    for r in queue.itertuples():
        lines.append(
            f"{r.content_id:<24} {r.priority_score:>6.2f}  "
            f"{str(r.flag_declining_with_demand):>9}  {str(r.flag_low_ctr_visible):>7}  "
            f"{r.ctr:<5} {r.avg_position}"
        )
    return "\n".join(lines)


if __name__ == "__main__":
    mcp.run(transport="stdio")
