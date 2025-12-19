# logic.py - Decision Engine V1
from dataclasses import dataclass
from typing import Dict, List, Tuple
from PIL import Image

@dataclass
class DecisionResult:
    """Represents the outcome of a trade decision evaluation."""
    score: int
    quality: str
    reasons: List[str]
    warnings: List[str]

def _collect_positive_points(criteria: Dict[str, bool]) -> Tuple[int, List[str]]:
    """Assign positive points based on passed criteria."""
    positive_rules = [
        ("structure_valid", 30, "Structure valid (clear S/R or trend break)"),
        ("liquidity_respected", 25, "Liquidity logic respected (post-sweep, no trap)"),
        ("pattern_confirmation", 20, "Pattern confirmation present"),
        ("optimal_timing", 15, "Timing is optimal (session/session open)"),
        ("acceptable_rr", 10, "Risk-reward is acceptable (RR ≥ 1.5)"),
    ]

    score = 0
    reasons: List[str] = []
    for key, points, description in positive_rules:
        if criteria.get(key):
            score += points
            reasons.append(description)
    return score, reasons

def _collect_negative_points(criteria: Dict[str, bool]) -> Tuple[int, List[str]]:
    """Assign negative points and record warnings for risky conditions."""
    negative_rules = [
        ("entry_before_sweep", -20, "Entry occurred before liquidity sweep"),
        ("counter_trend", -15, "Position is counter-trend"),
        ("impulsive_entry", -10, "Impulsive entry with no confirmation"),
    ]

    score = 0
    warnings: List[str] = []
    for key, points, description in negative_rules:
        if criteria.get(key):
            score += points
            warnings.append(description)
    return score, warnings

def _determine_quality(score: int) -> str:
    """Map a numeric score to a qualitative decision label."""
    if score >= 75:
        return "Good Decision"
    if score >= 50:
        return "Risky Decision"
    return "Bad Decision"

def evaluate_trade_decision(criteria: Dict[str, bool]) -> DecisionResult:
    """Evaluate a trade setup using a structured scoring model."""
    positive_score, reasons = _collect_positive_points(criteria)
    negative_score, warnings = _collect_negative_points(criteria)

    raw_score = positive_score + negative_score
    bounded_score = max(0, min(100, raw_score))
    quality = _determine_quality(bounded_score)

    return DecisionResult(
        score=bounded_score,
        quality=quality,
        reasons=reasons,
        warnings=warnings,
    )

def analyze_chart_image(uploaded_file):
    """Placeholder image analysis — يمكن تحديثها لاحقًا برؤية حاسوبية أو GPT Vision."""
    image = Image.open(uploaded_file)
    return "This function is deprecated; use evaluate_trade_decision instead."
