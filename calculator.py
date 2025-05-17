import numpy as np

def calculate_nutrients(food_entries):
    """
    Calculate the total nutritional values from a list of food entries
    
    Args:
        food_entries (list): List of dictionaries containing food nutrition information
        
    Returns:
        dict: Total nutritional values
    """
    if not food_entries:
        return {
            "calories": 0.0,
            "protein": 0.0,
            "carbs": 0.0,
            "fat": 0.0
        }
    
    # Initialize totals
    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fat = 0
    
    # Sum up all nutrients from food entries
    for entry in food_entries:
        total_calories += entry.get("calories", 0)
        total_protein += entry.get("protein", 0)
        total_carbs += entry.get("carbs", 0)
        total_fat += entry.get("fat", 0)
    
    return {
        "calories": total_calories,
        "protein": total_protein,
        "carbs": total_carbs,
        "fat": total_fat
    }

def calculate_percent_daily_values(totals, reference_values=None):
    """
    Calculate percent daily values based on reference values
    
    Args:
        totals (dict): Dictionary containing total nutritional values
        reference_values (dict, optional): Reference daily intake values
        
    Returns:
        dict: Percent daily values
    """
    # Default reference values based on a 2000 calorie diet
    if reference_values is None:
        reference_values = {
            "calories": 2000,
            "protein": 50,  # g
            "carbs": 275,   # g
            "fat": 78       # g
        }
    
    percent_values = {}
    
    for nutrient, total in totals.items():
        if nutrient in reference_values and reference_values[nutrient] > 0:
            percent_values[nutrient] = (total / reference_values[nutrient]) * 100
        else:
            percent_values[nutrient] = 0
    
    return percent_values

def calculate_macronutrient_ratio(totals):
    """
    Calculate the macronutrient ratio (protein:carbs:fat) based on calories
    
    Args:
        totals (dict): Dictionary containing total nutritional values
        
    Returns:
        dict: Macronutrient ratios as percentages
    """
    # Calculate calories from each macronutrient
    protein_calories = totals["protein"] * 4  # 4 calories per gram of protein
    carb_calories = totals["carbs"] * 4       # 4 calories per gram of carbs
    fat_calories = totals["fat"] * 9          # 9 calories per gram of fat
    
    total_macro_calories = protein_calories + carb_calories + fat_calories
    
    # Avoid division by zero
    if total_macro_calories == 0:
        return {
            "protein_percent": 0,
            "carb_percent": 0,
            "fat_percent": 0
        }
    
    # Calculate percentages
    protein_percent = (protein_calories / total_macro_calories) * 100
    carb_percent = (carb_calories / total_macro_calories) * 100
    fat_percent = (fat_calories / total_macro_calories) * 100
    
    return {
        "protein_percent": protein_percent,
        "carb_percent": carb_percent,
        "fat_percent": fat_percent
    }

def calculate_points(nutrition_data):
    """
    Calculate point value based on macronutrients where:
    - 1 point = 7g protein
    - 1 point = 1.5g fat
    - 1 point = 9g carb
    
    Args:
        nutrition_data (dict): Dictionary containing nutritional values
        
    Returns:
        float: Total point value
    """
    # Extract macronutrients
    protein = nutrition_data.get("protein", 0)
    fat = nutrition_data.get("fat", 0)
    carbs = nutrition_data.get("carbs", 0)
    
    # Calculate points for each macronutrient
    protein_points = protein / 7
    fat_points = fat / 1.5
    carb_points = carbs / 9
    
    # Return the sum of all points, rounded to 1 decimal place
    total_points = round(protein_points + fat_points + carb_points, 1)
    
    return total_points
