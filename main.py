"""Main entry point: loads initiatives from CSV or built-in defaults and optimizes allocation."""

import argparse
from pathlib import Path
from tabulate import tabulate

from src.models import Initiative, StrategicWeights
from src.scorer import calculate_portfolio_metrics
from src.optimizer import select_optimal_portfolio
from src.loader import load_initiatives_from_csv
from src.exporter import export_portfolio_results


def parse_args():
    parser = argparse.ArgumentParser(
        description="PMO Strategic Portfolio Optimization Engine"
    )
    parser.add_argument(
        "--csv",
        type=str,
        default="data/initiatives.csv",
        help="Path to the intake CSV file (default: data/initiatives.csv)",
    )
    parser.add_argument(
        "--budget",
        type=float,
        default=500.0,
        help="Total available capital budget in $k (default: 500.0)",
    )
    parser.add_argument(
        "--capacity",
        type=int,
        default=65,
        help="Total engineering capacity in person-weeks (default: 65)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="output/portfolio_results.xlsx",
        help="Filepath for the exported Excel report (default: output/portfolio_results.xlsx)",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    print("=" * 80)
    print("  PMO STRATEGIC PORTFOLIO ALLOCATION ENGINE")
    print("=" * 80)
    print(f"Loading initiatives from: {args.csv}")

    # 1. Define strategic priorities
    weights = StrategicWeights(
        strategic_alignment=0.35,
        customer_impact=0.30,
        operational_efficiency=0.15,
        risk_reduction=0.20,
    )

    # 2. Ingest from CSV
    initiatives = load_initiatives_from_csv(args.csv)

    # 3. Score and Optimize
    scored_df = calculate_portfolio_metrics(initiatives, weights)
    final_df = select_optimal_portfolio(scored_df, args.budget, args.capacity)

    # 4. Display Results
    display_cols = [
        "id", "name", "sponsor", "adjusted_score", "cost_k_usd",
        "eng_weeks", "is_mandatory", "selection_status"
    ]
    print("\n" + tabulate(final_df[display_cols], headers="keys", tablefmt="github", showindex=False))

    funded = final_df[final_df["selected"]]
    cut = final_df[~final_df["selected"]]

    print("\n" + "=" * 32 + " ALLOCATION SUMMARY " + "=" * 32)
    print(f"Total Initiatives Evaluated   : {len(final_df)}")
    print(f"Initiatives Funded            : {len(funded)} ({len(funded)/len(final_df):.0%})")
    print(f"Initiatives Deferred / Cut    : {len(cut)}")
    print(f"Budget Committed              : ${funded['cost_k_usd'].sum():.1f}k / ${args.budget:.1f}k")
    print(f"Eng Capacity Allocated        : {funded['eng_weeks'].sum()} / {args.capacity} person-weeks")
    print(f"Strategic Value Captured      : {funded['adjusted_score'].sum():.2f} pts")
    print("=" * 84)

    # 5. Export results to multi-tab Excel workbook
    output_file = export_portfolio_results(
        final_df, args.budget, args.capacity, args.output
    )
    print(f"\n[INFO] Portfolio workbook exported to: {output_file.resolve()}")


if __name__ == "__main__":
    main()