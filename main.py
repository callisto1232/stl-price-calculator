import sys
import os
from datetime import datetime

# --- CONFIGURATION (Your Sheet's Constants) ---
PRINTER_WATT = 300
ELECTRICITY_PER_KWH = 3.11
DEPRECIATION_PER_HOUR = 6.00
WASTAGE_MULTIPLIER = 1.1

FILAMENT_DATABASE = {
    "PLA": {"type": "Standard", "price_per_gram": 0.60},
    "PETG": {"type": "Standard", "price_per_gram": 0.74},
    "ABS": {"type": "Industrial", "price_per_gram": 0.55},
    "ASA": {"type": "Industrial", "price_per_gram": 0.81},
    "PETG-CF": {"type": "Industrial", "price_per_gram": 1.40},
    "TPU": {"type": "Standard", "price_per_gram": 1.00}
}

MULTIPLIERS = {
    "Standard": 2.5,
    "Industrial": 4.0
}

def calculate_printing_cost(filament_name, weight_grams, print_time_hours, labor_cost=0.0):
    if filament_name not in FILAMENT_DATABASE:
        print(f"Error: Material '{filament_name}' not found.")
        return None

    mat_info = FILAMENT_DATABASE[filament_name]
    
    # 1. Material Cost (with wastage)
    base_filament_cost = weight_grams * mat_info["price_per_gram"]
    total_filament_cost = base_filament_cost * WASTAGE_MULTIPLIER
    
    # 2. Electricity Cost
    electricity_cost = (PRINTER_WATT / 1000) * print_time_hours * ELECTRICITY_PER_KWH
    
    # 3. Depreciation/Machine Wear Cost
    depreciation_cost = print_time_hours * DEPRECIATION_PER_HOUR
    
    # 4. Total Expense
    total_expense = total_filament_cost + electricity_cost + depreciation_cost
    
    # 5. Selling Price Calculation based on Type
    mat_type = mat_info["type"]
    multiplier = MULTIPLIERS[mat_type]
    selling_price = (total_expense * multiplier) + labor_cost
    
    return {
        "filament_cost": total_filament_cost,
        "electricity_cost": electricity_cost,
        "depreciation_cost": depreciation_cost,
        "total_expense": total_expense,
        "selling_price": selling_price
    }

def save_to_markdown(model_name, filament, weight, time, labor, results):
    filename = "print_records.md"
    file_exists = os.path.exists(filename)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(filename, "a", encoding="utf-8") as f:
        if not file_exists:
            f.write("# 3D Printing Price Records\n\n")
            f.write("| Date/Time | Model Name | Filament | Weight (g) | Time (h) | Labor (TRY) | Total Expense (TRY) | Selling Price (TRY) |\n")
            f.write("|---|---|---|---|---|---|---|---|\n")
            
        f.write(f"| {timestamp} | {model_name} | {filament} | {weight} | {time} | {labor:.2f} | {results['total_expense']:.2f} | {results['selling_price']:.2f} |\n")
    
    print(f"\n[!] Record saved successfully to '{filename}'")

# --- INTERACTIVE TERMINAL CLI ---
def main():
    print("=== 3D Printing Price Calculator ===")
    print(f"Available filaments: {', '.join(FILAMENT_DATABASE.keys())}")
    
    try:
        filament = input("Enter filament type: ").strip().upper()
        weight = float(input("Enter model weight in grams: "))
        time = float(input("Enter print time in hours (e.g., 2.5): "))
        labor = input("Enter labor cost (Press Enter for 0.00 TRY): ")
        labor = float(labor) if labor.strip() else 0.0
        
        results = calculate_printing_cost(filament, weight, time, labor)
        
        if results:
            print("\n" + "="*30)
            print(f"Results for {filament} Print:")
            print(f"Filament Cost:    {results['filament_cost']:.2f} TRY")
            print(f"Electricity Cost: {results['electricity_cost']:.2f} TRY")
            print(f"Machine Wear:     {results['depreciation_cost']:.2f} TRY")
            print("-" * 30)
            print(f"Total Expense:    {results['total_expense']:.2f} TRY")
            print(f"SUGGESTED PRICE:  {results['selling_price']:.2f} TRY")
            print("="*30)
            
            # Ask to save first
            save_choice = input("\nDo you want to save this record to markdown? (y/N): ").strip().lower()
            if save_choice == 'y':
                model_name = input("Enter model/order name: ").strip()
                if not model_name:
                    model_name = "Unnamed Model"
                save_to_markdown(model_name, filament, weight, time, labor, results)
            else:
                print("Skipped saving.")
                
    except ValueError:
        print("Invalid input. Please enter numbers for weight, time, and labor.")

if __name__ == "__main__":
    main()
