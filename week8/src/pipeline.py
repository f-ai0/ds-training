"""
Day 1 - EDA + Cleaning Pipeline
Run with:  python src/pipeline.py   (from the week8_project/ folder)

Goal: go from the raw punch-record spreadsheet (Practice_Dataset.xlsx) to a
single clean_dataset.csv with the features the model will train on,
in one reproducible run - no manual steps, no notebook cells.
"""
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

RAW_PATH = 'data/Practice_Dataset.xlsx'
CLEAN_PATH = 'data/clean_dataset.csv'

# IMPORTANT: punch_count and hours_worked are 0 on the SAME day an
# employee is absent - they are basically another encoding of the label,
# not a real predictor (you can't know today's punches before today
# happens). Using them directly caused 100% "accuracy" (data leakage).
# Instead we use HISTORICAL attendance pattern up to (not including) the
# current day - this is what "predict from attendance pattern" actually
# means, and it's what a supervisor could compute before the day starts.
NUMERIC = ['prior_absence_rate', 'prior_avg_hours', 'prior_records']
CATEGORICAL = ['position', 'day_of_week']
TARGET = 'is_absent'


def load_data(path=RAW_PATH):
    df = pd.read_excel(path)
    print(f'Loaded {df.shape[0]} rows, {df.shape[1]} columns')
    return df


def engineer_features(df):
    """Derive the modeling columns from the raw punch-record columns."""
    df = df.copy()

    # Target: ABSENT -> 1, PRESENT -> 0
    df['is_absent'] = (df['status'].str.upper() == 'ABSENT').astype(int)

    # Same-day hours worked - kept for reference/EDA only, NOT used as a
    # model feature (see leakage note above).
    in_t = pd.to_datetime(df['in_time'], format='%H:%M', errors='coerce')
    out_t = pd.to_datetime(df['out_time'], format='%H:%M', errors='coerce')
    hours = (out_t - in_t).dt.total_seconds() / 3600
    df['hours_worked'] = hours.fillna(0).clip(lower=0)

    df['work_date'] = pd.to_datetime(df['work_date'])
    df['day_of_week'] = df['work_date'].dt.day_name()

    # NOTE: Practice_Dataset.xlsx has no 'department' column, only
    # 'position'. The dashboard (Day 4) needs a department filter, so we
    # derive one with a simple position -> department mapping. This is
    # an ASSUMPTION, not real company data - call it out in the README.
    DEPARTMENT_MAP = {
        'ENGINEER': 'Operations', 'TECHNICIAN': 'Operations',
        'SUPERVISOR': 'Management', 'ADMINISTRATOR': 'Management',
        'ACCOUNTANT': 'Finance', 'CLERK': 'Finance',
        'DRIVER': 'Logistics', 'LABORER': 'Logistics',
    }
    df['department'] = df['position'].map(DEPARTMENT_MAP).fillna('Other')

    # Historical (lag) features per employee - computed from records
    # BEFORE the current row only, using each employee's chronological
    # order. This is the honest version of "attendance pattern".
    df = df.sort_values(['badge_number', 'work_date']).reset_index(drop=True)
    grp = df.groupby('badge_number')

    df['prior_records'] = grp.cumcount()
    cum_absences = grp['is_absent'].cumsum() - df['is_absent']
    cum_hours = grp['hours_worked'].cumsum() - df['hours_worked']

    prior_records_safe = df['prior_records'].replace(0, np.nan)
    df['prior_absence_rate'] = cum_absences / prior_records_safe
    df['prior_avg_hours'] = cum_hours / prior_records_safe
    # First-ever record for an employee has no history - imputer in the
    # preprocessing Pipeline (median/most_frequent) fills these NaNs.

    return df


def quick_eda(df):
    print('\n--- MISSING VALUES (raw columns) ---')
    print(df.isnull().sum()[df.isnull().sum() > 0])

    print('\n--- TARGET BALANCE (is_absent) ---')
    print(df[TARGET].value_counts(normalize=True).round(3))

    print('\n--- NUMERIC SUMMARY ---')
    print(df[NUMERIC].describe().round(2))

    print('\n--- ABSENCE RATE BY POSITION ---')
    print(df.groupby('position')[TARGET].mean().round(3).sort_values(ascending=False))

    print('\n--- ABSENCE RATE BY DAY OF WEEK ---')
    print(df.groupby('day_of_week')[TARGET].mean().round(3).sort_values(ascending=False))


def build_preprocessor():
    """Reused ColumnTransformer approach from Week 3."""
    numeric_pipe = Pipeline([
        ('impute', SimpleImputer(strategy='median')),
        ('scale', StandardScaler()),
    ])
    categorical_pipe = Pipeline([
        ('impute', SimpleImputer(strategy='most_frequent')),
        ('encode', OneHotEncoder(handle_unknown='ignore', sparse_output=False)),
    ])
    return ColumnTransformer([
        ('num', numeric_pipe, NUMERIC),
        ('cat', categorical_pipe, CATEGORICAL),
    ])


if __name__ == '__main__':
    df = load_data()
    df = engineer_features(df)
    quick_eda(df)

    keep_cols = ['badge_number', 'position', 'department', 'work_date',
                 'day_of_week', 'punch_count', 'hours_worked', 'status',
                 TARGET, 'prior_records', 'prior_absence_rate',
                 'prior_avg_hours']
    df[keep_cols].to_csv(CLEAN_PATH, index=False)
    print(f'\nSaved {CLEAN_PATH}')
