"""Performance tests for optimizer"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_loader import FoodDatabase
from optimizer import NutritionOptimizer
import time

def test_optimization_speed():
    """Test how fast optimizer runs"""
    print("⏱️  Testing optimization speed...\n")
    
    db = FoodDatabase("data/foods.csv")
    foods = db.get_all_foods()
    optimizer = NutritionOptimizer(foods)
    
    test_cases = [
        {'name': 'Low Cal', 'cal': 1500, 'prot': 120, 'carbs': 150, 'fat': 50},
        {'name': 'Maintenance', 'cal': 2000, 'prot': 150, 'carbs': 200, 'fat': 65},
        {'name': 'Bulk', 'cal': 2800, 'prot': 200, 'carbs': 320, 'fat': 80},
    ]
    
    for test in test_cases:
        start = time.time()
        result = optimizer.optimize(
            target_calories=test['cal'],
            target_protein=test['prot'],
            target_carbs=test['carbs'],
            target_fat=test['fat']
        )
        end = time.time()
        
        duration = (end - start) * 1000  # ms
        status = "✅" if result['status'] == 'optimal' else "❌"
        
        print(f"{status} {test['name']:15s} - {duration:6.2f}ms - {result['status']}")
    
    print("\n✅ Performance test completed!")

if __name__ == "__main__":
    test_optimization_speed()