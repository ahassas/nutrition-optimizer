import pandas as pd
from typing import List, Dict

class FoodDatabase:
    """Loads and manages food nutritional data"""
    
    def __init__(self, csv_path: str = "data/foods.csv"):
        self.df = pd.read_csv(csv_path)
        
    def get_all_foods(self) -> pd.DataFrame:
        """Returns all foods in database"""
        return self.df
    
    def get_food_by_id(self, food_id: int) -> Dict:
        """Returns single food item by ID"""
        food = self.df[self.df['food_id'] == food_id]
        if food.empty:
            return None
        return food.iloc[0].to_dict()
    
    def search_foods(self, category: str = None) -> pd.DataFrame:
        """Filter foods by category"""
        if category:
            return self.df[self.df['category'] == category]
        return self.df

# Test
if __name__ == "__main__":
    db = FoodDatabase()
    print("All foods:")
    print(db.get_all_foods())
    print("\nProtein sources:")
    print(db.search_foods("protein"))