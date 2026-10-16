import pandas as pd
from src.optimizer import select_optimal_portfolio

def test_mandatory_initiatives_always_funded():
    df = pd.DataFrame([
        {"id": "1", "adjusted_score": 1.0, "cost_k_usd": 50, "eng_weeks": 10, "is_mandatory": True},
        {"id": "2", "adjusted_score": 10.0, "cost_k_usd": 100, "eng_weeks": 20, "is_mandatory": False},
    ])
    res = select_optimal_portfolio(df, max_budget_k_usd=60, max_eng_weeks=15)
    assert res.loc[res["id"] == "1", "selected"].values[0] == True
    assert res.loc[res["id"] == "2", "selected"].values[0] == False