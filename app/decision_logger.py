import csv
import os
from datetime import datetime
from logic import DecisionResult

LOG_FILE = "decision_log.csv"

def log_decision(decision: DecisionResult, trade_data: dict):
    """Logs a trade decision and its evaluation to a CSV file."""
    file_exists = os.path.isfile(LOG_FILE)
    
    with open(LOG_FILE, mode='a', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            "timestamp", "score", "quality",
            "reasons", "warnings",
            *trade_data.keys()
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        
        row = {
            "timestamp": datetime.now().isoformat(),
            "score": decision.score,
            "quality": decision.quality,
            "reasons": "; ".join(decision.reasons),
            "warnings": "; ".join(decision.warnings),
            **trade_data
        }
        writer.writerow(row)
