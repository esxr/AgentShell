#!/usr/bin/env python3
"""
Echo Tool - A simple tool that reads from stdin and transforms the input.

This script is an example for use with AgentShell.py. It reads lines from standard input,
applies transformations based on commands, and writes the results to standard output.

Commands:
- upper: Convert text to uppercase
- lower: Convert text to lowercase
- reverse: Reverse the text
- count: Count the number of characters
- quit/exit: Exit the program

If no command is specified, it simply echoes the input back.

License: MIT - Use freely for any purpose
"""
import sys


def main():
    print("Echo Tool (Ctrl+C to exit)")
    print("Commands: upper, lower, reverse, count, quit/exit")

    try:
        while True:
            line = input("> ")
            line = line.strip()

            if not line:
                continue

            if line.lower() in ("quit", "exit", "q"):
                print("Goodbye!")
                break

            parts = line.split(" ", 1)
            command = parts[0].lower()

            if len(parts) > 1:
                text = parts[1]
            else:
                text = ""

            if command == "upper":
                print(text.upper())
            elif command == "lower":
                print(text.lower())
            elif command == "reverse":
                print(text[::-1])
            elif command == "count":
                print(f"Character count: {len(text)}")
            else:
                # If no valid command, treat the whole line as text to echo
                print(line)

    except KeyboardInterrupt:
        print("\nGoodbye!")
    except EOFError:
        print("\nInput ended. Goodbye!")


if __name__ == "__main__":
    main()
