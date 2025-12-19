#!/usr/bin/env python3
"""
Interactive CLI Demo for Nutrition Optimizer
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_loader import FoodDatabase
from meal_planner import MealPlanner
from optimizer import NutritionOptimizer
from calorie_calculator import CalorieCalculator
import matplotlib.pyplot as plt
import numpy as np

class NutritionDemo:
    """Interactive demo for nutrition optimization"""
    
    def __init__(self):
        print("Loading food database...")
        self.db = FoodDatabase("data/foods.csv")
        self.foods = self.db.get_all_foods()
        self.planner = MealPlanner(self.foods)
        self.calculator = CalorieCalculator()
        print("Database loaded!\n")
    
    def show_welcome(self):
        """Display welcome message"""
        print("="*60)
        print("  DAILY NUTRITION OPTIMIZER")
        print("  Optimizing your meals with AI")
        print("="*60)
        print()
    
    def get_user_targets(self):
        """Get nutritional targets from user"""
        print("\nEnter your daily nutritional targets:\n")
        
        try:
            calories = float(input("  Daily Calories (e.g., 2000): "))
            protein = float(input("  Daily Protein in grams (e.g., 150): "))
            carbs = float(input("  Daily Carbs in grams (e.g., 200): "))
            fat = float(input("  Daily Fat in grams (e.g., 65): "))
            
            return {
                'calories': calories,
                'protein': protein,
                'carbs': carbs,
                'fat': fat
            }
        except ValueError:
            print("Invalid input! Please enter numbers only.")
            return None
    
    def show_preset_options(self):
        """Show preset meal plans"""
        print("\nChoose a preset:")
        print("  1. Weight Loss (1800 cal, High Protein)")
        print("  2. Muscle Gain (2500 cal, High Protein)")
        print("  3. Maintenance (2000 cal, Balanced)")
        print("  4. Back to main menu")
        
        choice = input("\nYour choice (1-4): ").strip()
        
        presets = {
            '1': {'calories': 1800, 'protein': 140, 'carbs': 150, 'fat': 60},
            '2': {'calories': 2500, 'protein': 180, 'carbs': 280, 'fat': 70},
            '3': {'calories': 2000, 'protein': 150, 'carbs': 200, 'fat': 65}
        }
        
        if choice in presets:
            return presets[choice]
        else:
            return None
    
    def optimize_meals(self, targets):
        """Run optimization"""
        print("\nOptimizing your meal plan...")
        print("This may take a few seconds...\n")
        
        plan = self.planner.create_daily_plan(
            daily_calories=targets['calories'],
            daily_protein=targets['protein'],
            daily_carbs=targets['carbs'],
            daily_fat=targets['fat']
        )
        
        return plan
    
    def display_results(self, plan, targets):
        """Display optimization results"""
        self.planner.print_daily_plan(plan)
        
        # Calculate accuracy
        grand_total = {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0}
        
        for meal_data in plan.values():
            if meal_data['status'] == 'optimal':
                for key in grand_total:
                    grand_total[key] += meal_data['totals'][key]
        
        print("\nTARGET vs ACTUAL:")
        print("-" * 60)
        metrics = ['calories', 'protein', 'carbs', 'fat']
        for metric in metrics:
            target = targets[metric]
            actual = grand_total[metric]
            diff = actual - target
            percentage = (actual / target * 100) if target > 0 else 0
            
            print(f"{metric.capitalize():10s}: "
                  f"Target: {target:7.1f} | "
                  f"Actual: {actual:7.1f} | "
                  f"Diff: {diff:+7.1f} ({percentage:.1f}%)")
        print("-" * 60)
    
    def visualize_results(self, plan, targets):
        """Create visualization of results"""
        print("\nGenerating visualization...")
        
        # Collect totals
        grand_total = {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0}
        meal_totals = {}
        
        for meal_name, meal_data in plan.items():
            if meal_data['status'] == 'optimal':
                meal_totals[meal_name] = meal_data['totals']
                for key in grand_total:
                    grand_total[key] += meal_data['totals'][key]
        
        # Create figure with subplots
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Daily Nutrition Plan Analysis', fontsize=16, fontweight='bold')
        
        # 1. Macros comparison
        ax1 = axes[0, 0]
        macros = ['Protein', 'Carbs', 'Fat']
        target_values = [targets['protein'], targets['carbs'], targets['fat']]
        actual_values = [grand_total['protein'], grand_total['carbs'], grand_total['fat']]
        
        x = np.arange(len(macros))
        width = 0.35
        
        ax1.bar(x - width/2, target_values, width, label='Target', color='skyblue')
        ax1.bar(x + width/2, actual_values, width, label='Actual', color='lightcoral')
        ax1.set_ylabel('Grams')
        ax1.set_title('Macronutrients: Target vs Actual')
        ax1.set_xticks(x)
        ax1.set_xticklabels(macros)
        ax1.legend()
        ax1.grid(axis='y', alpha=0.3)
        
        # 2. Calories by meal
        ax2 = axes[0, 1]
        meals = list(meal_totals.keys())
        meal_cals = [meal_totals[m]['calories'] for m in meals]
        colors = ['#FFD700', '#FF6347', '#4169E1']
        
        ax2.pie(meal_cals, labels=meals, autopct='%1.1f%%', colors=colors, startangle=90)
        ax2.set_title('Calorie Distribution by Meal')
        
        # 3. Protein distribution
        ax3 = axes[1, 0]
        meal_names = list(meal_totals.keys())
        protein_vals = [meal_totals[m]['protein'] for m in meal_names]
        
        ax3.barh(meal_names, protein_vals, color='salmon')
        ax3.set_xlabel('Protein (g)')
        ax3.set_title('Protein Distribution by Meal')
        ax3.grid(axis='x', alpha=0.3)
        
        # 4. Accuracy
        ax4 = axes[1, 1]
        categories = ['Calories', 'Protein\n(g)', 'Carbs\n(g)', 'Fat\n(g)']
        target_vals = [targets['calories'], targets['protein'], targets['carbs'], targets['fat']]
        actual_vals = [grand_total['calories'], grand_total['protein'], grand_total['carbs'], grand_total['fat']]
        accuracy = [(a/t*100) if t > 0 else 0 for a, t in zip(actual_vals, target_vals)]
        
        bars = ax4.bar(categories, accuracy, color=['green' if 95 <= a <= 105 else 'orange' for a in accuracy])
        ax4.axhline(y=100, color='red', linestyle='--', label='Target (100%)')
        ax4.set_ylabel('Accuracy (%)')
        ax4.set_title('Target Achievement')
        ax4.legend()
        ax4.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        
        output_path = 'demo/nutrition_analysis.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Visualization saved to: {output_path}")
        
        plt.show()
    
    def run(self):
        """Main demo loop"""
        self.show_welcome()
        
        while True:
            # Main menu
            print("\n" + "="*60)
            print("  MAIN MENU")
            print("="*60)
            print("\nHow would you like to proceed?\n")
            print("  1. Calculate personalized plan (BMI + Activity)")
            print("  2. Choose preset meal plan")
            print("  3. Enter custom targets manually")
            print("  4. Exit")
            
            choice = input("\nYour choice (1-4): ").strip()
            
            targets = None
            
            if choice == '1':
                # BMI Calculator
                print("\n" + "="*60)
                calc_result = self.calculator.get_personalized_plan()
                if calc_result:
                    targets = calc_result['targets']
                else:
                    continue
            
            elif choice == '2':
                # Presets
                targets = self.show_preset_options()
                if targets is None:
                    continue
            
            elif choice == '3':
                # Custom
                targets = self.get_user_targets()
                if targets is None:
                    continue
            
            elif choice == '4':
                print("\nThank you for using Nutrition Optimizer!")
                break
            
            else:
                print("Invalid choice! Please enter 1-4.")
                continue
            
            if targets is None:
                continue
            
            print(f"\nTargets confirmed!")
            print(f"  Calories: {targets['calories']} kcal")
            print(f"  Protein:  {targets['protein']}g")
            print(f"  Carbs:    {targets['carbs']}g")
            print(f"  Fat:      {targets['fat']}g")
            
            # Optimize
            plan = self.optimize_meals(targets)
            
            # Display
            self.display_results(plan, targets)
            
            # Visualize
            viz = input("\nGenerate visualization? (y/n): ").lower().strip()
            if viz == 'y':
                self.visualize_results(plan, targets)
            
            # Again?
            again = input("\nCreate another plan? (y/n): ").lower().strip()
            if again != 'y':
                print("\nThank you for using Nutrition Optimizer!")
                break


if __name__ == "__main__":
    demo = NutritionDemo()
    demo.run()
