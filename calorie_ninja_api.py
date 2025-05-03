import requests
import json
import os

# File handling setup
FAVORITES_FILE = "nutrition_favorites.json"

def load_favorites():
    """Load favorites from JSON file."""
    if os.path.exists(FAVORITES_FILE):
        try:
            with open(FAVORITES_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    return []

def save_favorites(favorites):
    """Save favorites to JSON file."""
    with open(FAVORITES_FILE, 'w') as f:
        json.dump(favorites, f, indent=2)

def get_nutrition_info(api_key, query):
    """Fetch nutrition data from API."""
    api_url = 'https://api.calorieninjas.com/v1/nutrition?query='
    headers = {'X-Api-Key': api_key}

    try:
        response = requests.get(api_url + query, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    return None

def print_nutrition(data):
    """Display nutrition information."""
    if not data or 'items' not in data or len(data['items']) == 0:
        print("No nutrition information found.")
        return

    for item in data['items']:
        print(f"\nNutrition facts for: {item.get('name', 'Unknown')}")
        print(f"Calories: {item.get('calories', 'N/A')}kcal")
        print(f"Protein: {item.get('protein_g', 'N/A')}g")
        print(f"Carbs: {item.get('carbohydrates_total_g', 'N/A')}g")
        print(f"Fat: {item.get('fat_total_g', 'N/A')}g")

def manage_favorites(data):
    """Improved Favorites management system with better feedback."""
    favorites = load_favorites()
    current_items = data.get('current', {}).get('items', []) if data.get('current') else []
    
    print("\n=== Favorites Menu ===")
    print("1. Add current items to favorites")
    print("2. View saved favorites")
    print("3. Return to main menu")
    
    choice = input("Choose an option (1-3): ")
    
    if choice == '1':
        if not current_items:
            print("No current items to add. Please search for items first.")
            return
            
        added_count = 0
        for item in current_items:
            if item not in favorites:
                favorites.append(item)
                print(f"✓ Added '{item.get('name', 'Unknown')}' to favorites!")
                added_count += 1
        if added_count == 0:
            print("All items already exist in favorites!")
        save_favorites(favorites)
    
    elif choice == '2':
        if not favorites:
            print("\nNo favorites saved yet.")
        else:
            print("\n=== Saved Favorites ===")
            for idx, item in enumerate(favorites, 1):
                print(f"{idx}. {item.get('name', 'Unknown')} - {item.get('calories', 'N/A')}kcal")
    
    elif choice == '3':
        return
    else:
        print("Invalid choice. Please try again.")

def main():
    API_KEY = "+UAZGtttO6YjFV8HlrKiBg==GG6PbNeSh3rUqUqS"
    current_data = None  # Store the last fetched nutrition data
    
    # Initialize favorites file if it doesn't exist
    if not os.path.exists(FAVORITES_FILE):
        save_favorites([])
    
    while True:
        print("\n==== NUTRITION_CALORIE_CALCULATOR ====")
        print("1. Get nutrition information")
        print("2. Favorites menu")
        print("3. Exit")
        
        choice = input("Select an option (1-3): ").strip()
        
        if choice == '1':
            query = input("Enter food/drink item(s): ").strip()
            if query:
                current_data = get_nutrition_info(API_KEY, query)
                print_nutrition(current_data)
        
        elif choice == '2':
            # Pass both current data and favorites
            manage_favorites({
                'current': current_data,
                'saved': {'items': load_favorites()}
            })
        
        elif choice == '3':
            print("Thank you!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()