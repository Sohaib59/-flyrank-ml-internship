"""
Run this ONCE after `pip install -r requirements.txt`, before wiring the
server into Claude Desktop. It imports the server module directly (not over
the MCP wire protocol) just to confirm every tool function runs without
crashing against the real CSV, on your machine, with the real `mcp` package
installed -- something the sandbox this was built in could not verify
(no network access there). If this prints all three "OK" lines, the MCP
wiring in Claude Desktop is very likely to work.
"""
import server

print("1) load_and_flag_dataset:")
print("   " + server.load_and_flag_dataset())
print("   OK\n")

print("2) list_clients (first few lines):")
out = server.list_clients()
print("   " + out.splitlines()[0])
print("   OK\n")

first_client = out.splitlines()[0].split(":")[0]
print(f"3) build_priority_queue('{first_client}', top_k=5):")
out2 = server.build_priority_queue(first_client, top_k=5)
print("   " + out2.splitlines()[0])
print("   OK\n")

print("All three tools ran successfully. Safe to connect this server to Claude Desktop.")
