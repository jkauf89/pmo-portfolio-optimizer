from dataclasses import dataclass


@dataclass
class StrategicWeights:
    strategic_alignment: float = 0.35
    customer_impact: float = 0.25
    operational_efficiency: float = 0.15
    risk_reduction: float = 0.25

    def validate(self) -> None:
        total = (
            self.strategic_alignment
            + self.customer_impact
            + self.operational_efficiency
            + self.risk_reduction
        )
        if not (0.99 <= total <= 1.01):
            raise ValueError(f"Weights must sum to 1.0. Current sum: {total:.2f}")


@dataclass
class Initiative:
    id: str
    name: str
    sponsor: str
    strategic_alignment: float
    customer_impact: float
    operational_efficiency: float
    risk_reduction: float
    cost_k_usd: float
    engineering_person_weeks: int
    technical_complexity: float
    is_mandatory: bool = False