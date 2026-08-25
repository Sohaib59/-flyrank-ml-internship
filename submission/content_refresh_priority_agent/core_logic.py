"""
Core job logic for the content-refresh priority agent.
Pure functions, no MCP/network dependency, so they can be unit-tested directly
before ever being wrapped in a server.
"""
import pandas as pd

# Named thresholds (see FL-01/FL-02 notebooks for where these came from)
MIN_IMPRESSIONS_FOR_DEMAND = 100
MIN_IMPRESSIONS_FOR_CTR_CHECK = 500
MAX_POSITION_FOR_CTR_CHECK = 20
LOW_CTR_THRESHOLD_PCT = 0.5


def load_dataset(path: str) -> pd.DataFrame:
    """Load and apply the same row filters used throughout the FL notebooks."""
    df = pd.read_csv(path)
    df = df[(df["impressions_90d"] > 0) & (df["content_age_days"] >= 90)].copy()
    df = df.drop_duplicates(subset="content_id").reset_index(drop=True)
    return df


def flag_candidates(df: pd.DataFrame) -> pd.DataFrame:
    """Attach two independent rule-based reason-code flags to every row."""
    df = df.copy()
    df["flag_declining_with_demand"] = (
        (df["trend_direction"] == "down") & (df["impressions_90d"] >= MIN_IMPRESSIONS_FOR_DEMAND)
    )
    df["flag_low_ctr_visible"] = (
        (df["impressions_90d"] >= MIN_IMPRESSIONS_FOR_CTR_CHECK)
        & (df["avg_position"] > 0)
        & (df["avg_position"] <= MAX_POSITION_FOR_CTR_CHECK)
        & (df["ctr"] < LOW_CTR_THRESHOLD_PCT)
    )
    df["any_flag"] = df["flag_declining_with_demand"] | df["flag_low_ctr_visible"]
    return df


def rank_queue(df: pd.DataFrame, client_id: str, top_k: int = 50) -> pd.DataFrame:
    """
    Rank ONE client's flagged candidates into a reviewer-sized queue.

    BUILD NOTE (see build log): v1 ranked globally across all 32 clients and
    the top-50 queue silently filled up with a single high-volume client
    (client_19581e27de had 4,871 flagged rows vs. a median of a few hundred
    per client), starving every other client's review time. A reviewer works
    one client at a time, so client_id is now a REQUIRED argument, not an
    optional filter -- this is a scope cut, not a nice-to-have.

    Score = simple, transparent weighted sum of the two flags plus a freshness
    tie-breaker. This is the same transparency-first baseline logic already
    validated in the FL notebooks (0.240 precision@50) -- not the trained
    model, which doesn't exist yet. The agent upgrade here is orchestration,
    not a smarter model.
    """
    df = df[df["client_id"] == client_id].copy()
    if df.empty:
        raise ValueError(f"No rows found for client_id={client_id!r} after filtering.")

    # BUILD NOTE #2: the first scoring attempt (2*flagA + 1*flagB + tiny freshness
    # fraction) produced a queue with almost zero spread -- most flagged rows for
    # a given client share both flags, so the two booleans alone can't rank them
    # against each other. Swapped in the actual magnitude of decline (trend_pct,
    # clipped to a sane range since one outlier hit +3458%) and how far CTR sits
    # below the threshold, so rows with the same flags still rank by how bad the
    # underlying number actually is -- a queue where most rows tie isn't a queue.
    trend_severity = df["trend_pct"].clip(lower=-100, upper=100).abs() / 100  # 0-1
    ctr_gap = (LOW_CTR_THRESHOLD_PCT - df["ctr"]).clip(lower=0) / LOW_CTR_THRESHOLD_PCT  # 0-1

    df["priority_score"] = (
        df["flag_declining_with_demand"].astype(int) * 2
        + df["flag_low_ctr_visible"].astype(int) * 1
        + trend_severity.fillna(0) * df["flag_declining_with_demand"].astype(int)
        + ctr_gap.fillna(0) * df["flag_low_ctr_visible"].astype(int)
    )
    queue = df[df["any_flag"]].sort_values("priority_score", ascending=False).head(top_k)
    return queue


def list_clients(df: pd.DataFrame) -> pd.DataFrame:
    """Helper tool: show which clients actually have flagged candidates, and how many."""
    flagged = df[df["any_flag"]]
    return (
        flagged.groupby("client_id").size().sort_values(ascending=False)
        .rename("flagged_count").reset_index()
    )


def write_report(queue: pd.DataFrame, out_path: str) -> str:
    """Write the final ranked queue as a clean CSV a reviewer could actually open."""
    cols = [
        "content_id", "client_id", "content_type", "priority_score",
        "flag_declining_with_demand", "flag_low_ctr_visible",
        "impressions_90d", "ctr", "avg_position", "days_since_last_update",
    ]
    queue[cols].to_csv(out_path, index=False)
    return out_path
