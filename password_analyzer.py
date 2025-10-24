import re
from zxcvbn import zxcvbn
import sqlite3
import logging
import os

logging.basicConfig(level=logging.INFO)

def check_length(password: str) -> bool:
    """Checks if password meets minimum length of 12 characters."""
    return len(password) >= 12

def check_diversity(password: str) -> dict:
    """Uses regex to verify character types: uppercase, lowercase, digits, symbols."""
    patterns = {
        'uppercase': re.compile(r'[A-Z]'),
        'lowercase': re.compile(r'[a-z]'),
        'digits': re.compile(r'\d'),
        'symbols': re.compile(r'[!@#$%^&*(),.?":{}|<>]')
    }
    return {k: bool(p.search(password)) for k, p in patterns.items()}

def check_common_words(password: str) -> bool:
    """Queries SQLite DB for matches against common weak passwords."""
    try:
        db_path = os.path.join(os.path.dirname(__file__), 'weak_passwords.db') if '__file__' in globals() else os.path.join(os.getcwd(), 'weak_passwords.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM weak_passwords WHERE password = ?", (password,))
        result = cursor.fetchone()
        conn.close()
        return result is not None
    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")
        return False

def score_password(password: str) -> tuple:
    """Combines zxcvbn guesses_log10 with custom checks for overall score (0-4: weak to strong)."""
    try:
        results = zxcvbn(password)
        guesses_log10 = results.get('guesses_log10', 0)
        diversity = check_diversity(password)
        num_types = sum(diversity.values())
        custom_score = 0
        if check_length(password):
            custom_score += 1
        if num_types >= 3:
            custom_score += 1
        if not check_common_words(password):
            custom_score += 1
        if not re.search(r'(.)\1{2,}', password):
            custom_score += 1
        if not re.search(r'(\d\d|abc|qwerty)', password):
            custom_score += 1
        overall_score = min(4, max(0, (guesses_log10 / 15) + custom_score))
        index = min(3, max(0, int(overall_score)))
        strength = ['Weak', 'Medium', 'Strong', 'Very Strong'][index]
        suggestions = results.get('feedback', {}).get('suggestions', [])
        logging.debug(f"Debug: guesses_log10={guesses_log10}, custom_score={custom_score}, overall_score={overall_score}")
        return overall_score, strength, suggestions
    except Exception as e:
        logging.error(f"Error in score_password: {e}")
        return 0, "Weak", ["Unable to analyze password; try again."]

def suggest_improvements(password: str) -> list:
    """Generates tips based on failed checks."""
    tips = []
    if not check_length(password):
        tips.append("Increase length to at least 12 characters.")
    diversity = check_diversity(password)
    missing = [k for k, v in diversity.items() if not v]
    if missing:
        tips.append(f"Add {', '.join(missing)} characters.")
    if check_common_words(password):
        tips.append("Avoid common words; use unique phrases.")
    return tips

if __name__ == "__main__":
    pwd = input("Enter password: ")
    score, strength, zxcvbn_tips = score_password(pwd)
    tips = suggest_improvements(pwd)
    print(f"Score: {score:.1f}/4 - {strength}")
    print("Suggestions:", tips + zxcvbn_tips)
    if score < 2:
        logging.warning(f"Weak password detected: {pwd[:3]}***")