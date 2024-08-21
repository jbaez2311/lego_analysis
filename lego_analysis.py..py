import os


def read_lego_data(filename, line_limit=1000):
    """
    Reads the first 'line_limit' lines of a LEGO data CSV file and populates price and difficulty dictionaries.

    Args:
    - filename (str): Path to the CSV file.
    - line_limit (int): Number of lines to read from the file.

    Returns:
    - price_dict (dict): Dictionary with product IDs as keys and prices as values.
    - difficulty_dict (dict): Dictionary with product IDs as keys and review difficulties as values.
    """
    price_dict = {}
    difficulty_dict = {}
    lines_read = 0

    if not os.path.exists(filename):
        print(f"Error: The file {filename} does not exist.")
        return price_dict, difficulty_dict

    try:
        with open(filename, 'r') as file:
            next(file)  # Skip the header row
            for line in file:
                if lines_read >= line_limit:
                    break

                tokens = line.strip().split(',')
                if len(tokens) < 6:  # Check if the line has enough columns
                    print(f"Warning: Skipping malformed line: {line.strip()}")
                    continue

                product_id = tokens[4]  # prod_id
                price = tokens[0]  # list_price
                difficulty = tokens[5]  # review_difficulty

                # Populate the dictionaries
                price_dict[product_id] = price
                difficulty_dict[product_id] = difficulty

                lines_read += 1
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")

    return price_dict, difficulty_dict


def analyze_data(price_dict, difficulty_dict):
    """
    Performs basic analysis on the LEGO data and prints summary statistics.

    Args:
    - price_dict (dict): Dictionary with product IDs as keys and prices as values.
    - difficulty_dict (dict): Dictionary with product IDs as keys and review difficulties as values.
    """
    # Convert prices to floats for analysis
    prices_by_difficulty = {}

    for product_id, price in price_dict.items():
        difficulty = difficulty_dict.get(product_id, "Unknown")
        try:
            price = float(price)
        except ValueError:
            print(f"Warning: Invalid price '{price}' for product ID {product_id}. Skipping.")
            continue

        if difficulty not in prices_by_difficulty:
            prices_by_difficulty[difficulty] = []

        prices_by_difficulty[difficulty].append(price)

    # Print summary statistics
    print("\nSummary of Prices by Difficulty Level:")
    for difficulty, prices in prices_by_difficulty.items():
        avg_price = sum(prices) / len(prices)
        print(f"- {difficulty}: {len(prices)} sets, Average Price: ${avg_price:.2f}")


def main():
    # Path to the CSV file
    filename = './lego_setsHB.csv'

    # Read the LEGO data
    price_dict, difficulty_dict = read_lego_data(filename, line_limit=1000)

    # Print some sample data
    print("Sample Data (Product ID, Price, Difficulty):")
    for key, value in list(price_dict.items())[:10]:
        print(key, value, difficulty_dict[key])

    # Analyze the data
    analyze_data(price_dict, difficulty_dict)


if __name__ == "__main__":
    main()