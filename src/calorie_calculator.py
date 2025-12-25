"""
BMI and Calorie Calculator for personalized nutrition targets
"""

from typing import Dict, Tuple

class CalorieCalculator:
    """
    Calculates BMI, BMR (Basal Metabolic Rate), and TDEE 
    (Total Daily Energy Expenditure) for personalized nutrition
    """
    
    def __init__(self):
        self.activity_multipliers = {
            '1': {'name': 'Sedentary (little or no exercise)', 'multiplier': 1.2},
            '2': {'name': 'Lightly active (1-3 days/week)', 'multiplier': 1.375},
            '3': {'name': 'Moderately active (3-5 days/week)', 'multiplier': 1.55},
            '4': {'name': 'Very active (6-7 days/week)', 'multiplier': 1.725},
            '5': {'name': 'Extra active (athlete)', 'multiplier': 1.9}
        }
    
    def calculate_bmi(self, weight_kg: float, height_cm: float) -> Dict:
        """
        Calculate BMI (Body Mass Index)
        
        Args:
            weight_kg: Weight in kilograms
            height_cm: Height in centimeters
            
        Returns:
            Dictionary with BMI value and category
        """
        height_m = height_cm / 100
        bmi = weight_kg / (height_m ** 2)
        
        # Determine category
        if bmi < 18.5:
            category = "Underweight"
            health_status = "⚠️  Below healthy weight"
        elif 18.5 <= bmi < 25:
            category = "Normal"
            health_status = "✅ Healthy weight"
        elif 25 <= bmi < 30:
            category = "Overweight"
            health_status = "⚠️  Above healthy weight"
        else:
            category = "Obese"
            health_status = "❌ Significantly above healthy weight"
        
        return {
            'bmi': round(bmi, 1),
            'category': category,
            'health_status': health_status
        }
    
    def calculate_bmr(self, weight_kg: float, height_cm: float, 
                     age: int, gender: str) -> float:
        """
        Calculate BMR using Mifflin-St Jeor Equation
        
        Args:
            weight_kg: Weight in kilograms
            height_cm: Height in centimeters
            age: Age in years
            gender: 'male' or 'female'
            
        Returns:
            BMR in calories
        """
        if gender.lower() == 'male':
            bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
        else:  # female
            bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
        
        return bmr
    
    def calculate_tdee(self, bmr: float, activity_level: str) -> float:
        """
        Calculate TDEE (Total Daily Energy Expenditure)
        
        Args:
            bmr: Basal Metabolic Rate
            activity_level: Activity level key ('1' to '5')
            
        Returns:
            TDEE in calories
        """
        multiplier = self.activity_multipliers[activity_level]['multiplier']
        return bmr * multiplier
    
    def calculate_macros(self, calories: float, goal: str) -> Dict:
        """
        Calculate macronutrient targets based on goal
        
        Args:
            calories: Daily calorie target
            goal: 'weight_loss', 'maintenance', or 'muscle_gain'
            
        Returns:
            Dictionary with protein, carbs, fat in grams
        """
        # Macro ratios based on goal
        if goal == 'weight_loss':
            # High protein, moderate carbs, lower fat
            protein_ratio = 0.35  # 35% of calories
            carbs_ratio = 0.35    # 35% of calories
            fat_ratio = 0.30      # 30% of calories
        elif goal == 'muscle_gain':
            # High protein, high carbs, moderate fat
            protein_ratio = 0.30
            carbs_ratio = 0.45
            fat_ratio = 0.25
        else:  # maintenance
            # Balanced
            protein_ratio = 0.30
            carbs_ratio = 0.40
            fat_ratio = 0.30
        
        # Calculate grams (protein: 4 cal/g, carbs: 4 cal/g, fat: 9 cal/g)
        protein_g = (calories * protein_ratio) / 4
        carbs_g = (calories * carbs_ratio) / 4
        fat_g = (calories * fat_ratio) / 9
        
        return {
            'protein': round(protein_g, 1),
            'carbs': round(carbs_g, 1),
            'fat': round(fat_g, 1)
        }
    
    def get_calorie_target(self, tdee: float, goal: str) -> float:
        """
        Adjust TDEE based on goal
        
        Args:
            tdee: Maintenance calories
            goal: 'weight_loss', 'maintenance', or 'muscle_gain'
            
        Returns:
            Adjusted calorie target
        """
        if goal == 'weight_loss':
            return tdee - 500  # 500 cal deficit
        elif goal == 'muscle_gain':
            return tdee + 300  # 300 cal surplus
        else:  # maintenance
            return tdee
    
    def get_personalized_plan(self) -> Dict:
        """
        Interactive function to get personalized nutrition plan
        
        Returns:
            Dictionary with all calculated values
        """
        print("\n" + "="*60)
        print("  PERSONALIZED NUTRITION CALCULATOR")
        print("="*60)
        print()
        
        # Get user info
        try:
            print("📋 Enter your information:\n")
            
            weight = float(input("  Weight (kg): "))
            height = float(input("  Height (cm): "))
            age = int(input("  Age (years): "))
            
            gender = input("  Gender (male/female): ").lower()
            while gender not in ['male', 'female']:
                print("  ❌ Please enter 'male' or 'female'")
                gender = input("  Gender (male/female): ").lower()
            
            # Calculate BMI
            bmi_data = self.calculate_bmi(weight, height)
            print(f"\n  Your BMI: {bmi_data['bmi']} ({bmi_data['category']})")
            print(f"  {bmi_data['health_status']}")
            
            # Get activity level
            print("\n🏃 Select your activity level:\n")
            for key, value in self.activity_multipliers.items():
                print(f"  {key}. {value['name']}")
            
            activity = input("\nYour choice (1-5): ")
            while activity not in self.activity_multipliers:
                print("  ❌ Please enter a number between 1-5")
                activity = input("Your choice (1-5): ")
            
            # Calculate BMR and TDEE
            bmr = self.calculate_bmr(weight, height, age, gender)
            tdee = self.calculate_tdee(bmr, activity)
            
            print(f"\n  Your BMR: {round(bmr)} calories/day")
            print(f"  Your TDEE: {round(tdee)} calories/day (maintenance)")
            
            # Get goal
            print("\n🎯 Select your goal:\n")
            print("  1. Weight Loss (lose ~0.5kg/week)")
            print("  2. Maintenance (maintain current weight)")
            print("  3. Muscle Gain (gain ~0.25kg/week)")
            
            goal_choice = input("\nYour choice (1-3): ")
            goal_map = {
                '1': 'weight_loss',
                '2': 'maintenance',
                '3': 'muscle_gain'
            }
            
            while goal_choice not in goal_map:
                print("  ❌ Please enter 1, 2, or 3")
                goal_choice = input("Your choice (1-3): ")
            
            goal = goal_map[goal_choice]
            
            # Calculate targets
            target_calories = self.get_calorie_target(tdee, goal)
            macros = self.calculate_macros(target_calories, goal)
            
            # Display results
            print("\n" + "="*60)
            print("  YOUR PERSONALIZED NUTRITION PLAN")
            print("="*60)
            
            goal_names = {
                'weight_loss': 'Weight Loss',
                'maintenance': 'Maintenance',
                'muscle_gain': 'Muscle Gain'
            }
            
            print(f"\nGoal: {goal_names[goal]}")
            print(f"\nDaily Targets:")
            print(f"  Calories:  {round(target_calories)} kcal")
            print(f"  Protein:   {macros['protein']}g")
            print(f"  Carbs:     {macros['carbs']}g")
            print(f"  Fat:       {macros['fat']}g")
            print("\n" + "="*60)
            
            return {
                'bmi': bmi_data,
                'bmr': round(bmr),
                'tdee': round(tdee),
                'goal': goal,
                'targets': {
                    'calories': round(target_calories),
                    'protein': macros['protein'],
                    'carbs': macros['carbs'],
                    'fat': macros['fat']
                },
                'user_info': {
                    'weight': weight,
                    'height': height,
                    'age': age,
                    'gender': gender,
                    'activity': activity
                }
            }
            
        except ValueError:
            print("❌ Invalid input! Please enter valid numbers.")
            return None


# Test
if __name__ == "__main__":
    calc = CalorieCalculator()
    result = calc.get_personalized_plan()
    
    if result:
        print("\n✅ Calculation complete!")
        print(f"Recommendation: {result['targets']}")