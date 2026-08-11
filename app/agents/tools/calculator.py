def calculate(
    operation: str,
    a: float,
    b: float,
) -> str:
    operations = {
        "add": lambda: a + b,
        "subtract": lambda: a - b,
        "multiply": lambda: a * b,
        "divide": lambda: a / b,
    }

    if operation not in operations:
        return f"Unsupported operation: {operation}"

    if operation == "divide" and b == 0:
        return "Cannot divide by zero."

    result = operations[operation]()

    return str(result)
