# ============================================================
# Simple Calculator — Session 1.1
# Concepts used: input(), float(), if/elif/else, while, def
# ============================================================


def calculate(a, b, operation):
    """
    Takes two numbers and an operation symbol.
    Returns the result, or an error message string.
    """
    if operation == "+":
        return a + b
    elif operation == "-":
        return a - b
    elif operation == "*":
        return a * b
    elif operation == "/":
        if b == 0:
            return "Error: can't divide by zero"
        return a / b
    else:
        return "Error: unknown operation"


# ------------------------------------------------------------
# Main program loop — keeps running until user types 'q'
# ------------------------------------------------------------
print("=== Simple Calculator ===")
print("Operations: +  -  *  /")
print("Type 'q' at any prompt to quit.")
print()

while True:                          # loop forever until we break out

    # --- Get first number ---
    first_input = input("Enter first number: ")
    if first_input.lower() == "q":  # .lower() makes 'Q' work too
        break                        # exit the while loop

    # --- Get second number ---
    second_input = input("Enter second number: ")
    if second_input.lower() == "q":
        break

    # --- Get operation ---
    op = input("Operation (+ - * /): ")
    if op.lower() == "q":
        break

    # --- Convert text to numbers ---
    # input() always gives us a string — float() turns "3.5" into 3.5
    num1 = float(first_input)
    num2 = float(second_input)

    # --- Calculate and display ---
    result = calculate(num1, num2, op)
    print(f"  Result: {num1} {op} {num2} = {result}")
    print()   # blank line for readability

print("Goodbye!")
