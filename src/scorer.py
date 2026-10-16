from typing import List
import pandas as pd
from src.models import Initiative, StrategicWeights


def calculate_portfolio_metrics(
    initiatives: List[Initiative], weights: StrategicWeights
) -> pd.DataFrame:
    weights.validate()

    records = []
    for init in initiatives:
        raw_score = (
            init.strategic_alignment * weights.strategic_alignment
            + init.customer_impact * weights.customer_impact
            + init.operational_efficiency * weights.operational_efficiency
            + init.risk_reduction * weights.risk_reduction
        )

        complexity_penalty = 1.0 - ((init.technical_complexity - 1) * 0.05)
        adjusted_score = round(raw_score * complexity_penalty, 2)
        efficiency_ratio = round(adjusted_score / max(init.engineering_person_weeks, 1), 3)

        records.append({
            "id": init.id,
            "name": init.name,
            "sponsor": init.sponsor,
            "is_mandatory": init.is_mandatory,
            "raw_score": round(raw_score, 2),
            "adjusted_score": adjusted_score,
            "cost_k_usd": init.cost_k_usd,
            "eng_weeks": init.engineering_person_weeks,
            "complexity": init.technical_complexity,
            "efficiency_ratio": efficiency_ratio,
        })

    df = pd.DataFrame(records)
    return df.sort_values(by="adjusted_score", ascending=False).reset_index(drop=True)