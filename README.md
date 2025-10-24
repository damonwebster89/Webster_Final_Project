Final Project Password Analyzer
# Password Strength Analyzer

## Project Objectives
This Python-based tool evaluates password strength against common attack patterns like brute force and dictionary attacks. It provides real-time feedback, scores passwords (weak/medium/strong), and suggests improvements to enforce secure password policies. Built using PyCharm, Anaconda, and Jupyter Notebook, it enhances security automation by integrating validation into user systems.

## Key Features
- **Evaluation**: Checks length (≥12 chars), diversity (uppercase, lowercase, numbers, symbols), and patterns using regex and zxcvbn library.
- **Scoring**: Entropy-based scoring with visualizations via matplotlib.
- **Suggestions**: Actionable tips for weak passwords.
- **Database**: SQLite for common password wordlist.
- **Automation**: Real-time validation scripts with logging.
- **AI Integration**: Uses GitHub Copilot for code assistance.

## Setup Instructions
1. **Prerequisites**:
   - Python 3.12+ via Anaconda.
   - Git for version control.
   - Libraries: `zxcvbn`, `matplotlib`, `sqlite3` (install via `conda install` or `pip install zxcvbn matplotlib`).

2. **Clone Repository**:
3. **Environment Setup**:
- Create Anaconda env: `conda create -n password-analyzer python=3.12`
- Activate: `conda activate password-analyzer`
- Install deps: `pip install zxcvbn matplotlib`

4. **Run the Code**:
- Main script: `python password_analyzer.py`
- Jupyter Notebook: `jupyter notebook password_analysis.ipynb` (prototype tests).
- Example: Input a password via CLI; view score and suggestions.

## Additional Information
- Data: `weak_passwords.db` contains 2025 common passwords (e.g., "123456") sourced ethically.
- Testing: Run `tests/test_strength.py` for unit tests.

