# Pipe Handler

A utility for managing bidirectional communication with commands through named pipes.

## Overview

Pipe Handler provides a command-line interface to manage bidirectional communication with any command via named pipes, allowing for process control and health monitoring. It's useful for:

- Running long-lived processes in the background
- Communicating with interactive processes via stdin/stdout
- Monitoring process health and pipe status
- Managing cleanup of processes and pipes

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

Pipe Handler provides several commands for managing piped communication:

```
python3 pipe_handler.py [setup|start|write|read|health|cleanup]
```

### Command Reference

- `setup`: Create input and output pipes if they don't exist
- `start [command]`: Start a command in the background with piped I/O
- `write <content>`: Write a message to the input pipe
- `read`: Read content from the output pipe (with timeout)
- `health [pid]`: Check health status of pipes and process
- `cleanup [pid]`: Remove pipes and optionally terminate the process

## Examples

### Example 1: Simple Echo with `cat`

```bash
# Set up the pipes
$ python3 pipe_handler.py setup
Pipes created successfully.

# Start the cat command
$ python3 pipe_handler.py start "cat"
Started command (PID: 99311): cat

# Write to the input pipe
$ python3 pipe_handler.py write 'Hello world'
Wrote to input pipe: 'Hello world'

# Read from the output pipe
$ python3 pipe_handler.py read
Read from output pipe: 'Hello world'

# Check health
$ python3 pipe_handler.py health
Health check:
  Input pipe: ✅ exists
  Output pipe: ✅ exists
  Process (PID 99311): ✅ running
  Command: cat
  Current cmdline: /bin/zsh -c cat < input_pipe > output_pipe
Overall status: healthy

# Clean up
$ python3 pipe_handler.py cleanup
Terminated process 99311
Removed pipes
```

### Example 2: Interactive Python Interpreter

```bash
# Set up the pipes
$ python3 pipe_handler.py setup
Pipes created successfully.

# Start Python in interactive mode
$ python3 pipe_handler.py start "python3 -i"
Started command (PID: 99469): python3 -i

# Send a Python expression
$ python3 pipe_handler.py write 'print(2 + 2)'
Wrote to input pipe: 'print(2 + 2)'

# Read the output
$ python3 pipe_handler.py read
Python 3.12.9 (main, Feb  4 2025, 14:38:38) [Clang 16.0.0 (clang-1600.0.26.6)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> >>>
Read from output pipe: '4'

# Clean up when done
$ python3 pipe_handler.py cleanup
Removed pipes
```

### Example 3: Using with the Excalidraw Agent

```bash
# Set up the pipes
$ python3 pipe_handler.py setup
Pipes created successfully.

# Start the excalidraw agent (default if no command specified)
$ python3 pipe_handler.py start
Started command (PID: 96364): source .venv/bin/activate && python3 excalidraw_agent.py --interactive

# Send a prompt
$ python3 pipe_handler.py write "hello"
Wrote to input pipe: 'hello'

# Read response
$ python3 pipe_handler.py read
Read from output pipe: 'Excalidraw Generator (press Ctrl+C to exit)
--------------------------------------
Type 'reset' to start a new conversation, or 'exit'/'quit'/'q' to exit

What would you like to draw?'

# Check health with PID
$ python3 pipe_handler.py health 96364
Health check:
  Input pipe: ✅ exists
  Output pipe: ✅ exists
  Process (PID 96364): ✅ running
  Process verification: ✅ confirmed as excalidraw agent
Overall status: healthy

# Clean up
$ python3 pipe_handler.py cleanup
Removed pipes
```

## Troubleshooting

### Common Issues

1. **Process termination failures**
   If you see "Failed to terminate process", the process might have already exited or might require a stronger signal. You can try:

   ```bash
   $ kill -9 [PID]
   ```

2. **No data available (timeout)**
   If the read command returns "No data available", the process might not have generated output yet. Try:

   - Increasing the timeout (modify the `timeout` variable in the `read_from_pipe` function)
   - Ensuring that the process is still running with `health` command
   - Checking if the process requires additional input

3. **Module not found: psutil**
   Install the psutil module:
   ```bash
   $ pip install psutil
   ```
   Or use your virtual environment:
   ```bash
   $ source .venv/bin/activate && pip install psutil
   ```

## Advanced Usage

### Process Management

The pipe handler stores process information in a hidden file (`.pipe_handler_process.json`), which allows commands like `health` and `cleanup` to work without explicitly providing a PID.

### Custom Commands

You can run any command that can accept stdin and produce stdout:

```bash
# Run a custom script
$ python3 pipe_handler.py start "./my_script.sh"

# Run a command with arguments
$ python3 pipe_handler.py start "grep -i pattern"

# Run a Python script
$ python3 pipe_handler.py start "python3 my_script.py --arg1 value"
```

### Environment Setup

For commands that require specific environment setup:

```bash
$ python3 pipe_handler.py start "source .venv/bin/activate && python3 my_script.py"
```
