"""CSV intake and validation for PMO initiatives exported from Excel or Google Sheets."""

from __future__ import annotations
from pathlib import Path
from typing import List
import pandas as pd
from src.models import Initiative


REQUIRED_COLUMNS = {
    "id",
    "name",
    "sponsor",
    "strategic_alignment",
    "customer_impact",
    "operational_efficiency",
    "risk_reduction",
    "cost_k_usd",
    "engineering_person_weeks",
    "technical_complexity",
    "is_mandatory",
}


def load_initiatives_from_csv(filepath: Union[str, Path]) -> List[Initiative]:
    """Reads a CSV file exported from Sheets/Excel and parses it into validated Initiative models."""
    path = Path(filepath)

    # If the relative path isn't found in current working directory,
    # check relative to the project root (one level above src/)
    if not path.is_absolute() and not path.exists():
        project_root = Path(__file__).resolve().parent.parent
        candidate = project_root / filepath
        if candidate.exists():
            path = candidate

    if not path.exists():
        raise FileNotFoundError(f"Portfolio file not found at: {path.resolve()}")

    df = pd.read_csv(path)

    # 1. Clean column names (strip whitespace and lowercase)
    df.columns = df.columns.str.strip().str.lower()

    # 2. Check for missing required columns
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"CSV is missing required headers: {sorted(missing)}")

    # 3. Normalize boolean column (handles True/False, 'yes'/'no', 1/0)
    df["is_mandatory"] = (
        df["is_mandatory"]
        .astype(str)
        .str.strip()
        .str.lower()
        .isin(["true", "1", "yes", "y"])
    )

    # 4. Construct Initiative instances
    initiatives: List[Initiative] = []
    for _, row in df.iterrows():
        initiatives.append(
            Initiative(
                id=str(row["id"]).strip(),
                name=str(row["name"]).strip(),
                sponsor=str(row["sponsor"]).strip(),
                strategic_alignment=float(row["strategic_alignment"]),
                customer_impact=float(row["customer_impact"]),
                operational_efficiency=float(row["operational_efficiency"]),
                risk_reduction=float(row["risk_reduction"]),
                cost_k_usd=float(row["cost_k_usd"]),
                engineering_person_weeks=int(row["engineering_person_weeks"]),
                technical_complexity=float(row["technical_complexity"]),
                is_mandatory=bool(row["is_mandatory"]),
            )
        )

    return initiatives