""" tests/test_calculator.py """
import sys
from io import StringIO
from app.calculator import calculator

# NOTE: This function was taken from https://github.com/kaw393939/module3_is601/blob/main/tests/test_calculator.py
def run_calculator_with_input(monkeypatch, inputs):
    """
    Simulates user input and captures output from the calculator REPL.

    :param monkeypatch: pytest fixture to simulate user input
    :param inputs: list of inputs to simulate
    :return: captured output as a string
    """
    input_iterator = iter(inputs)
    monkeypatch.setattr('builtins.input', lambda _: next(input_iterator))
    captured_output = StringIO()
    sys.stdout = captured_output
    calculator()
    sys.stdout = sys.__stdout__
    return captured_output.getvalue()


# --- Basic operations ---

def test_addition(monkeypatch):
    """Test addition full expression."""
    output = run_calculator_with_input(monkeypatch, ["1 + 2", "q"])
    assert "3" in output

def test_subtraction(monkeypatch):
    """Test subtraction full expression."""
    output = run_calculator_with_input(monkeypatch, ["10 - 4", "q"])
    assert "6" in output

def test_multiplication(monkeypatch):
    """Test multiplication full expression."""
    output = run_calculator_with_input(monkeypatch, ["4 * 5", "q"])
    assert "20" in output

def test_division(monkeypatch):
    """Test division full expression."""
    output = run_calculator_with_input(monkeypatch, ["10 / 2", "q"])
    assert "5" in output

def test_float_result(monkeypatch):
    """Test that non-integer results are shown as floats."""
    output = run_calculator_with_input(monkeypatch, ["1 / 3", "q"])
    assert "." in output  # e.g. 0.3333...


# --- Continuation ---

def test_continuation(monkeypatch):
    """Test continuing from a previous result."""
    output = run_calculator_with_input(monkeypatch, ["1 + 2", "+ 5", "q"])
    assert "3" in output
    assert "8" in output

def test_continuation_no_previous_result(monkeypatch):
    """Test continuation with no prior result gives an error."""
    output = run_calculator_with_input(monkeypatch, ["+ 5", "q"])
    assert "Error: No previous result" in output


# --- = command ---

def test_equals_with_result(monkeypatch):
    """Test = shows the current result."""
    output = run_calculator_with_input(monkeypatch, ["3 + 3", "=", "q"])
    assert output.count("6") >= 2  # once from expression, once from =

def test_equals_no_result(monkeypatch):
    """Test = with no result yet."""
    output = run_calculator_with_input(monkeypatch, ["=", "q"])
    assert "No result yet." in output


# --- clear ---

def test_clear(monkeypatch):
    """Test clear resets the result."""
    output = run_calculator_with_input(monkeypatch, ["3 + 3", "c", "=", "q"])
    assert "Cleared." in output
    assert "No result yet." in output

def test_clear_alias(monkeypatch):
    """Test 'clear' alias works the same as 'c'."""
    output = run_calculator_with_input(monkeypatch, ["3 + 3", "clear", "=", "q"])
    assert "Cleared." in output


# --- help ---

def test_help(monkeypatch):
    """Test h prints help text."""
    output = run_calculator_with_input(monkeypatch, ["h", "q"])
    assert "Calculator REPL" in output

def test_help_alias(monkeypatch):
    """Test 'help' alias prints help text."""
    output = run_calculator_with_input(monkeypatch, ["help", "q"])
    assert "Calculator REPL" in output


# --- quit ---

def test_quit(monkeypatch):
    """Test q exits with message."""
    output = run_calculator_with_input(monkeypatch, ["q"])
    assert "Exiting" in output

def test_quit_alias(monkeypatch):
    """Test 'quit' alias exits."""
    output = run_calculator_with_input(monkeypatch, ["quit"])
    assert "Exiting" in output


# --- Empty input ---

def test_empty_input(monkeypatch):
    """Test that empty input is ignored and loop continues."""
    output = run_calculator_with_input(monkeypatch, ["", "q"])
    assert "Exiting" in output


# --- Error cases ---

def test_unrecognized_input(monkeypatch):
    """Test that unrecognized input prints an error."""
    output = run_calculator_with_input(monkeypatch, ["hello world", "q"])
    assert "Error: Unrecognized input" in output

def test_division_by_zero(monkeypatch):
    """Test division by zero prints an error."""
    output = run_calculator_with_input(monkeypatch, ["5 / 0", "q"])
    assert "Error:" in output

def test_invalid_number_in_expression():
    """Test that a non-numeric value in parse_number raises ValueError."""
    import pytest
    from app.calculator import parse_number
    with pytest.raises(ValueError, match="Not a valid number"):
        parse_number("abc")


# --- EOFError / KeyboardInterrupt ---

def test_eoferror_exits(monkeypatch):
    """Test that EOFError exits gracefully."""
    monkeypatch.setattr('builtins.input', lambda _: (_ for _ in ()).throw(EOFError))
    captured_output = StringIO()
    sys.stdout = captured_output
    calculator()
    sys.stdout = sys.__stdout__
    assert "Exiting" in captured_output.getvalue()

def test_keyboardinterrupt_exits(monkeypatch):
    """Test that KeyboardInterrupt exits gracefully."""
    monkeypatch.setattr('builtins.input', lambda _: (_ for _ in ()).throw(KeyboardInterrupt))
    captured_output = StringIO()
    sys.stdout = captured_output
    calculator()
    sys.stdout = sys.__stdout__
    assert "Exiting" in captured_output.getvalue()