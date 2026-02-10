import re
from app.operations.operations import operations

OPERATIONS = {
    '+': operations.add,
    '-': operations.subtract,
    '*': operations.multiply,
    '/': operations.divide,
}

HELP_TEXT = \
"""
Calculator REPL
---------------
Usage:
  <num> <op> <num>      Start a new expression e.g. 1 + 2
  <op> <num>            Continue from last result e.g. + 5
  =                     Show current result
  c / clear             Clear and start over
  h / help              Show this help
  q / quit              Exit
"""

def parse_number(s: str) -> float:
    try:
        return float(s.replace(' ', ''))
    except ValueError:
        raise ValueError(f"Error: Not a valid number: '{s}'")

def calculator():
    result = None
    print(HELP_TEXT)

    while True:
        prompt = f"[{str(int(result) if result.is_integer() else result)}] > " if result is not None else "> "
        try:
            raw = input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting")
            break

        if not raw:
            continue

        cmd = raw.lower()

        # Quit
        if cmd in ('q', 'quit'):
            print("Exiting")
            break

        # Help
        if cmd in ('h', 'help'):
            print(HELP_TEXT)
            continue
        
        # Clear results
        if cmd in ('c', 'clear'):
            result = None
            print("Cleared.")
            continue

        # Get current running total
        if cmd == '=':
            if result is None:
                print("No result yet.")
            else:
                print(f"= {str(int(result) if result.is_integer() else result)}")
            continue
        
        # Regex to check valid expression
        match = re.fullmatch(
            r'([+-]?\s*\d+(?:\.\d+)?)\s*([+\-*/])\s*([+-]?\s*\d+(?:\.\d+)?)'
            r'|([+\-*/])\s*([+-]?\s*\d+(?:\.\d+)?)',
            raw
        )

        if not match:
            print("Error: Unrecognized input. Type 'h' for help.")
            continue

        try:
            # If full expression
            if match.group(1) is not None:
                a = parse_number(match.group(1))
                op = match.group(2)
                b = parse_number(match.group(3))
                result = OPERATIONS[op](a, b)
            # Else continuation from last result
            else:
                if result is None:
                    print("Error: No previous result. Start with a full expression, e.g. '1 + 2'.")
                    continue
                op = match.group(4)
                b = parse_number(match.group(5))
                result = OPERATIONS[op](result, b)

            # Print result. Remove extra zeroes if integer
            print(str(int(result) if result.is_integer() else result))

        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")