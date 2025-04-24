#!/usr/bin/env python3
"""
Calculator Tool - An interactive command-line calculator.

This script is an example for use with AgentShell.py. It reads expressions from standard input,
evaluates them, and writes the results to standard output.

Version 4: Numerical + Algebraic + Trigonometric + Equation Solving
- add: Add two numbers (e.g., add 5 3)
- subtract: Subtract second number from first (e.g., subtract 10 4)
- multiply: Multiply two numbers (e.g., multiply 6 7)
- divide: Divide first number by second (e.g., divide 20 5)
- eval: Evaluate algebraic expressions (e.g., eval 2*(3+4))
- sin: Calculate sine in radians (e.g., sin 0.5)
- cos: Calculate cosine in radians (e.g., cos 1)
- tan: Calculate tangent in radians (e.g., tan 0.75)
- deg: Convert degrees to radians (e.g., deg 90)
- solve: Solve algebraic equations (e.g., solve x+5=10 or solve 2*x-3=7)
- quit/exit: Exit the program

License: MIT - Use freely for any purpose
"""
import sys
import re
import math
import sympy


def evaluate_expression(expression):
    """Safely evaluate a mathematical expression."""
    # Clean the expression to ensure it only contains valid characters
    clean_expr = re.sub(r'[^0-9+\-*/().% ]', '', expression)
    
    try:
        # Use eval with restricted globals for safety
        result = eval(clean_expr, {"__builtins__": {}})
        return result
    except Exception as e:
        return f"Error: {str(e)}"


def calculate_trig(func, value):
    """Calculate trigonometric function."""
    try:
        if func == "sin":
            return math.sin(value)
        elif func == "cos":
            return math.cos(value)
        elif func == "tan":
            return math.tan(value)
        else:
            return f"Error: Unknown trigonometric function: {func}"
    except Exception as e:
        return f"Error: {str(e)}"


def solve_equation(equation):
    """Solve an algebraic equation using sympy."""
    try:
        # Split the equation into left and right sides
        if "=" not in equation:
            return "Error: Equation must contain an equals sign (=)"
        
        left_side, right_side = equation.split("=", 1)
        
        # Convert to sympy expression
        x = sympy.Symbol('x')
        
        # Replace common alternative notation
        equation_normalized = equation.replace("^", "**")
        left_side, right_side = equation_normalized.split("=", 1)
        
        # Parse the expressions
        left_expr = sympy.sympify(left_side)
        right_expr = sympy.sympify(right_side)
        
        # Move everything to one side: left_expr - right_expr = 0
        equation_expr = left_expr - right_expr
        
        # Solve the equation
        solutions = sympy.solve(equation_expr, x)
        
        if not solutions:
            return "No solutions found"
        elif len(solutions) == 1:
            return f"x = {solutions[0]}"
        else:
            result = "Solutions:\n"
            for i, sol in enumerate(solutions, 1):
                result += f"x{i} = {sol}\n"
            return result.strip()
            
    except Exception as e:
        return f"Error solving equation: {str(e)}"


def main():
    print("Calculator Tool v4.0 - Numerical + Algebraic + Trigonometric + Equation Solving")
    print("Commands: add, subtract, multiply, divide, eval, sin, cos, tan, deg, solve, quit/exit")
    print("Examples: add 5 3, eval 2*(3+4), sin 0.5, solve x+5=10")

    try:
        while True:
            try:
                line = input("> ")
                line = line.strip()

                if not line:
                    continue

                if line.lower() in ("quit", "exit", "q"):
                    print("Goodbye!")
                    break

                parts = line.split(maxsplit=1)
                command = parts[0].lower()
                
                # Equation solving
                if command == "solve" and len(parts) > 1:
                    equation = parts[1]
                    result = solve_equation(equation)
                    print(f"{result}")
                    continue
                
                # Trigonometric functions
                if command in ["sin", "cos", "tan"] and len(parts) > 1:
                    try:
                        value = float(parts[1])
                        result = calculate_trig(command, value)
                        print(f"Result: {result}")
                        continue
                    except ValueError:
                        print("Error: Please provide a valid number")
                        continue
                
                # Degree to radian conversion
                if command == "deg" and len(parts) > 1:
                    try:
                        degrees = float(parts[1])
                        radians = math.radians(degrees)
                        print(f"Result: {radians} radians")
                        continue
                    except ValueError:
                        print("Error: Please provide a valid number")
                        continue
                
                # Expression evaluation
                if command == "eval" and len(parts) > 1:
                    expression = parts[1]
                    result = evaluate_expression(expression)
                    print(f"Result: {result}")
                    continue
                
                try:
                    if len(parts) < 2:
                        print("Error: Not enough arguments")
                        continue
                        
                    if command in ["add", "subtract", "multiply", "divide"]:
                        num_parts = parts[1].split()
                        if len(num_parts) < 2:
                            print("Error: Not enough numbers provided")
                            continue
                            
                        num1 = float(num_parts[0])
                        num2 = float(num_parts[1])
                        
                        if command == "add":
                            print(f"Result: {num1 + num2}")
                        elif command == "subtract":
                            print(f"Result: {num1 - num2}")
                        elif command == "multiply":
                            print(f"Result: {num1 * num2}")
                        elif command == "divide":
                            if num2 == 0:
                                print("Error: Cannot divide by zero")
                            else:
                                print(f"Result: {num1 / num2}")
                    else:
                        print(f"Unknown command: {command}")
                        
                except ValueError:
                    print("Error: Please provide valid numbers")
                except IndexError:
                    print("Error: Not enough arguments provided")
                except Exception as e:
                    print(f"Error: {str(e)}")
                    
            except EOFError:
                # This should only happen when AgentShell.py ends the process
                print("\nInput ended. Goodbye!")
                break

    except KeyboardInterrupt:
        print("\nGoodbye!")


if __name__ == "__main__":
    main() 