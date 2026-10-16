from __future__ import annotations
import numpy as np
import pandas as pd
from scipy.optimize import Bounds, LinearConstraint, milp


def select_optimal_portfolio(
    df: pd.DataFrame,
    budget_cap: float = None,
    capacity_cap: int = None,
    max_budget_k_usd: float = None,
    max_eng_weeks: int = None,
) -> pd.DataFrame:
    """Solves the multi-constraint knapsack problem using MILP."""
    # Resolve argument aliases
    effective_budget = budget_cap if budget_cap is not None else max_budget_k_usd
    effective_capacity = capacity_cap if capacity_cap is not None else max_eng_weeks

    if effective_budget is None or effective_capacity is None:
        raise ValueError("Budget and capacity constraints must be specified.")

    df = df.copy()

    # Objective: Maximize total adjusted score (negated for minimization)
    c = -df["adjusted_score"].values

    # Constraints: Cost and Capacity ceilings
    A = np.vstack([df["cost_k_usd"].values, df["eng_weeks"].values])
    b_u = np.array([effective_budget, effective_capacity])
    b_l = np.array([0.0, 0.0])
    constraints = LinearConstraint(A, b_l, b_u)

    # Bounds: Mandatory projects forced to 1.0, others between 0.0 and 1.0
    lb = np.where(df["is_mandatory"].values, 1.0, 0.0)
    ub = np.ones(len(df))
    bounds = Bounds(lb, ub)

    # Integrality: 1 indicates all variables are binary (0 or 1)
    integrality = np.ones(len(df))

    res = milp(c=c, constraints=constraints, bounds=bounds, integrality=integrality)

    if not res.success:
        raise RuntimeError(f"Optimization failed: {res.status_message}")

    df["selected"] = res.x > 0.5
    df["selection_status"] = np.where(df["selected"], "FUNDED", "CUT")

    df = df.sort_values(
        by=["selected", "adjusted_score"], ascending=[False, False]
    ).reset_index(drop=True)

    return df