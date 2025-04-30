import requests

def get_nutrition_info(api_key, query):
    api_url = 'https://api.calorieninjas.com/v1/nutrition?query='
    headers = {'X-Api-Key': api_key}

    try:
        response = requests.get(api_url + query, headers=headers)
        response.raise_for_status() 
        data = response.json()
        return data
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} - {response.text}")
    except Exception as err:
        print(f"An error occurred: {err}")
    return None

def print_nutrition(data):
    """
    Nicely print nutrition information from API response.

    Parameters:
    - data (dict): JSON data returned from the API.
    """
    if not data or 'items' not in data or len(data['items']) == 0:
        print("No nutrition information found for the given query.")
        return

    for item in data['items']:
        print(f"\nNutrition facts for: {item.get('name', 'Unknown')}")
        print(f"Serving Size: {item.get('serving_size_g', 'N/A')} g")
        print(f"Calories: {item.get('calories', 'N/A')}")
        print(f"Total Fat: {item.get('fat_total_g', 'N/A')} g")
        print(f"Saturated Fat: {item.get('fat_saturated_g', 'N/A')} g")
        print(f"Cholesterol: {item.get('cholesterol_mg', 'N/A')} mg")
        print(f"Sodium: {item.get('sodium_mg', 'N/A')} mg")
        print(f"Total Carbohydrates: {item.get('carbohydrates_total_g', 'N/A')} g")
        print(f"Fiber: {item.get('fiber_g', 'N/A')} g")
        print(f"Sugar: {item.get('sugar_g', 'N/A')} g")
        print(f"Protein: {item.get('protein_g', 'N/A')} g")
        print(f"Potassium: {item.get('potassium_mg', 'N/A')} mg")

if __name__ == "__main__":
    API_KEY = "+UAZGtttO6YjFV8HlrKiBg==GG6PbNeSh3rUqUqS"

    food_query = input("Enter the food or drink item(s) to query nutrition info for: ").strip()

    nutrition_data = get_nutrition_info(API_KEY, food_query)
    print_nutrition(nutrition_data)
