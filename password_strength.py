import numpy as np
import re

def analyse_passwords(passwords: list[str]) -> np.ndarray:
    """Analyse a list of passwords and return a NumPy array of scores"""

    p_array = np.array(passwords)
    
    # Calculate Length Score (capped at 12)
    # Using np.char.str_len for vectorized length calculation
    lengths = np.char.str_len(p_array)
    length_scores = np.clip(lengths, 0, 12)
    
    # Complexity Bonuses (Vectorized checks using list comprehension)
    has_digit = np.array([1 if re.search(r'\d', p) else 0 for p in passwords])
    has_special = np.array([1 if re.search(r'[!@#£$%^&*(),.?":{}|<>]', p) else 0 for p in passwords])
    has_upper = np.array([1 if re.search(r'[A-Z]', p) else 0 for p in passwords])
    
    # Final Score Calculation
    return length_scores + (has_digit * 2) + (has_special * 3) + (has_upper * 2)

def get_strength_labels(scores: np.ndarray) -> np.ndarray:
    """Categorise numerical scores into human-readable labels using NumPy"""

    conditions = [
        (scores <= 5),
        (scores > 5) & (scores <= 10),
        (scores > 10) & (scores <= 15),
        (scores > 15)
    ]
    
    choices = ["Very Weak 😱", "Weak 😟", "Moderate 😐", "Strong 💪"]
    
    # np.select applies the labels based on the score ranges
    return np.select(conditions, choices, default="Unrated ❓")

# Main Execution Block
if __name__ == "__main__":
    # Test dataset
    my_passwords = [
        "123", 
        "password", 
        "Admin123", 
        "Secure!Tr0n9", 
        "qwerty", 
        "P@ssw0rd2024!!",
        "cat"
    ]
    
    # Process the data
    raw_scores = analyse_passwords(my_passwords)
    strength_levels = get_strength_labels(raw_scores)
    
    # Print the Table
    print(f"\n{'Password':<20} | {'Score':<5} | {'Strength'}")
    print("-" * 45)
    for pw, score, label in zip(my_passwords, raw_scores, strength_levels):
        print(f"{pw:<20} | {score:<5} | {label}")
    
    # Generate NumPy Summary Report
    print("\n" + "="*45)
    print("📊 BATCH SECURITY REPORT (Powered by NumPy)")
    print("="*45)
    
    print(f"Total Passwords Analysed : {len(raw_scores)}")
    print(f"Average Security Score   : {np.mean(raw_scores):.2f}")
    print(f"Highest Security Score   : {np.max(raw_scores)}")
    print(f"Lowest Security Score    : {np.min(raw_scores)}")
    
    # Use np.unique to count how many of each category we have
    categories, counts = np.unique(strength_levels, return_counts=True)
    stats = dict(zip(categories, counts))
    
    print("\nBreakdown by Category:")
    # Loop through known labels to keep the order nice
    for cat in ["Strong 💪", "Moderate 😐", "Weak 😟", "Very Weak 😱"]:
        count = stats.get(cat, 0)
        print(f"- {cat:15}: {count}")
    
    print("="*45)