"""
Input validation utilities for nutrition targets
"""

def validate_custom_targets(calories, protein, carbs, fat):
    """
    Validate user input for custom nutritional targets
    
    Args:
        calories (float): Target daily calories
        protein (float): Target daily protein in grams
        carbs (float): Target daily carbohydrates in grams
        fat (float): Target daily fat in grams
    
    Returns:
        tuple: (is_valid, error_message)
    """
    
    # Calculate minimum calories from macros
    # Protein: 4 cal/g, Carbs: 4 cal/g, Fat: 9 cal/g
    min_calories_from_macros = (protein * 4) + (carbs * 4) + (fat * 9)
    
    # Check if calories are reasonable
    if calories < 500:
        return False, (
            "\n⚠️  WARNING: Calorie target is very low (< 500 kcal)\n"
            "    Minimum recommended: 1200-1500 kcal for most people\n"
            "    Please enter a higher calorie target."
        )
    
    # Check if macros match calories (with 20% tolerance)
    if min_calories_from_macros > calories * 1.2:
        return False, (
            f"\n⚠️  ERROR: Macronutrients don't match calorie target!\n"
            f"    Your macros require ~{min_calories_from_macros:.0f} kcal\n"
            f"    But you entered {calories:.0f} kcal\n"
            f"\n    Tip: Use option 1 (BMI calculator) for balanced targets"
        )
    
    # Check if macros are too far below calories
    if min_calories_from_macros < calories * 0.7:
        return False, (
            f"\n⚠️  WARNING: Macronutrients are too low for calorie target\n"
            f"    Your macros only provide ~{min_calories_from_macros:.0f} kcal\n"
            f"    But you entered {calories:.0f} kcal target\n"
            f"\n    Please adjust your macro targets to match calories"
        )
    
    # Check if any macro is too low
    if protein < 30:
        return False, (
            f"\n⚠️  WARNING: Protein is too low ({protein}g)\n"
            f"    Minimum recommended: 30g\n"
            f"    Please enter a higher protein target."
        )
    
    if carbs < 50:
        return False, (
            f"\n⚠️  WARNING: Carbs are too low ({carbs}g)\n"
            f"    Minimum recommended: 50g\n"
            f"    Please enter a higher carb target."
        )
    
    if fat < 20:
        return False, (
            f"\n⚠️  WARNING: Fat is too low ({fat}g)\n"
            f"    Minimum recommended: 20g\n"
            f"    Please enter a higher fat target."
        )
    
    # Check if any macro is unreasonably high
    if protein > 400:
        return False, f"\n⚠️  WARNING: Protein is very high ({protein}g). Maximum recommended: 400g"
    
    if carbs > 600:
        return False, f"\n⚠️  WARNING: Carbs are very high ({carbs}g). Maximum recommended: 600g"
    
    if fat > 200:
        return False, f"\n⚠️  WARNING: Fat is very high ({fat}g). Maximum recommended: 200g"
    
    if calories > 5000:
        return False, f"\n⚠️  WARNING: Calories are very high ({calories}). Maximum recommended: 5000 kcal"
    
    return True, None


def validate_bmi_inputs(weight, height, age):
    """
    Validate BMI calculator inputs
    
    Args:
        weight (float): Weight in kg
        height (float): Height in cm
        age (int): Age in years
    
    Returns:
        tuple: (is_valid, error_message)
    """
    
    if weight < 30 or weight > 300:
        return False, "\n⚠️  ERROR: Weight must be between 30-300 kg"
    
    if height < 100 or height > 250:
        return False, "\n⚠️  ERROR: Height must be between 100-250 cm"
    
    if age < 15 or age > 100:
        return False, "\n⚠️  ERROR: Age must be between 15-100 years"
    
    return True, None