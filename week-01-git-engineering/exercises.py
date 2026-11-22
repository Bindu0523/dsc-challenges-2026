"""Week 1: Python Fundamentals Practice Tasks."""

import csv
import json
from typing import Dict, List, Tuple, Any


def evaluate_attendance_status(attended: int, total: int) -> str:
    if total <= 0:
        return "NO_SESSIONS"

    percentage = (attended / total) * 100

    if percentage >= 75:
        return "ELIGIBLE"
    elif percentage >= 65:
        return "WARNING"
    else:
        return "SHORTAGE"


def safe_parse_float(raw_value: Any, default: float = 0.0) -> float:
    try:
        return float(raw_value)
    except (ValueError, TypeError):
        return default


def analyze_pod_scores(records: List[Tuple[str, str, float]]) -> Dict[str, Any]:
    unique_usns = {usn for usn, pod_name, score in records}

    high_scorers = [
        usn for usn, pod_name, score in records if score >= 80
    ]

    pod_scores = {}
    for usn, pod_name, score in records:
        pod_scores.setdefault(pod_name, []).append(score)

    pod_averages = {
        pod: round(sum(scores) / len(scores), 2)
        for pod, scores in pod_scores.items()
    }

    return {
        "unique_student_count": len(unique_usns),
        "high_scorers": high_scorers,
        "pod_averages": pod_averages,
    }


def summarize_csv_to_json(csv_path: str, json_path: str) -> Dict[str, Any]:
    with open(csv_path, "r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        records = list(reader)

    total_students = len(records)

    branches = sorted({
        row["branch"] for row in records
    })

    scores = [
        float(row["score"]) for row in records
    ]

    average_score = (
        round(sum(scores) / len(scores), 2)
        if scores else 0.0
    )

    summary = {
        "total_students": total_students,
        "branches": branches,
        "average_score": average_score,
    }

    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(summary, json_file, indent=4)

    return summary


class StudentRecord:
    """Tracks weekly evaluation scores for a single DSC recruit."""

    def __init__(self, usn: str, name: str):
        self.usn = usn.upper()
        self.name = name
        self.scores = []

    def add_score(self, score: float) -> None:
        if not 0 <= score <= 100:
            raise ValueError("Score must be between 0 and 100")
        self.scores.append(score)

    def average(self) -> float:
        if not self.scores:
            return 0.0
        return round(sum(self.scores) / len(self.scores), 2)

    def is_passing(self, threshold: float = 50.0) -> bool:
        return self.average() >= threshold