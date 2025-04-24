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

### 2. Calculator Tool (`calculator.py`)

An interactive command-line calculator that:

- Reads expressions from stdin and outputs results to stdout
- Supports basic arithmetic operations: add, subtract, multiply, divide
- Provides algebraic expression evaluation with the eval command
- Includes trigonometric functions: sin, cos, tan
- Can convert degrees to radians with the deg command
- Solves algebraic equations with the solve command
- Demonstrates more complex interactive processing with AgentShell

Usage with AgentShell:

```bash
python3 ../AgentShell.py setup
python3 ../AgentShell.py start "./calculator.py"
python3 ../AgentShell.py send "add 5 3"
python3 ../AgentShell.py receive
python3 ../AgentShell.py send "eval 2*(3+4)"
python3 ../AgentShell.py receive
python3 ../AgentShell.py send "solve x+5=10"
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
