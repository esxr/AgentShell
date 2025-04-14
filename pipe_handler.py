#!/usr/bin/env python3
"""
Pipe Handler - A utility for managing bidirectional communication with commands through named pipes.

This script provides a command-line interface to manage bidirectional communication with
any command via named pipes, allowing for process control and health monitoring.

Commands:
    setup      - Create input and output pipes if they don't exist
    start      - Start a command in the background with piped I/O
    write      - Write a message to the input pipe
    read       - Read content from the output pipe (with timeout)
    health     - Check health status of pipes and process
    cleanup    - Remove pipes and optionally terminate the process

Examples:
    # Set up the environment
    python3 pipe_handler.py setup
    
    # Start a command with pipe I/O
    python3 pipe_handler.py start "python3 my_script.py --arg1 value"
    
    # Send input and read output
    python3 pipe_handler.py write "some input"
    python3 pipe_handler.py read
    
    # Check health of pipes and process
    python3 pipe_handler.py health
    python3 pipe_handler.py health <PID>
    
    # Clean up when done
    python3 pipe_handler.py cleanup
"""
import os
import sys
import subprocess
import time
import signal
import psutil
import json

# Create the pipes if they don't exist
def setup_pipes():
    """
    Create named pipes for input and output if they don't exist.
    
    Creates:
        - input_pipe: Used to send commands to the process
        - output_pipe: Used to receive responses from the process
    
    Returns:
        None
    """
    if not os.path.exists('input_pipe'):
        os.mkfifo('input_pipe')
    if not os.path.exists('output_pipe'):
        os.mkfifo('output_pipe')
    print("Pipes created successfully.")

# Start a command in the background
def start_command(command=None):
    """
    Start a command process in the background, connecting its stdin/stdout to the pipes.
    
    Args:
        command (str): The command to execute. If None, defaults to excalidraw_agent.py
                       for backward compatibility.
    
    Returns:
        subprocess.Popen: A Popen object representing the command process
        
    Note:
        The command will receive input from input_pipe and send output to output_pipe.
        To save the process information for later use, the PID is stored in a JSON file.
    """
    # Default command for backward compatibility
    if command is None:
        print("Error: No command specified")
        sys.exit(1)
    
    # Execute the command, redirecting stdin/stdout to pipes
    full_cmd = f"{command} < input_pipe > output_pipe"
    process = subprocess.Popen(full_cmd, shell=True, executable="/bin/zsh")
    
    # Store process info for later health checks
    process_info = {
        "pid": process.pid,
        "command": command,
        "started_at": time.time()
    }
    
    # Save process info to file
    with open('.pipe_handler_process.json', 'w') as f:
        json.dump(process_info, f)
    
    print(f"Started command (PID: {process.pid}): {command}")
    return process

# Write to the input pipe
def write_to_pipe(content):
    """
    Write a message to the input pipe, which becomes stdin for the running process.
    
    Args:
        content (str): The message to send to the process
        
    Returns:
        None
    
    Raises:
        Exception: If there's an error writing to the pipe
    """
    try:
        with open('input_pipe', 'w') as f:
            f.write(content + '\n')
        print(f"Wrote to input pipe: '{content}'")
    except Exception as e:
        print(f"Error writing to input pipe: {e}")

# Read from the output pipe
def read_from_pipe():
    """
    Read content from the output pipe with a timeout.
    
    Uses a non-blocking read approach to collect all available data from the pipe
    within a specified timeout (3 seconds by default). The function reads data in
    chunks and assembles the complete output.
    
    Returns:
        str: The content read from the pipe, or an empty string if no data is available
        
    Raises:
        Exception: If there's an error reading from the pipe
    """
    try:
        # Set a timeout to avoid blocking indefinitely
        timeout = 3
        start_time = time.time()
        output = ""
        
        # Open in non-blocking mode
        fd = os.open('output_pipe', os.O_RDONLY | os.O_NONBLOCK)
        
        # Read until timeout
        while time.time() - start_time < timeout:
            try:
                # Try to read a chunk of data (4096 bytes at a time)
                chunk = os.read(fd, 4096)
                if chunk:
                    output += chunk.decode('utf-8')
                else:
                    # No more data available right now
                    time.sleep(0.1)
                    
                    # If we've collected some data and there's nothing more to read,
                    # we can return early
                    if output:
                        break
            except BlockingIOError:
                # No data available right now
                if output:
                    # If we already have some output, we can consider it complete
                    break
                time.sleep(0.1)
        
        # Close the file descriptor
        os.close(fd)
        
        if output:
            print(f"Read from output pipe: '{output.strip()}'")
        else:
            print("No data available (timeout)")
        
        return output
            
    except Exception as e:
        print(f"Error reading from output pipe: {e}")
        return ""

# Check health of pipes and process
def check_health(pid=None):
    """
    Check the health of pipes and optionally a specified process.
    
    Verifies:
        - Existence of input_pipe and output_pipe
        - Whether the specified process is running (if PID provided)
    
    Args:
        pid (int, optional): Process ID to check. If None, attempts to load from stored file.
    
    Returns:
        dict: Health status information containing:
            - input_pipe: Boolean indicating if input pipe exists
            - output_pipe: Boolean indicating if output pipe exists
            - process: Boolean indicating if process is running (if PID provided)
            - status: "healthy" or "unhealthy" overall status
    """
    health_status = {
        "input_pipe": False,
        "output_pipe": False,
        "process": False,
        "status": "unhealthy"
    }
    
    # Check if pipes exist
    if os.path.exists('input_pipe'):
        health_status["input_pipe"] = True
    if os.path.exists('output_pipe'):
        health_status["output_pipe"] = True
    
    # Try to load process info from file if no PID specified
    process_info = None
    if pid is None and os.path.exists('.pipe_handler_process.json'):
        try:
            with open('.pipe_handler_process.json', 'r') as f:
                process_info = json.load(f)
                pid = process_info.get('pid')
                health_status["command"] = process_info.get('command', 'unknown')
        except:
            pass
    
    # Check if process is running
    if pid:
        try:
            process = psutil.Process(pid)
            if process.is_running() and process.status() != 'zombie':
                health_status["process"] = True
                health_status["pid"] = pid
                
                # Get command line for verification
                cmdline = process.cmdline()
                health_status["process_cmdline"] = ' '.join(cmdline)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    # Overall health
    if health_status["input_pipe"] and health_status["output_pipe"]:
        if pid is None or health_status["process"]:
            health_status["status"] = "healthy"
    
    # Print health status
    print(f"Health check:")
    print(f"  Input pipe: {'✅ exists' if health_status['input_pipe'] else '❌ missing'}")
    print(f"  Output pipe: {'✅ exists' if health_status['output_pipe'] else '❌ missing'}")
    
    if pid:
        process_status = "✅ running" if health_status["process"] else "❌ not running"
        print(f"  Process (PID {pid}): {process_status}")
        
        if health_status["process"]:
            if "command" in health_status:
                print(f"  Command: {health_status['command']}")
            if "process_cmdline" in health_status:
                print(f"  Current cmdline: {health_status['process_cmdline']}")
    else:
        print("  Process: not specified")
    
    print(f"Overall status: {health_status['status']}")
    
    return health_status

# Cleanup function
def cleanup(pid=None):
    """
    Clean up by removing pipes and optionally terminating the process.
    
    Args:
        pid (int, optional): Process ID to terminate. If None, attempts to load from
                           stored file.
    
    Returns:
        None
    """
    # Try to load process info if no PID specified
    if pid is None and os.path.exists('.pipe_handler_process.json'):
        try:
            with open('.pipe_handler_process.json', 'r') as f:
                process_info = json.load(f)
                pid = process_info.get('pid')
        except:
            pass
    
    # Terminate process if PID is available
    if pid:
        try:
            process = psutil.Process(pid)
            process.terminate()
            print(f"Terminated process {pid}")
        except:
            try:
                # Try harder to kill the process
                os.kill(pid, signal.SIGKILL)
                print(f"Force-killed process {pid}")
            except:
                print(f"Failed to terminate process {pid}")
    
    # Remove process info file
    try:
        if os.path.exists('.pipe_handler_process.json'):
            os.unlink('.pipe_handler_process.json')
    except:
        pass
    
    # Remove pipes
    try:
        if os.path.exists('input_pipe'):
            os.unlink('input_pipe')
        if os.path.exists('output_pipe'):
            os.unlink('output_pipe')
        print("Removed pipes")
    except Exception as e:
        print(f"Error removing pipes: {e}")

def main():
    """
    Parse command-line arguments and execute the requested action.
    
    Commands:
        setup             - Create named pipes
        start [command]   - Start a command with piped I/O
        write <content>   - Write to the input pipe
        read              - Read from the output pipe
        health [pid]      - Check health of pipes and process
        cleanup [pid]     - Remove pipes and clean up
    
    Returns:
        None
    """
    if len(sys.argv) < 2:
        print("Usage: python pipe_handler.py [setup|start|write|read|health|cleanup]")
        sys.exit(1)
    
    action = sys.argv[1]
    
    if action == "setup":
        setup_pipes()
    
    elif action == "start":
        # Get command if provided, otherwise default is used
        command = None
        if len(sys.argv) >= 3:
            command = sys.argv[2]
        start_command(command)
    
    elif action == "write":
        if len(sys.argv) < 3:
            print("Error: Missing content to write")
            sys.exit(1)
        write_to_pipe(sys.argv[2])
    
    elif action == "read":
        read_from_pipe()
        
    elif action == "health":
        pid = None
        if len(sys.argv) >= 3:
            try:
                pid = int(sys.argv[2])
            except ValueError:
                print(f"Warning: Invalid PID format: {sys.argv[2]}")
        check_health(pid)
    
    elif action == "cleanup":
        pid = None
        if len(sys.argv) >= 3:
            try:
                pid = int(sys.argv[2])
            except ValueError:
                print(f"Warning: Invalid PID format: {sys.argv[2]}")
        cleanup(pid)
    
    else:
        print(f"Unknown action: {action}")
        sys.exit(1)

if __name__ == "__main__":
    main() 