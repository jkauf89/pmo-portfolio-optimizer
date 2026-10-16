## PMO Portfolio Optimizer

A quantitative decision-support tool designed for PMOs, Technical Program Managers, and IT Directors. This engine uses Mixed-Integer Linear Programming (MILP) to resolve competing roadmap demands by finding the mathematically optimal portfolio of initiatives that maximizes strategic return within hard capital budget and engineering capacity constraints.

The Business Problem

* Every planning cycle, leadership faces more project requests than teams have the time, money, or people to deliver. Without an objective framework, planning often runs into predictable challenges:
* The Loudest Voice Wins: Projects often get approved based on executive advocacy or political influence rather than clear business value.
* Chronic Overcommitment: Teams say "yes" to too many high-priority initiatives without a clear view of shared team limits, leading to missed deadlines and employee burnout.
* Hidden Delivery Risks: Complex, unpredictable projects are treated the same as straightforward ones, leading to budget overruns down the road.
* Unclear Trade-offs: When hard choices must be made, leaders lack a transparent way to explain why Project A was funded while Project B was cut.
* This tool gives decision-makers a clear, transparent framework to score competing initiatives, honor strict budget and staffing limits, and build a defensible portfolio that delivers the highest strategic return.

**Project Structure**

```text
pmo-portfolio-optimizer/
│
├── data/
│   └── initiatives.csv        # Intake file (Excel/Google Sheets export)
│
├── output/
│   └── portfolio_results.xlsx # Auto-generated multi-tab executive workbook
│
├── src/
│   ├── __init__.py
│   ├── models.py              # Domain dataclasses & constraint schemas
│   ├── loader.py              # Defensive CSV parser & data sanitizer
│   ├── scorer.py              # Strategic value & complexity penalty math
│   ├── optimizer.py           # Mixed-Integer Linear Programming (MILP) solver
│   └── exporter.py            # Styled multi-tab Excel reporting engine
│
├── tests/
│   └── test_optimizer.py      # Automated boundary & knapsack unit tests
│
├── .gitignore
├── main.py                    # Configurable CLI runner
├── requirements.txt
└── README.md
```

**Data Schema & Intake**

The optimizer ingests intake exports directly from **Google Sheets** or **Microsoft Excel** saved as `.csv`. 

Files must include the following 11 column headers:

| Column Header | Type | Valid Values | Description |
|---|---|---|---|
| `id` | String | e.g., `INIT-101` | Unique initiative tracking identifier |
| `name` | String | Text | Initiative title |
| `sponsor` | String | Text | Department or executive owner |
| `strategic_alignment` | Float | `1.0` to `10.0` | Direct contribution to corporate OKRs |
| `customer_impact` | Float | `1.0` to `10.0` | Revenue lift, retention, or acquisition impact |
| `operational_efficiency`| Float | `1.0` to `10.0` | Internal toil reduction & tech debt payoff |
| `risk_reduction` | Float | `1.0` to `10.0` | Security, compliance, and reliability uplift |
| `cost_k_usd` | Float | `> 0` | Capital cost in thousands (`180` = $180,000) |
| `engineering_person_weeks` | Integer | `> 0` | Total dev team capacity needed |
| `technical_complexity` | Float | `1.0` to `5.0` | Architectural risk penalty factor (`1.0` low, `5.0` extreme) |
| `is_mandatory` | Boolean | `True`/`False`, `yes`/`no` | Legal, audit, or security non-negotiable |

The built-in parser (`src/loader.py`) automatically strips whitespace, normalizes case variations, and validates that all mandatory headers are present before calculation.

**Executive Reporting & Excel Export**


In addition to standard terminal summaries, each optimization run automatically outputs a publication-grade, styled Excel workbook (`output/portfolio_results.xlsx`) containing 4 purpose-built sheets:

| Sheet Name | Content / Purpose |
|---|---|
| **Executive Summary** | High-level scorecard structured into 4 executive categories: *Portfolio Scope*, *Financial Capital*, *Capacity & Resourcing*, and *Strategic ROI*. Includes budget and person-week utilization rates. |
| **Funded Initiatives** | Filtered view containing only the projects selected for capital allocation, sorted by strategic value score. |
| **Cut & Deferred** | Backlog of unselected initiatives for transparency, steering committees, and scenario replay. |
| **Full Master List** | Complete intake portfolio labeled with final selection status (`FUNDED` vs. `CUT`) and efficiency ratios. |

Design & Usability Highlights
* **Auto-Fitted Column Dimensions:** Column widths dynamically calculate against data length to prevent truncated values or text clipping.
* **Corporate Visual Hierarchy:** Formatted with bold navy headers (`#1F497D`), light-gray cell borders, and clean text/number alignments.
* **Gridlines Enabled:** Explicitly forces native spreadsheet gridlines on across all platforms.


**Quickstart**/**Prerequisites**
- Python 3.10+
- Virtual environment (`venv`)

1.) Clone & Set Up Environment

```bash
git clone [https://github.com/*INPUT_YOUR_USERNAME*/pmo-portfolio-optimizer.git](https://github.com/YOUR_USERNAME/pmo-portfolio-optimizer.git)
cd pmo-portfolio-optimizer
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2.) Run the Optimization Pipeline

Run with default constraints and the built-in sample dataset:

```bash
python main.py
```

3.) Run Custom Scenarios

Pass any custom CSV file, budget limit, or engineering capacity via CLI arguments:

```bash
# Evaluate a custom planning export with specific caps
python main.py --csv data/initiatives.csv --budget 600 --capacity 75

# Point to an external file from your downloads
python main.py --csv "/path/to/my_q4_intake.csv" --budget 450 --capacity 50
```

**Available CLI Options:**
* `--csv` (str): Path to your input `.csv` file *(default: `data/initiatives.csv`)*
* `--budget` (float): Total capital budget cap in $k *(default: `500.0`)*
* `--capacity` (int): Total engineering capacity in person-weeks *(default: `65`)*
* `--output` (str): Filepath for the exported Excel report *(default: `output/portfolio_results.xlsx`)*

**Running Automated Tests**
```bash
pytest -v
```

**Extending the Engine**

1.) Custom Strategic Weights: Update the StrategicWeights configuration in main.py to match your organization's quarterly priorities.\

2.) Third-Party Integrations: The modular Initiative dataclass accepts data ingested from Jira Software (via REST API), Linear, or CSV exports.

3.) Advanced Constraints: Additional constraints (e.g., minimum headcount guarantees per departmental pillar or dependency blocking relationships) can be added to src/optimizer.py as linear inequalities.

