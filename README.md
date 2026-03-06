# Cardiovascular Disease Prediction

## Project goal
Build a reproducible, end-to-end data science workflow that predicts the presence of cardiovascular disease (`disease`) from routine health and lifestyle features. The project is structured as such: data cleaning -> EDA -> modeling -> evaluation -> packaging and reporting.

## Why this project (business and public health motivation)
An imagined stakeholder is a regional health system (or payer/provider partnership) that wants to reduce preventable cardiovascular events by identifying higher-risk patients earlier.

How this can create value:
- **Clinical operations**: prioritize outreach (e.g., follow-ups, care management, reminders) for patients at higher predicted risk.
- **Population health**: inform targeted interventions for groups with elevated risk signals.
- **Resource allocation**: reduce avoidable admissions by focusing preventive resources where they matter most.
- **Public health impact**: earlier detection + behavior change support can reduce morbidity and long-term healthcare costs.

Important caveat: this dataset is observational and the model is not a medical device. Results here are for learning and prototyping, not clinical decision-making.

## Data source (Kaggle)
Dataset: Cardiovascular Disease Dataset on Kaggle  
https://www.kaggle.com/datasets/sulianova/cardiovascular-disease-dataset/data


### Local data files
- **Raw**: `data/cardio_train.csv` (downloaded from Kaggle; uses `;` as the separator)
- **Cleaned**: `data/cleaned_data.csv` (created by `notebooks/data_cleaning.ipynb`)

## Repository layout
- `README.md`: project overview + how to run + results
- `requirements.txt`: Python dependencies
- `learnings`: written rationale for the modeling flow (steps 1–8)
- `data/`
  - `cardio_train.csv` (raw, Kaggle)
  - `cleaned_data.csv` (cleaned + feature engineered)
- `notebooks/`
  - `data_cleaning.ipynb`: cleaning + feature engineering, writes `cleaned_data.csv`
  - `eda.ipynb`: exploratory analysis and hypothesis-driven checks
  - `model_building.ipynb`: leakage-safe modeling (CV + tuning + final test evaluation)

## How to run (recommended order)
### Quickstart
1) Create an environment and install dependencies:
- `python3 -m venv .venv`
- `source .venv/bin/activate`
- `python -m pip install -r requirements.txt`

If using XGBoost on macOS, install OpenMP runtime (one-time):
- `brew install libomp`

2) Get the dataset:
- Place `cardio_train.csv` into `data/` 

3) Run the notebooks:
- `jupyter lab`
- Execute in order:
  1. `notebooks/data_cleaning.ipynb`
  2. `notebooks/eda.ipynb`
  3. `notebooks/model_building.ipynb`

## Project stages
### 1) Data cleaning + feature engineering (`notebooks/data_cleaning.ipynb`)
Key transformations:
- Renames raw columns into readable names (e.g., `ap_hi` → `systolic blood pressure`)
- Maps coded categorical integers into human-readable categories (e.g., `cholesterol`, `glucose`)
- Converts `age` from days to years
- Filters impossible values (height/weight/blood pressure ranges)
- Engineers `bmi` and categorical `weight status`
- Removes exact duplicate rows
- Saves the result to `data/cleaned_data.csv`

### 2) EDA (`notebooks/eda.ipynb`)
What it covers:
- Distribution checks and target prevalence inspection
- Visual comparisons of features vs. target (`disease`)
- Basic hypothesis tests (e.g., Welch’s t-test, chi-square) and an odds ratio example
- Correlation heatmap for numeric features

### 3) Model building (`notebooks/model_building.ipynb`)
What it does:
- Creates a **stratified holdout test set** (used once at the end)
- Builds a leakage-safe preprocessing + modeling `Pipeline` using `ColumnTransformer`
- Compares baselines with **cross-validation on training only** (`StratifiedKFold`)
- Tunes hyperparameters (`GridSearchCV` / `RandomizedSearchCV`)
- Evaluates final performance on the holdout test set (ROC-AUC, PR-AUC, confusion matrix)

Leakage statement (explicit):
> All preprocessing steps were fit on the training data only and applied to validation/test sets.

The detailed “why” behind each modeling step is documented in `learnings`.

## Results summary (current)
Results include dataset/EDA summaries plus a baseline modeling run. Metrics can change slightly when re-running due to randomness and environment differences; random seeds are fixed where possible.

### Cleaned dataset snapshot
- Rows/columns: **64,899 × 14**
- Target prevalence (`disease=Yes`): **~50.9%**
- No missing values after cleaning (as saved in `data/cleaned_data.csv`)

### EDA highlights (descriptive)
Observed mean differences by `disease` label:
- Age: `Yes` ~ **54.93** vs `No` ~ **51.72**
- BMI: `Yes` ~ **28.57** vs `No` ~ **26.63**
- Systolic BP: `Yes` ~ **134.11** vs `No` ~ **119.60**
- Diastolic BP: `Yes` ~ **84.69** vs `No` ~ **78.09**

Observed proportional shifts (largest category differences, `Yes` minus `No`):
- Cholesterol: fewer `normal` and more `well above normal` in `Yes`
- Weight status: fewer `Healthy` and more `Obese` in `Yes`
- Physical activity: lower `Yes` and higher `No` in `Yes`

### Modeling (baseline run)
From `notebooks/model_building.ipynb` using a leakage-safe pipeline and a single holdout test set:
- Best baseline (by CV ROC-AUC): Logistic Regression
- Holdout test ROC-AUC: **~0.79**
- Holdout test PR-AUC: **~0.78**

## Assumptions, risks, and limitations
- **Not clinical-grade**: no external validation; no prospective evaluation; no calibration guarantee.
- **Observational confounding**: associations in EDA do not imply interventions will change outcomes.
- **Leakage control**: preprocessing and model selection are done via pipelines and CV on training only; the test set is used once.
- **Generalization**: dataset population may not match your target deployment population.

## Next improvements
High-value additions for a more production-like workflow:
- Calibration and reliability checks (Brier score, calibration curve)
- Threshold selection driven by a business/clinical constraint (e.g., minimum recall)
- Error analysis (false positives/false negatives) and model monitoring considerations
- Model-agnostic feature importance (permutation importance) and stronger interpretability


## Acknowledgements
- Sulianova (Kaggle): Cardiovascular Disease Dataset. https://www.kaggle.com/datasets/sulianova/cardiovascular-disease-dataset/data
