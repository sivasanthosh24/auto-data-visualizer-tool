# config.py

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VISUALS_PATH = os.path.join(BASE_DIR, '..', 'visuals')
REPORT_PATH = os.path.join(BASE_DIR, '..', 'visualization_report.pdf')
DATA_PATH = os.path.join(BASE_DIR, '..', 'DataAnalyst.csv')

os.makedirs(VISUALS_PATH, exist_ok=True)
