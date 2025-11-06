"""
Module for basic inventory management.
Allows adding, removing, checking, loading, and saving stock data.
"""
import json
import logging
from datetime import datetime

# Setup logging to report issues
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def add_item(stock_data, item="default", qty=0, logs=None):
    """
    Adds a specified quantity of an item to the inventory.

    Args:
        stock_data (dict): The inventory dictionary to modify.
        item (str): The name of the item.
        qty (int): The quantity to add. Must be a non-negative integer.
        logs (list, optional): A list to append log messages to.
    
    Raises:
        ValueError: If item is not a non-empty string or qty is not a non-negative integer.
    """
    # FIX (Issue 1): Mutable default argument
    if logs is None:
        logs = []

    # FIX (Issue 6): Missing input validation
    if not isinstance(item, str) or not item:
        raise ValueError(f"Item name must be a non-empty string, got: {item}")
    if not isinstance(qty, int):
        raise ValueError(f"Quantity must be an integer, got: {qty}")
    if qty < 0:
        raise ValueError("Quantity cannot be negative for add_item.")

    stock_data[item] = stock_data.get(item, 0) + qty

    # FIX (Issue 10): String formatting old-style
    log_message = f"{datetime.now()}: Added {qty} of {item}"
    logs.append(log_message)
    # FIX (Issue 11): Use logging
    logging.info(log_message)


def remove_item(stock_data, item, qty):
    """
    Removes a specified quantity of an item from the inventory.
    If the quantity to remove is greater than stock, the item is removed.

    Args:
        stock_data (dict): The inventory dictionary to modify.
        item (str): The name of the item.
        qty (int): The quantity to remove.
    """
    # Added validation for consistency, though not in the original table
    if not isinstance(qty, int) or qty < 0:
        logging.warning("Quantity to remove must be a positive integer.")
        return

    # FIX (Issue 2): Bare except
    try:
        current_qty = stock_data[item]
        if current_qty - qty <= 0:
            del stock_data[item]
            logging.info("Removed all stock for '%s'.", item)
        else:
            stock_data[item] -= qty
            logging.info("Removed %d of '%s'.", qty, item)
    except KeyError:
        # Catch the specific exception
        logging.warning("Attempted to remove '%s', but it is not in stock.", item)


def get_qty(stock_data, item):
    """
    Gets the current quantity of a specific item.

    Args:
        stock_data (dict): The inventory dictionary.
        item (str): The name of the item.

    Returns:
        int: The quantity of the item, or 0 if not found.
    """
    # FIX (Issue 7): May raise KeyError
    return stock_data.get(item, 0)


def load_data(file="inventory.json"):
    """
    Loads inventory data from a JSON file.

    Args:
        file (str): The path to the JSON file.

    Returns:
        dict: The loaded inventory data. Returns an empty dict if file not found or invalid.
    """
    # FIX (Issue 5): Global mutable state (now returns data)
    # FIX (Issue 4): Unsafe file handling (no 'with', no encoding)
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        logging.warning("'%s' not found. Starting with an empty inventory.", file)
        return {}
    except json.JSONDecodeError:
        logging.error("Could not decode JSON from '%s'. Starting with empty inventory.", file)
        return {}
    except IOError as e:
        logging.error("Error loading data from '%s': %s", file, e)
        return {}


def save_data(stock_data, file="inventory.json"):
    """
    Saves the inventory data to a JSON file.

    Args:
        stock_data (dict): The inventory dictionary to save.
        file (str): The path to the JSON file.
    """
    # FIX (Issue 4): Unsafe file handling (no 'with', no encoding)
    try:
        with open(file, "w", encoding="utf-8") as f:
            json.dump(stock_data, f, indent=4)
    except IOError as e:
        logging.error("Error saving data to '%s': %s", file, e)


def print_data(stock_data):
    """
    Prints a formatted report of all items and their quantities.

    Args:
        stock_data (dict): The inventory dictionary.
    """
    print("\n--- Items Report ---")
    if not stock_data:
        print("Inventory is empty.")
    else:
        for item, quantity in stock_data.items():
            print(f"{item} -> {quantity}")
    print("--------------------\n")


def check_low_items(stock_data, threshold=5):
    """
    Finds items with a quantity below a specified threshold.

    Args:
        stock_data (dict): The inventory dictionary.
        threshold (int): The stock level to check against.

    Returns:
        list: A list of item names below the threshold.
    """
    return [item for item, qty in stock_data.items() if qty < threshold]


def main():
    """Main function to run the inventory management demo."""

    # FIX (Issue 5): Load data instead of relying on global
    stock = load_data("inventory.json")
    print("Initial data loaded:")
    print_data(stock)

    try:
        # These will succeed
        add_item(stock, "apple", 10)
        add_item(stock, "banana", 20)

        # These will fail validation and be caught
        add_item(stock, "banana", -2)
    except ValueError as e:
        logging.error("Failed to add item: %s", e)

    try:
        add_item(stock, 123, "ten")
    except ValueError as e:
        logging.error("Failed to add item: %s", e)

    remove_item(stock, "apple", 3)
    remove_item(stock, "orange", 1)  # Will log a warning (not in stock)
    remove_item(stock, "banana", 25) # Will remove item entirely

    print(f"Apple stock: {get_qty(stock, 'apple')}")
    print(f"Banana stock: {get_qty(stock, 'banana')}") # Should be 0
    print(f"Orange stock: {get_qty(stock, 'orange')}") # Should be 0

    print(f"Low items (below 15): {check_low_items(stock, 15)}")

    print("Final data:")
    print_data(stock)

    save_data(stock, "inventory.json")
    print("Data saved.")

    # FIX (Issue 3): Use of eval (removed)
    logging.info("Demo finished. 'eval' call was removed.")


# Standard practice to run main
if __name__ == "__main__":
    # FIX (Issue 8 & 12): Function names are all snake_case,
    # and functions are separated by two blank lines.
    main()
