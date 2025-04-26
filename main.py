import requests

API_KEY = ''  
API_URL = 'https://api.calorieninjas.com/v1/nutrition?query='

def get_calories_from_api(food_item):
    """Get calorie info from CalorieNinjas API"""
    headers = {'X-Api-Key': API_KEY}
    response = requests.get(API_URL + food_item, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if data['items']:
            return data['items'][0]['calories']  # Return calories of first item found
        else:
            print(f"No data found for '{food_item}'.")
            return 0
    else:
        print(f"Error fetching data: {response.status_code}")
        return 0

def calculate_total_calories(meal_items):
    """Calculate total calories from API data."""
    total_calories = 0
    for item in meal_items:
        item = item.strip()
        calories = get_calories_from_api(item)
        print(f"{item.title()}: {calories} kcal")
        total_calories += calories
    return total_calories

def main():
    print("Welcome to the Nutrition & Calorie Calculator (Live Data Version)!")
    meal = input("Enter your meal items separated by commas (e.g., apple, rice, chicken breast (100g)): ")
    meal_items = [i.strip() for i in meal.split(',')]

    total = calculate_total_calories(meal_items)
    print(f"\nTotal calories for your meal: {total} kcal")

if _name_ == "_main_":
    main()

