# AgentShell

A cursor utility file that enables AI agents to interact with interactive REPL-style or shell-like command-line tools.

## Usage Instructions
Just paste this file in your workspace and give a query like so:
```
Create a commandline tool called calculator.py in @examples. Make one feature at a time (e.g. first numerical, then algebraic, and then trigonometric). ALWAYS use @AgentShell.py to test it at every turn and interact with it. CAREFULLY READ the instructions in @AgentShell.py to learn how to use it. Activate the virtual environment beforehand.
```

## Problems
This was made to solve the following problems.

![Cursor agent mode - when running terminal commands often hangs up the terminal, requiring a click to pop it out in order to continue commands](<media/Screenshot 2025-04-24 at 12.47.58 pm.png>)

![The cursor agent doesn't support "interactive" commands. For example, if the command requires further input, sometimes cursor agent just hangs and waits for me to input y/n or other input to the interactive command, even in yolo mode](<media/Screenshot 2025-04-24 at 12.48.52 pm.png>)

## Demo

![AgentShell Demo](<media/AgentShell.gif>)

Watch the video: https://www.youtube.com/watch?v=LPHC2ZC2UrU

## Prerequisites

- Python 3.6+
- `psutil` package


## Command Reference

The AgentShell tool provides these commands:

```
python3 AgentShell.py [setup|start|send|receive|status|end]
```

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

## Contribution
Please feel free to improve the file for your usecases and submit a PR