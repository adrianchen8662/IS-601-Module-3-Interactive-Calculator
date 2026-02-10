class operations:
    # Addition operation
    def add(a, b):
        return a + b

    # Subtraction operation
    def subtract(a, b):
        return a - b

    # Multiplication operation
    def multiply(a, b):
        return a * b

    # Division operation
    def divide(a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b