"""
Script to explore the Kaggle construction dataset
"""
import pandas as pd
import os

def explore_dataset():
    """Explore the construction dataset structure"""

    # Check which files exist
    files = {
        'tasks': 'Construction_Data_PM_Tasks_All_Projects.csv',
        'forms': 'Construction_Data_PM_Forms_All_Projects.csv'
    }

    for name, filepath in files.items():
        if os.path.exists(filepath):
            print(f"\n{'='*80}")
            print(f"EXPLORING: {name.upper()} - {filepath}")
            print('='*80)

            # Load the dataset
            df = pd.read_csv(filepath)

            # Basic info
            print(f"\n[SHAPE] {df.shape[0]} rows x {df.shape[1]} columns")

            # Column names
            print(f"\n[COLUMNS] ({len(df.columns)}):")
            for i, col in enumerate(df.columns, 1):
                print(f"  {i:2d}. {col}")

            # Data types
            print(f"\n[DATA TYPES]:")
            print(df.dtypes.value_counts())

            # First few rows
            print(f"\n[FIRST 3 ROWS]:")
            print(df.head(3).to_string())

            # Missing values
            print(f"\n[MISSING VALUES]:")
            missing = df.isnull().sum()
            if missing.sum() > 0:
                print(missing[missing > 0])
            else:
                print("  No missing values!")

            # Sample values for text columns
            print(f"\n[SAMPLE TEXT COLUMNS]:")
            text_cols = df.select_dtypes(include=['object']).columns
            for col in text_cols[:5]:  # Show first 5 text columns
                print(f"\n  {col}:")
                print(f"    Unique values: {df[col].nunique()}")
                print(f"    Sample: {df[col].dropna().iloc[0] if len(df[col].dropna()) > 0 else 'N/A'}")
        else:
            print(f"\n[WARNING] File not found: {filepath}")

if __name__ == "__main__":
    explore_dataset()
