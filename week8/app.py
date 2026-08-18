"""
Employee Attendance Predictor - Streamlit app (Days 3-4)
Run with:  streamlit run app.py   (from the week8_project/ folder)
"""
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px

st.set_page_config(page_title='Attendance Predictor', layout='wide')

MODEL_PATH = 'models/final_model.pkl'
DATA_PATH = 'data/clean_dataset.csv'


# ---------------------------------------------------------------------
# Task 4.3 - load model with a clear message instead of a stack trace
# if it's missing (edge case: "delete final_model.pkl")
# ---------------------------------------------------------------------
@st.cache_resource
def load_model():
    try:
        return joblib.load(MODEL_PATH)
    except FileNotFoundError:
        st.error(f"Model file not found at '{MODEL_PATH}'. Run: python src/train.py")
        st.stop()


@st.cache_data
def load_data():
    try:
        return pd.read_csv(DATA_PATH)
    except FileNotFoundError:
        st.error(f"Data file not found at '{DATA_PATH}'. Run: python src/pipeline.py")
        st.stop()


model = load_model()
df = load_data()

st.title('Employee Attendance Predictor')
st.caption('Predicts absence risk from HISTORICAL attendance patterns (not same-day data).')

# =======================================================================
# Task 3.2 - Prediction interface
# Inputs match the model's actual features: position, day_of_week,
# prior_absence_rate, prior_avg_hours, prior_records. (No punch_count /
# hours_worked here on purpose - those are same-day outcomes the model
# was NOT trained on, to avoid the leakage found on Day 2.)
# =======================================================================
st.header('Make a Prediction')
st.caption("Enter an employee's attendance history up to today to estimate today's absence risk.")

col1, col2 = st.columns(2)
with col1:
    position = st.selectbox('Position', sorted(df['position'].dropna().unique()))
    day_of_week = st.selectbox(
        'Day of week',
        ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
    )
    prior_records = st.slider('Prior work-day records on file', 0, 30, 5)
with col2:
    prior_absence_rate = st.slider('Prior absence rate (0.0-1.0)', 0.0, 1.0, 0.1, step=0.01)
    prior_avg_hours = st.slider('Prior average hours worked/day', 0.0, 12.0, 8.0, step=0.25)

if st.button('Predict', type='primary'):
    input_df = pd.DataFrame([{
        'position': position,
        'day_of_week': day_of_week,
        'prior_absence_rate': prior_absence_rate,
        'prior_avg_hours': prior_avg_hours,
        'prior_records': prior_records,
    }])

    # Task 4.3 - guard the prediction call itself
    try:
        pred = model.predict(input_df)[0]
        proba = model.predict_proba(input_df)[0][1]
    except Exception as e:
        st.error(f'Prediction failed: {e}')
        st.stop()

    if pred == 1:
        st.error(f'HIGH absence risk — probability {proba:.1%}')
    else:
        st.success(f'LOW absence risk — probability {proba:.1%}')
    st.progress(float(proba))

# =======================================================================
# Task 3.3 - Feature importance / "what drives the prediction"
# The winning model is Logistic Regression (not a tree model), so we
# pull |coefficients| instead of .feature_importances_ - this handles
# either model type generically.
# =======================================================================
st.header('What Drives the Prediction?')

clf = model.named_steps['model']
prep = model.named_steps['prep']
feature_names = prep.get_feature_names_out()

if hasattr(clf, 'feature_importances_'):
    importance = clf.feature_importances_
elif hasattr(clf, 'coef_'):
    importance = np.abs(clf.coef_[0])
else:
    importance = None

if importance is not None:
    importance_df = pd.DataFrame({
        'feature': feature_names,
        'importance': importance,
    }).sort_values('importance', ascending=False).head(10)
    st.bar_chart(importance_df.set_index('feature'))
    st.caption('Top 10 features the model relies on most (absolute logistic-regression '
               'coefficient magnitude - larger = bigger effect on absence risk).')
else:
    st.info('This model type does not expose feature importances.')

# =======================================================================
# Task 4.1 - KPI cards & filters
# =======================================================================
st.header('Attendance Dashboard')

st.sidebar.header('Filters')
dept_options = sorted(df['department'].dropna().unique())
pos_options = sorted(df['position'].dropna().unique())
dept_filter = st.sidebar.multiselect('Department', options=dept_options, default=dept_options)
pos_filter = st.sidebar.multiselect('Position', options=pos_options, default=pos_options)

filtered = df[df['department'].isin(dept_filter) & df['position'].isin(pos_filter)]

# Task 4.1 / edge case - empty filter selection must not crash the app
if filtered.empty:
    st.warning('No records match these filters. Widen your selection in the sidebar.')
    st.stop()

c1, c2, c3, c4 = st.columns(4)
c1.metric('Total Records', len(filtered))
c2.metric('Unique Employees', filtered['badge_number'].nunique())
c3.metric('Absence Rate', f"{filtered['is_absent'].mean():.1%}")
c4.metric('Avg Hours Worked', f"{filtered['hours_worked'].mean():.1f}")

# =======================================================================
# Task 4.2 - Interactive charts in tabs + CSV download
# =======================================================================
tab1, tab2, tab3 = st.tabs(['By Department', 'Distributions', 'Raw Data'])

with tab1:
    dept_stats = filtered.groupby('department').agg(
        absence_rate=('is_absent', 'mean'),
        avg_hours=('hours_worked', 'mean'),
        headcount=('badge_number', 'nunique'),
    ).reset_index()
    fig = px.bar(dept_stats, x='department', y='absence_rate',
                 title='Absence Rate by Department',
                 color='absence_rate', color_continuous_scale='Teal')
    st.plotly_chart(fig, width='stretch')
    st.dataframe(dept_stats, width='stretch')

with tab2:
    col = st.selectbox('Column', ['punch_count', 'hours_worked',
                                   'prior_absence_rate', 'prior_avg_hours'])
    fig2 = px.histogram(filtered, x=col, color='status', marginal='box',
                         title=f'Distribution of {col}')
    st.plotly_chart(fig2, width='stretch')

with tab3:
    st.dataframe(filtered, width='stretch')
    st.download_button('Download filtered data (CSV)',
                        filtered.to_csv(index=False),
                        'filtered_attendance.csv', 'text/csv')
