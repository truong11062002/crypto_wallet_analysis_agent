from datetime import datetime
from typing import List, Dict

from dataclasses import dataclass


@dataclass
class WalletAge:
    first_transaction_date: datetime
    age_years: int
    age_months: int
    age_days: int
    category: str
    analysis: str


@dataclass
class TrendAnalysis:
    period_days: int
    overall_change: str
    notable_changes: List[str]


@dataclass
class TransactionAnalysis:
    avg_size_usd: float
    size_category: str
    total_volume_usd: float
    volume_percent: float
    top_assets: List[Dict[str, str]]
    daily_transactions: float
    analysis: str


@dataclass
class BehavioralAnalysis:
    classification: str
    confidence: str
    key_indicators: List[str]
    contradicting_factors: List[str]
    analysis: str
