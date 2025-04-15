# AgentShell

A utility that enables AI agents to interact with command-line tools that require input.

## Overview

This tool makes it possible for AI Agents to interact with any command-line program that expects user input, especially interactive tools like REPLs, shell sessions, and text-based applications. It's particularly useful when:

- Working with AI assistants or tools that don't natively support interactive input
- Running interactive sessions in the background
- Sending input to and receiving output from long-running processes
- Working with interactive shells, interpreters, or REPLs

## Installation

### Requirements

- Python 3.6+
- `psutil` package

### Setup

```bash
# Install dependencies
pip install psutil
```

## Basic Usage

The AgentShell tool provides these commands:

```
python3 AgentShell.py [setup|start|send|receive|status|end]
```

### Command Reference

- `setup`: Initialize the environment for the interactive session
- `start [command]`: Start an interactive command in the background
- `send <input>`: Send input to the running command
- `receive`: Receive output from the command (with timeout)
- `status [pid]`: Check status of the interactive session
- `end [pid]`: End the interactive session and clean up

## Examples

### Example 1: Interactive Python Interpreter

```bash
# Set up the environment
$ python3 AgentShell.py setup
AgentShell session ready.

# Start Python in interactive mode
$ python3 AgentShell.py start "python3 -i"
Started interactive command (PID: 12345): python3 -i

# Send a Python expression
$ python3 AgentShell.py send "print(2 + 2)"
Sent: 'print(2 + 2)'

# Read the output
$ python3 AgentShell.py receive
Received: 'Python 3.10.0 (default, Oct 12 2023, 15:21:12)
>>> 4
>>> '

# Check status
$ python3 AgentShell.py status
AgentShell status:
  Input channel: ✅ ready
  Output channel: ✅ ready
  Command (PID 12345): ✅ running
  Running: python3 -i
Overall status: healthy

# Clean up when done
$ python3 AgentShell.py end
Terminated command (PID 12345)
AgentShell session ended.
```

### Example 2: Working with a Shell

```bash
# Set up the session
$ python3 AgentShell.py setup
AgentShell session ready.

# Start a bash shell
$ python3 AgentShell.py start "bash"
Started interactive command (PID: 12346): bash

# Send a command
$ python3 AgentShell.py send "echo Hello, World!"
Sent: 'echo Hello, World!'

# Read the output
$ python3 AgentShell.py receive
Received: 'Hello, World!'

# Send another command
$ python3 AgentShell.py send "ls -la"
Sent: 'ls -la'

# Read the directory listing output
$ python3 AgentShell.py receive
Received: 'total 32
drwxr-xr-x  8 user  staff   256 Apr 10 15:42 .
drwxr-xr-x  5 user  staff   160 Apr 10 14:20 ..
...'

# End the session
$ python3 AgentShell.py end
Terminated command (PID 12346)
AgentShell session ended.
```

### Example 3: Working with Custom Interactive Scripts

```bash
# Set up the session
$ python3 AgentShell.py setup
AgentShell session ready.

# Start the custom script
$ python3 AgentShell.py start "./echo_transformer.py"
Started interactive command (PID: 12347): ./echo_transformer.py

# Send a command to transform text
$ python3 AgentShell.py send "upper hello world"
Sent: 'upper hello world'

# Receive the transformed output
$ python3 AgentShell.py receive
Received: 'Echo Transformer (Ctrl+C to exit)
Commands: upper, lower, reverse, count, quit/exit
> HELLO WORLD'

# End the session
$ python3 AgentShell.py end
Terminated command (PID 12347)
AgentShell session ended.
```

### Example 4: Interactive Node.js Server

```bash
# Set up the session
$ python3 AgentShell.py setup
AgentShell session ready.

# Start the Node.js server
$ python3 AgentShell.py start "node server.js"
Started interactive command (PID: 96992): node server.js

# View server help commands
$ python3 AgentShell.py send "help"
Sent: 'help'

# Receive the help output
$ python3 AgentShell.py receive
Received: 'Interactive Node.js Server
Type "help" for available commands
server> Available commands:
  start [port]  - Start the server (optional port)
  stop          - Stop the server
  status        - Check server status
  help          - Show this help
  exit          - Exit the program
server>'

# Start the HTTP server
$ python3 AgentShell.py send "start"
Sent: 'start'

# Test the HTTP server with curl
$ curl -s http://localhost:3000/
Welcome to the interactive Node.js server!

# Test the echo endpoint
$ curl -s http://localhost:3000/echo/hello-world
Echo: hello-world

# Stop the server
$ python3 AgentShell.py send "stop"
Sent: 'stop'

# End the session
$ python3 AgentShell.py end
Terminated command (PID 96992)
AgentShell session ended.
```

## Troubleshooting

### Common Issues

1. **No output available (timeout)**
   If the receive command returns "No output available", the command might not have generated output yet. Try:

   - Checking if the command is running with `status`
   - Waiting a bit longer and trying again
   - Checking if the command requires additional input

2. **Command termination failures**
   If you see "Failed to terminate command", you can manually terminate it:

   ```bash
   $ kill -9 [PID]
   ```

3. **Module not found: psutil**
   Install the psutil module:
   ```bash
   $ pip install psutil
   ```

## Implementation Details

This tool uses named pipes (FIFOs) to create communication channels between processes. For more details on how it works, see the comments in the source code.
