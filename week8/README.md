# Employee Attendance Predictor

Predicts employee absence risk from historical attendance patterns and provides an interactive dashboard for supervisors.

## Problem

Supervisors cannot easily tell which employees are at risk of absence, and attendance data sits in a raw punch-record spreadsheet nobody analyzes. This project predicts whether an employee is likely to be absent, based on their attendance history, and gives supervisors a dashboard to explore trends and run predictions on demand. It's built for site supervisors and HR staff — non-technical users, no code required.

## Setup

```bash
pip install -r requirements.txt
python src/pipeline.py     # clean the raw data, engineer features
python src/train.py        # train, compare, tune, and export the model
streamlit run app.py       # launch the app (opens at http://localhost:8501)
```

Tested from a clean virtual environment end to end — all three steps run without manual edits.

## Results

360 attendance records, 30 employees, 16 work days. Target (`is_absent`) is imbalanced: ~9.7% absent.

| Model                       | CV F1  | Test F1 | Test AUC |
|------------------------------|--------|---------|----------|
| Baseline (majority class)    | ---    | 0.00    | 0.50     |
| Logistic Regression           | 0.165  | ---     | ---      |
| Random Forest                 | 0.000  | ---     | ---      |
| Logistic Regression (tuned, C=0.1) | 0.194 | 0.21 | 0.55 |

Logistic Regression was chosen because it clearly beat Random Forest on cross-validated F1 — Random Forest never learned to flag the minority (absent) class at all with this little data. The baseline's 90% accuracy is misleading here (it's just always guessing "present"), which is exactly why F1/AUC on the absent class are tracked instead of accuracy alone.

## Project Structure

```
week8_project/
  data/
      Practice_Dataset.xlsx        # raw input
      clean_dataset.csv            # produced by pipeline.py
  models/
      final_model.pkl              # full pipeline: preprocessing + model
  src/
      pipeline.py                  # EDA + cleaning + feature engineering
      train.py                     # baseline, model comparison, tuning
  tests/
      test_edge_cases.py           # automated Streamlit edge-case tests
  app.py                           # Streamlit prediction app + dashboard
  presentation.pptx                # slides for the Day 5 presentation
  build_slides.js                  # regenerates presentation.pptx (pptxgenjs)
  requirements.txt
  problem_statement.txt
  model_comparison.csv
  .gitignore
  README.md
```

## Limitations

- **Small dataset**: trained on 360 records for 30 employees over just 16 days. Performance on a larger, real population is unverified, and most employees have very little history to learn from yet.
- **Weak predictive signal**: after removing data leakage (see below), the tuned model only slightly beats random guessing (Test AUC 0.55). This is an honest result, not a bug — flagging it rather than hiding it.
- **Data leakage was found and fixed on Day 2**: the raw `punch_count` and `hours_worked` columns are 0 by construction on the same day an employee is absent, so using them as predictors produced a fake 100% accuracy. The final model instead uses only *historical* features (each employee's prior absence rate, prior average hours, and record count, computed using only days before the one being predicted).
- **`department` is not in the source data.** The dataset only has `position`, so `department` was derived with a simple position → department mapping (see `src/pipeline.py`) purely so the dashboard could have a department filter. It is an assumption, not real company data — confirm with a supervisor before relying on it.
- No real-time integration with the badge system, and this predicts same-day absence risk, not future absence dates (both explicitly out of scope — see `problem_statement.txt`).

## Author

[Your name] — Data Science Co-Op

*(Fill in your name/company before submitting — left blank since I don't have that info.)*
