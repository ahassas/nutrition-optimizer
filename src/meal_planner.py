import pandas as pd
from typing import Dict, List
from optimizer import NutritionOptimizer

class MealPlanner:
    """
    Distributes daily nutrition across meals (breakfast, lunch, dinner)
    with meal-appropriate food selection
    """
    
    def __init__(self, foods_df: pd.DataFrame):
        self.foods_df = foods_df
        self.optimizer = NutritionOptimizer(foods_df)
    
    def filter_foods_by_meal(self, meal_name: str) -> pd.DataFrame:
        """
        Filter foods appropriate for specific meal
        
        Args:
            meal_name: 'breakfast', 'lunch', or 'dinner'
            
        Returns:
            Filtered DataFrame
        """
        if meal_name == 'breakfast':
            # Only breakfast and 'all' foods
            mask = (self.foods_df['meal_type'] == 'breakfast') | \
                   (self.foods_df['meal_type'] == 'all')
        else:
            # For lunch/dinner: lunch_dinner and 'all' foods
            mask = (self.foods_df['meal_type'] == 'lunch_dinner') | \
                   (self.foods_df['meal_type'] == 'all')
        
        return self.foods_df[mask].copy()
    
    def create_daily_plan(self,
                         daily_calories: float,
                         daily_protein: float,
                         daily_carbs: float,
                         daily_fat: float,
                         meal_distribution: Dict[str, float] = None) -> Dict:
        """
        Creates meal plan for entire day with meal-appropriate foods
        
        Args:
            daily_*: Total daily targets
            meal_distribution: Percentage per meal
        """
        
        if meal_distribution is None:
            meal_distribution = {
                'breakfast': 0.25,
                'lunch': 0.40,
                'dinner': 0.35
            }
        
        daily_plan = {}
        
        for meal_name, percentage in meal_distribution.items():
            print(f"\nOptimizing {meal_name}...")
            
            # Filter foods appropriate for this meal
            meal_foods = self.filter_foods_by_meal(meal_name)
            
            print(f"Available foods: {len(meal_foods)}")
            
            # Create optimizer with filtered foods
            meal_optimizer = NutritionOptimizer(meal_foods)
            
            result = meal_optimizer.optimize(
                target_calories=daily_calories * percentage,
                target_protein=daily_protein * percentage,
                target_carbs=daily_carbs * percentage,
                target_fat=daily_fat * percentage,
                tolerance=0.15
            )
            
            if result['status'] == 'optimal':
                daily_plan[meal_name] = result
            else:
                daily_plan[meal_name] = {
                    'status': 'failed',
                    'message': f'Could not optimize {meal_name}'
                }
        
        return daily_plan
    
    def print_daily_plan(self, plan: Dict):
        """Pretty print the daily meal plan"""
        print("\n" + "="*60)
        print("DAILY MEAL PLAN")
        print("="*60)
        
        grand_total = {
            'calories': 0,
            'protein': 0,
            'carbs': 0,
            'fat': 0
        }
        
        for meal_name, meal_data in plan.items():
            print(f"\n{meal_name.upper()}:")
            print("-" * 60)
            
            if meal_data['status'] == 'optimal':
                for food in meal_data['foods']:
                    # Get display unit from database
                    food_info = self.foods_df[
                        self.foods_df['food_id'] == food['food_id']
                    ].iloc[0]
                    
                    display_unit = food_info.get('display_unit', '')
                    
                    # Format display
                    amount_str = f"{food['amount_g']}g"
                    
                    if display_unit and isinstance(display_unit, str) and display_unit.strip():
                        # Parse display_unit (e.g., "egg:50" or "tbsp:15")
                        parts = display_unit.split(':')
                        if len(parts) == 2:
                            unit_name = parts[0]
                            unit_weight = float(parts[1])
                            count = food['amount_g'] / unit_weight
                            
                            # Format unit name
                            if count > 1.5:
                                count_int = round(count)
                            else:
                                count_int = round(count, 1)
                            
                            # Plural forms
                            if unit_name == 'egg':
                                unit_display = f"{count_int} {'egg' if count_int == 1 else 'eggs'}"
                            elif unit_name == 'tbsp':
                                unit_display = f"{count_int} tbsp"
                            elif unit_name == 'piece':
                                unit_display = f"{count_int} {'piece' if count_int == 1 else 'pieces'}"
                            elif unit_name == 'slice':
                                unit_display = f"{count_int} {'slice' if count_int == 1 else 'slices'}"
                            elif unit_name == 'cup':
                                unit_display = f"{count_int} {'cup' if count_int == 1 else 'cups'}"
                            else:
                                unit_display = f"{count_int} {unit_name}"
                            
                            amount_str = f"{food['amount_g']}g ({unit_display})"
                    
                    print(f"  - {food['name']}: {amount_str}")
                    print(f"    Cal: {food['calories']:.1f}, "
                          f"P: {food['protein']:.1f}g, "
                          f"C: {food['carbs']:.1f}g, "
                          f"F: {food['fat']:.1f}g")
                
                totals = meal_data['totals']
                print(f"\n  Meal Total: {totals['calories']:.1f} cal, "
                      f"P: {totals['protein']:.1f}g, "
                      f"C: {totals['carbs']:.1f}g, "
                      f"F: {totals['fat']:.1f}g")
                
                for key in grand_total:
                    grand_total[key] += totals[key]
        
        print("\n" + "="*60)
        print("DAILY TOTAL:")
        print(f"Calories: {grand_total['calories']:.1f} kcal")
        print(f"Protein: {grand_total['protein']:.1f}g")
        print(f"Carbs: {grand_total['carbs']:.1f}g")
        print(f"Fat: {grand_total['fat']:.1f}g")
        print("="*60)


# Test
if __name__ == "__main__":
    from data_loader import FoodDatabase
    
    db = FoodDatabase()
    foods = db.get_all_foods()
    
    planner = MealPlanner(foods)
    
    plan = planner.create_daily_plan(
        daily_calories=2000,
        daily_protein=150,
        daily_carbs=200,
        daily_fat=65
    )
    
    planner.print_daily_plan(plan)