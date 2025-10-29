import sys

# --- Unit Conversion Data ---
# Structure: {Unit Type: {From Unit: {To Unit: Conversion Factor}}}
# Example: Convert 1 meter (Length/Meters) to centimeters (Length/Centimeters)
# Conversion Factor: 100.0 (1 meter * 100.0 = 100 centimeters)
CONVERSION_FACTORS = {
    "LENGTH": {
        "METERS": 1.0, "FEET": 3.28084, "INCHES": 39.3701, "CENTIMETERS": 100.0,
    },
    "MASS": {
        "KILOGRAMS": 1.0, "POUNDS": 2.20462, "OUNCES": 35.274, "GRAMS": 1000.0,
    },
    "TEMPERATURE": { # Simple offset-based conversion requires dedicated logic
        "CELSIUS": 1.0, "FAHRENHEIT": 1.0, "KELVIN": 1.0
    }
}

def standard_calculator(expression):
    """
    Performs standard arithmetic using Python's built-in evaluation function.
    Handles common errors gracefully.
    """
    print("\n--- Standard Calculation ---")
    try:
        # Use simple string evaluation (be cautious of external input in real apps)
        # For this internship demonstration, it showcases simple math execution.
        result = eval(expression)
        print(f"Result: {expression} = {result:.4f}")
    except (NameError, TypeError, SyntaxError):
        print("Error: Invalid mathematical expression.")
    except ZeroDivisionError:
        print("Error: Cannot divide by zero.")
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")

def convert_units(category, value, from_unit, to_unit):
    """
    Performs unit conversion based on predefined factors.
    """
    value = float(value)
    category = category.upper()
    from_unit = from_unit.upper()
    to_unit = to_unit.upper()

    if category not in CONVERSION_FACTORS:
        print(f"Error: Unknown category '{category}'.")
        return

    if category == "TEMPERATURE":
        # Temperature requires specific formulas, not just factors
        result = handle_temperature_conversion(value, from_unit, to_unit)
    else:
        # Generic factor-based conversion
        factors = CONVERSION_FACTORS[category]

        if from_unit not in factors or to_unit not in factors:
            print("Error: Invalid unit names for the selected category.")
            return

        # Convert to base unit first, then to target unit
        base_value = value / factors[from_unit]
        result = base_value * factors[to_unit]

    print(f"\nConverted Result: {value:.2f} {from_unit} = {result:.4f} {to_unit}")

def handle_temperature_conversion(value, from_unit, to_unit):
    """Handles the complex logic for temperature conversions."""
    
    # 1. Convert initial unit to Celsius (base for temperature)
    if from_unit == "FAHRENHEIT":
        celsius = (value - 32) * 5/9
    elif from_unit == "KELVIN":
        celsius = value - 273.15
    elif from_unit == "CELSIUS":
        celsius = value
    else:
        return f"Error: Unknown temperature unit {from_unit}"

    # 2. Convert Celsius to the target unit
    if to_unit == "FAHRENHEIT":
        return celsius * 9/5 + 32
    elif to_unit == "KELVIN":
        return celsius + 273.15
    elif to_unit == "CELSIUS":
        return celsius
    else:
        return f"Error: Unknown temperature unit {to_unit}"


def display_menu():
    """Prints the main menu for the calculator."""
    print("\n" + "=" * 50)
    print(" DUAL-MODE CALCULATOR & CONVERTER ")
    print("=" * 50)
    print("1: Standard Calculator (e.g., 5 * (12 + 3) / 2)")
    print("2: Unit Converter (e.g., Length, Mass, Temperature)")
    print("QUIT: Exit Application")
    print("-" * 50)


def main_app_loop():
    """The main loop managing user interaction and mode switching."""
    while True:
        display_menu()
        choice = input("Enter mode (1, 2, or QUIT): ").strip().upper()

        if choice == 'QUIT':
            print("\nExiting application. Thank you!")
            sys.exit(0)
        
        elif choice == '1':
            print("\nMODE: Standard Calculator")
            expr = input("Enter expression (e.g., 10 + 5 * 2): ").strip()
            if expr:
                standard_calculator(expr)
        
        elif choice == '2':
            print("\nMODE: Unit Converter")
            
            # List available categories
            categories = ", ".join(CONVERSION_FACTORS.keys())
            print(f"Available Categories: {categories}")
            category = input("Enter category (e.g., LENGTH): ").strip()

            if category.upper() not in CONVERSION_FACTORS:
                print("Invalid category. Returning to main menu.")
                continue

            # List available units for the chosen category
            units = ", ".join(CONVERSION_FACTORS[category.upper()].keys())
            print(f"Units for {category.upper()}: {units}")
            
            try:
                value = input("Enter value to convert: ").strip()
                float(value) # Validate input is a number early
                from_unit = input("Convert FROM unit (e.g., METERS): ").strip()
                to_unit = input("Convert TO unit (e.g., FEET): ").strip()
                
                convert_units(category, value, from_unit, to_unit)
                
            except ValueError:
                print("Invalid input for value. Please enter a number.")
            except Exception as e:
                print(f"Error: An error occurred during conversion input: {e}")

        else:
            print("Invalid choice. Please enter 1, 2, or QUIT.")

if __name__ == "__main__":
    main_app_loop()
