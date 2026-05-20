import math

def add(a, b):
    """Returns the sum of a and b."""
    return a + b

def subtract(a, b):
    """Returns the difference of a and b."""
    return a - b

def multiply(a, b):
    """Returns the product of a and b."""
    return a * b

def divide(a, b):
    """Returns the quotient of a and b. Raises ValueError on division by zero."""
    if b == 0:
        raise ValueError("Error: Division by zero is not allowed.")
    return a / b

def power(a, b):
    """Returns a raised to the power of b."""
    return a ** b

def modulo(a, b):
    """Returns the remainder of a divided by b. Raises ValueError on modulo by zero."""
    if b == 0:
        raise ValueError("Error: Modulo by zero is not allowed.")
    return a % b

def square_root(a):
    """Returns the square root of a. Raises ValueError on negative inputs."""
    if a < 0:
        raise ValueError("Error: Cannot calculate the square root of a negative number in real numbers.")
    return math.sqrt(a)

def get_number(prompt):
    """Safely prompts the user for a floating point number."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def main():
    print("=" * 40)
    print("         COMPLEX CALCULATOR CLI")
    print("=" * 40)
    
    while True:
        print("\nAvailable Operations:")
        print("1. Addition (+)")
        print("2. Subtraction (-)")
        print("3. Multiplication (*)")
        print("4. Division (/)")
        print("5. Exponentiation (^)")
        print("6. Modulo (%)")
        print("7. Square Root (√)")
        print("8. Exit")
        
        choice = input("\nSelect operation (1-8): ").strip()
        
        if choice == '8':
            print("\nThank you for using the Complex Calculator. Goodbye!")
            break
            
        if choice in ['1', '2', '3', '4', '5', '6']:
            num1 = get_number("Enter the first number: ")
            num2 = get_number("Enter the second number: ")
            
            try:
                if choice == '1':
                    result = add(num1, num2)
                    print(f"\nResult: {num1} + {num2} = {result}")
                elif choice == '2':
                    result = subtract(num1, num2)
                    print(f"\nResult: {num1} - {num2} = {result}")
                elif choice == '3':
                    result = multiply(num1, num2)
                    print(f"\nResult: {num1} * {num2} = {result}")
                elif choice == '4':
                    result = divide(num1, num2)
                    print(f"\nResult: {num1} / {num2} = {result}")
                elif choice == '5':
                    result = power(num1, num2)
                    print(f"\nResult: {num1} ^ {num2} = {result}")
                elif choice == '6':
                    result = modulo(num1, num2)
                    print(f"\nResult: {num1} % {num2} = {result}")
            except ValueError as e:
                print(f"\n{e}")
                
        elif choice == '7':
            num = get_number("Enter the number: ")
            try:
                result = square_root(num)
                print(f"\nResult: √{num} = {result}")
            except ValueError as e:
                print(f"\n{e}")
        else:
            print("\nInvalid choice. Please select an option between 1 and 8.")
            
        print("-" * 40)

if __name__ == '__main__':
    # Simple non-interactive demonstration run
    print("Demo calculation: 2 + 3 =", add(2, 3))
    print("Demo calculation: 5 ^ 3 =", power(5, 3))
    print("=" * 40)
    
    # Run the interactive menu
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCalculator interrupted. Goodbye!")
