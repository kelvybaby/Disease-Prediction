# Cardiovascular Disease Prediction

## Project goal
Build a reproducible, end-to-end data science workflow that predicts the presence of cardiovascular disease (`disease`) from routine health and lifestyle features. The project is structured as a realistic DS deliverable: data cleaning → EDA → modeling → evaluation → (future) packaging and reporting.

## Why this project (business + public health motivation)
An imagined stakeholder is a regional health system (or payer/provider partnership) that wants to reduce preventable cardiovascular events by identifying higher-risk patients earlier.

How this can create value:
- **Clinical operations**: prioritize outreach (e.g., follow-ups, care management, reminders) for patients at higher predicted risk.
- **Population health**: inform targeted interventions for groups with elevated risk signals.
- **Resource allocation**: reduce avoidable admissions by focusing preventive resources where they matter most.
- **Public health impact**: earlier detection + behavior change support can reduce morbidity and long-term healthcare costs.

Important caveat: this dataset is observational and the model is **not** a medical device. Results here are for learning and prototyping, not clinical decision-making.

## Data source (Kaggle)
Dataset: Cardiovascular Disease Dataset on Kaggle  
https://www.kaggle.com/datasets/sulianova/cardiovascular-disease-dataset/data


### Local data files
- **Raw**: `data/cardio_train.csv` (downloaded from Kaggle; uses `;` as the separator)
- **Derived**: `data/cleaned_data.csv` (created by `notebooks/data_cleaning.ipynb`)

## Repository layout
- `data/`
  - `cardio_train.csv` (raw, Kaggle)
  - `cleaned_data.csv` (cleaned + feature engineered)
- `notebooks/`
  - `data_cleaning.ipynb`: cleaning + feature engineering, writes `cleaned_data.csv`
  - `eda.ipynb`: exploratory analysis and hypothesis-driven checks
  - `model_building.ipynb`: preprocessing + model training (in progress)

## How to run (recommended order)
### Quickstart
1) Create an environment and install dependencies:
- `python3 -m venv .venv`
- `source .venv/bin/activate`
- `python -m pip install -r requirements.txt`

2) Get the dataset:
- Place `cardio_train.csv` into `data/` (downloaded from Kaggle), or use Kaggle CLI:
  - `kaggle datasets download -d sulianova/cardiovascular-disease-dataset -p data/`
  - `unzip -o data/cardiovascular-disease-dataset.zip -d data/`

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
- Filters implausible values (height/weight/blood pressure ranges)
- Engineers `bmi` and categorical `weight status`
- Removes exact duplicate rows
- Saves the result to `data/cleaned_data.csv`

### 2) EDA (`notebooks/eda.ipynb`)
What it covers:
- Distribution checks and target prevalence inspection
- Visual comparisons of features vs. target (`disease`)
- Basic hypothesis tests (e.g., Welch’s t-test, chi-square) and an odds ratio example
- Correlation heatmap for numeric features

### 3) Model building (in progress) (`notebooks/model_building.ipynb`)
Implemented so far:
- Train/validation/test splitting with stratification
- A `ColumnTransformer` design:
  - numeric scaling (RobustScaler)
  - ordinal encoding (ordered categories for `cholesterol`, `glucose`, `weight status`)
  - one-hot encoding for nominal features

Planned next steps (skeleton):
- [ ] Build an end-to-end `Pipeline(preprocessor → model)` to prevent leakage
- [ ] Establish baselines:
  - [ ] Logistic Regression
  - [ ] Random Forest
- [ ] Model selection via cross-validation (e.g., `StratifiedKFold`)
- [ ] Evaluate on holdout test set with:
  - [ ] ROC-AUC and PR-AUC
  - [ ] confusion matrix at an operating threshold
  - [ ] calibration (probability quality)
- [ ] Hyperparameter tuning (grid/random search)
- [ ] Interpretability:
  - [ ] coefficient inspection (logistic regression)
  - [ ] permutation importance / tree-based importances
- [ ] Save artifacts (model, metrics, plots) for reproducibility

## Results summary (current)
Modeling results are not finalized yet. Current results are descriptive from the cleaned dataset and EDA.

### Cleaned dataset snapshot
- Rows/columns: **64,899 × 14**
- Target prevalence (`disease=Yes`): **~50.9%**
- No missing values after cleaning (as saved in `data/cleaned_data.csv`)

### EDA highlights (descriptive, not causal)
Observed mean differences by `disease` label:
- Age: `Yes` ~ **54.93** vs `No` ~ **51.72**
- BMI: `Yes` ~ **28.57** vs `No` ~ **26.63**
- Systolic BP: `Yes` ~ **134.11** vs `No` ~ **119.60**
- Diastolic BP: `Yes` ~ **84.69** vs `No` ~ **78.09**

Observed proportional shifts (largest category differences, `Yes` minus `No`):
- Cholesterol: fewer `normal` and more `well above normal` in `Yes`
- Weight status: fewer `Healthy` and more `Obese` in `Yes`
- Physical activity: lower `Yes` and higher `No` in `Yes`

## Assumptions, risks, and limitations
- **Not clinical-grade**: no external validation; no prospective evaluation; no calibration guarantee.
- **Observational confounding**: associations in EDA do not imply interventions will change outcomes.
- **Potential leakage risk**: feature selection and hyperparameter tuning must be done inside CV/pipelines (planned).
- **Generalization**: dataset population may not match your target deployment population.

## Production-ready README additions
Common additions in production data science repositories:
- Environment specification (`requirements.txt` / `environment.yml`) and exact run commands
- Reproducibility details (random seeds, artifact locations, deterministic data versions)
- Results table with model metrics (and confidence intervals when appropriate)
- Model card (intended use, non-goals, fairness considerations, monitoring plan)
- Repository hygiene (`.gitignore`, no committed virtualenv/IDE files, controlled outputs)

## Acknowledgements
- Sulianova (Kaggle): Cardiovascular Disease Dataset. https://www.kaggle.com/datasets/sulianova/cardiovascular-disease-dataset/data
