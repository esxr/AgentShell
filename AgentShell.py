#!/usr/bin/env python3
"""
AgentShell - Enable AI agents to interact with command-line tools that require input.

This script provides a command-line interface for AI agents to interact with any command-line tool that
requires user input, allowing asynchronous sending of input and receiving of output.

Commands:
    setup       - Initialize the environment for interactive commands
    start       - Start an interactive command in the background
    send        - Send input to the running command
    receive     - Receive output from the command (with timeout)
    status      - Check status of the interactive session
    end         - End the interactive session and clean up

# IMPORTANT: activate the virtual environment
# AgentShell works best in virtual environment

Examples:
    # Pre-requisites:
    # IMPORTANT: activate the virtual environment
    # AgentShell works best in virtual environment
    source .venv/bin/activate
    
    # install the dependencies
    pip install psutil

    # Set up the environment
    python3 AgentShell.py setup

    # Start an interactive Python session
    python3 AgentShell.py start "python3 -i"

    # Send input and receive output
    python3 AgentShell.py send "print('Hello world')"
    python3 AgentShell.py receive

    # Check status of the session
    python3 AgentShell.py status

    # End the session when done
    python3 AgentShell.py end
"""
import os
import sys
import subprocess
import time
import signal
import psutil
import json


# Set up the environment for interaction
def setup_interaction():
    """
    Initialize the environment for interactive commands.

    Creates the necessary communication channels for sending input to
    and receiving output from interactive commands.

    Returns:
        None
    """
    if not os.path.exists("input_pipe"):
        os.mkfifo("input_pipe")
    if not os.path.exists("output_pipe"):
        os.mkfifo("output_pipe")
    print("AgentShell session ready.")


# Start an interactive command
def start_interactive_command(command=None):
    """
    Start an interactive command in the background.

    Launches a command that can receive input and produce output through the
    interactive session channels.

    Args:
        command (str): The command to execute. Must be specified.

    Returns:
        subprocess.Popen: A process object representing the command

    Note:
        This runs the command in the background so you can interact with it
        using the send and receive commands.
    """
    # Check if command is provided
    if command is None:
        print("Error: No command specified")
        sys.exit(1)

    # Execute the command with input/output redirection
    full_cmd = f"{command} < input_pipe > output_pipe"
    process = subprocess.Popen(full_cmd, shell=True, executable="/bin/zsh")

    # Store process info for later status checks
    process_info = {"pid": process.pid, "command": command, "started_at": time.time()}

    # Save process info to file
    with open(".agentshell_session.json", "w") as f:
        json.dump(process_info, f)

    print(f"Started interactive command (PID: {process.pid}): {command}")
    return process


# Send input to the command
def send_input(content):
    """
    Send input to the running interactive command.

    Sends a message as if you had typed it into the command's standard input.

    Args:
        content (str): The input to send to the command

    Returns:
        None

    Raises:
        Exception: If there's an error sending the input
    """
    try:
        with open("input_pipe", "w") as f:
            f.write(content + "\n")
        print(f"Sent: '{content}'")
    except Exception as e:
        print(f"Error sending input: {e}")


# Receive output from the command
def get_output():
    """
    Receive output from the interactive command.

    Gets any available output that the command has produced since the last
    receive operation, with a timeout to avoid waiting indefinitely.

    Returns:
        str: The output received from the command

    Raises:
        Exception: If there's an error receiving the output
    """
    try:
        # Set a timeout to avoid blocking indefinitely
        timeout = 3
        start_time = time.time()
        output = ""

        # Open in non-blocking mode
        fd = os.open("output_pipe", os.O_RDONLY | os.O_NONBLOCK)

        # Read until timeout
        while time.time() - start_time < timeout:
            try:
                # Try to read a chunk of data (4096 bytes at a time)
                chunk = os.read(fd, 4096)
                if chunk:
                    output += chunk.decode("utf-8")
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
            print(f"Received: '{output.strip()}'")
        else:
            print("No output available (timeout)")

        return output

    except Exception as e:
        print(f"Error receiving output: {e}")
        return ""


# Check status of the interactive session
def check_status(pid=None):
    """
    Check the status of the AgentShell session.

    Verifies that all components of the interactive session are functional:
    - The communication channels
    - The running command (if PID provided)

    Args:
        pid (int, optional): Process ID to check. If None, attempts to load from session file.

    Returns:
        dict: Status information containing:
            - Input channel status
            - Output channel status
            - Process status (if PID provided)
            - Overall status
    """
    status_info = {
        "input_channel": False,
        "output_channel": False,
        "process": False,
        "overall_status": "unhealthy",
    }

    # Check if pipes exist
    if os.path.exists("input_pipe"):
        status_info["input_channel"] = True
    if os.path.exists("output_pipe"):
        status_info["output_channel"] = True

    # Try to load process info from file if no PID specified
    process_info = None
    if pid is None and os.path.exists(".agentshell_session.json"):
        try:
            with open(".agentshell_session.json", "r") as f:
                process_info = json.load(f)
                pid = process_info.get("pid")
                status_info["command"] = process_info.get("command", "unknown")
        except:
            pass

    # Check if process is running
    if pid:
        try:
            process = psutil.Process(pid)
            if process.is_running() and process.status() != "zombie":
                status_info["process"] = True
                status_info["pid"] = pid

                # Get command line for verification
                cmdline = process.cmdline()
                status_info["process_cmdline"] = " ".join(cmdline)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    # Overall status
    if status_info["input_channel"] and status_info["output_channel"]:
        if pid is None or status_info["process"]:
            status_info["overall_status"] = "healthy"

    # Print status information
    print(f"AgentShell status:")
    print(
        f"  Input channel: {'✅ ready' if status_info['input_channel'] else '❌ not available'}"
    )
    print(
        f"  Output channel: {'✅ ready' if status_info['output_channel'] else '❌ not available'}"
    )

    if pid:
        process_status = "✅ running" if status_info["process"] else "❌ not running"
        print(f"  Command (PID {pid}): {process_status}")

        if status_info["process"]:
            if "command" in status_info:
                print(f"  Running: {status_info['command']}")
            if "process_cmdline" in status_info:
                print(f"  Command line: {status_info['process_cmdline']}")
    else:
        print("  Command: not specified")

    print(f"Overall status: {status_info['overall_status']}")

    return status_info


# End the interactive session
def end_interaction(pid=None):
    """
    End the AgentShell session and clean up resources.

    Terminates the running command (if specified) and removes
    the communication channels.

    Args:
        pid (int, optional): Process ID to terminate. If None, attempts to load from
                           session file.

    Returns:
        None
    """
    # Try to load process info if no PID specified
    if pid is None and os.path.exists(".agentshell_session.json"):
        try:
            with open(".agentshell_session.json", "r") as f:
                process_info = json.load(f)
                pid = process_info.get("pid")
        except:
            pass

    # Terminate process if PID is available
    if pid:
        try:
            process = psutil.Process(pid)
            process.terminate()
            print(f"Terminated command (PID {pid})")
        except:
            try:
                # Try harder to kill the process
                os.kill(pid, signal.SIGKILL)
                print(f"Force-terminated command (PID {pid})")
            except:
                print(f"Failed to terminate command (PID {pid})")

    # Remove process info file
    try:
        if os.path.exists(".agentshell_session.json"):
            os.unlink(".agentshell_session.json")
    except:
        pass

    # Remove communication channels
    try:
        if os.path.exists("input_pipe"):
            os.unlink("input_pipe")
        if os.path.exists("output_pipe"):
            os.unlink("output_pipe")
        print("AgentShell session ended.")
    except Exception as e:
        print(f"Error ending AgentShell session: {e}")


def main():
    """
    Parse command-line arguments and execute the requested action.

    Commands:
        setup             - Initialize the environment for interactive commands
        start [command]   - Start an interactive command in the background
        send <input>      - Send input to the running command
        receive           - Receive output from the command
        status [pid]      - Check status of the interactive session
        end [pid]         - End the interactive session and clean up

    Returns:
        None
    """
    if len(sys.argv) < 2:
        print("Usage: python AgentShell.py [setup|start|send|receive|status|end]")
        sys.exit(1)

    action = sys.argv[1]

    if action == "setup":
        setup_interaction()

    elif action == "start":
        # Get command if provided, otherwise default is used
        command = None
        if len(sys.argv) >= 3:
            command = sys.argv[2]
        start_interactive_command(command)

    elif action == "send":
        if len(sys.argv) < 3:
            print("Error: Missing input to send")
            sys.exit(1)
        send_input(sys.argv[2])

    elif action == "receive":
        get_output()

    elif action == "status":
        pid = None
        if len(sys.argv) >= 3:
            try:
                pid = int(sys.argv[2])
            except ValueError:
                print(f"Warning: Invalid PID format: {sys.argv[2]}")
        check_status(pid)

    elif action == "end":
        pid = None
        if len(sys.argv) >= 3:
            try:
                pid = int(sys.argv[2])
            except ValueError:
                print(f"Warning: Invalid PID format: {sys.argv[2]}")
        end_interaction(pid)

    else:
        print(f"Unknown action: {action}")
        print("Available actions: setup, start, send, receive, status, end")
        sys.exit(1)


"""
Implementation Details:

This tool uses named pipes (FIFOs) to create communication channels between
processes. The implementation uses:

1. Two named pipes:
   - input_pipe: For sending input to the command
   - output_pipe: For receiving output from the command

2. Process management with psutil:
   - Tracking process status
   - Clean termination of processes

3. Non-blocking I/O for reading output:
   - Prevents hanging when no output is available
   - Uses a timeout to avoid waiting indefinitely

4. Session persistence:
   - Stores process information in .agentshell_session.json
   - Allows commands to reference the running process without specifying PID
"""

if __name__ == "__main__":
    main()
