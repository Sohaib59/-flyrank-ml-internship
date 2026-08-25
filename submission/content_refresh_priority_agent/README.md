# Content-Refresh Priority Agent

The core job: given FlyRank's content dataset, build a ranked, per-client
"refresh this first" queue for a reviewer, using two transparent rule-based
signals as reason codes.

This is an MCP server exposing three tools:
- `load_and_flag_dataset` -- load the CSV, compute reason-code flags
- `list_clients` -- see which clients have flagged pages, and how many
- `build_priority_queue(client_id, top_k)` -- rank one client's queue, write a CSV

The **agent** part is not this server -- it's Claude, running in Claude
Desktop, deciding on its own which of these three tools to call, in what
order, based on what it learns from each result. This server just gives it
real hands to do the job with.

## 1. Install (on your machine, not the sandbox this was built in)

```bash
cd agent_build
pip install -r requirements.txt
```

## 2. Smoke-test before wiring it into Claude Desktop

```bash
python3 smoke_test.py
```
You should see three "OK" lines. If this fails, fix it here first --
don't debug the MCP wiring and the business logic at the same time.

## 3. Connect it to Claude Desktop

Open your Claude Desktop config file:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Add this (create the file if it doesn't exist), replacing the path with the
**absolute path** to this folder on your machine:

```json
{
  "mcpServers": {
    "content-refresh-priority-agent": {
      "command": "python3",
      "args": ["/absolute/path/to/agent_build/server.py"]
    }
  }
}
```

Restart Claude Desktop completely (quit, not just close the window). You
should see a small tool/hammer icon indicating connected tools.

## 4. Run the actual agent -- this is what you screen-record

Start a new chat in Claude Desktop and type something like:

> "Using the content-refresh-priority-agent tools, find the client with the
> most flagged pages and build me their top-20 refresh priority queue.
> Tell me what you found and why those pages are flagged."

Watch what happens: Claude should call `load_and_flag_dataset` first, then
`list_clients`, read the result, pick the top client itself, then call
`build_priority_queue` with that client's real ID -- three live tool calls,
each one informed by the previous result, with no code from you in between.
That decision sequence (which client, in what order) is the model's, not a
script's -- that's the actual "agent" behavior this whole exercise is about.

Record this from the moment you send the message to the moment it finishes
and gives you the final queue. About 2 minutes, unedited.

## Known limitation (see build_log.md)

The MCP protocol layer (`server.py`) was written but not run in the
environment that built it -- no network access there to `pip install mcp`.
Every function it wraps (`core_logic.py`) was fully tested against the real
30,000-row dataset first. Run `smoke_test.py` before your recorded run so
you're not debugging the protocol and the recording at the same time.
