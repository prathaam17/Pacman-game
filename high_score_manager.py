import json
import os

class HighScoreManager:
    def __init__(self, filename="high_scores.json"):
        self.filename = filename
        self.high_score = self.load_high_score()

    def load_high_score(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("high_score", 0)
            except Exception:
                return 0
        return 0

    def update_high_score(self, current_score):
        if current_score > self.high_score:
            self.high_score = current_score
            self.save_high_score()
            return True
        return False

    def save_high_score(self):
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump({"high_score": self.high_score}, f)
        except Exception:
            pass
