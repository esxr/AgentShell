# AgentShell Examples

This directory contains example applications that can be used with AgentShell for interactive control.

## Available Examples

### 1. Echo Tool (`echo_tool.py`)

A simple Python-based interactive text transformation tool that:

- Reads from stdin and transforms the input
- Supports commands: upper, lower, reverse, count
- Demonstrates basic interactive I/O with AgentShell

Usage with AgentShell:

```bash
python3 ../AgentShell.py setup
python3 ../AgentShell.py start "./echo_tool.py"
python3 ../AgentShell.py send "upper hello world"
python3 ../AgentShell.py receive
python3 ../AgentShell.py end
```

### 2. Node.js Interactive Server (`nodejs_server.js`)

A more complex example with both an HTTP server and CLI interface:

- HTTP server with endpoints for the web
- Interactive command-line interface for management
- Demonstrates how AgentShell can control server applications

Usage with AgentShell:

```bash
python3 ../AgentShell.py setup
python3 ../AgentShell.py start "node nodejs_server.js"
python3 ../AgentShell.py send "help"
python3 ../AgentShell.py receive
python3 ../AgentShell.py send "start"
python3 ../AgentShell.py receive

# In a different terminal:
curl http://localhost:3000/
curl http://localhost:3000/echo/hello-world

# Continue in the original terminal:
python3 ../AgentShell.py send "stop"
python3 ../AgentShell.py receive
python3 ../AgentShell.py end
```

## Creating Your Own Examples

When creating your own interactive applications for use with AgentShell:

1. Ensure your application reads from stdin and writes to stdout
2. Handle input and output buffering appropriately
3. Implement proper error handling for broken pipes
4. Include graceful shutdown mechanisms
5. Provide clear command help for users
