"""
Task 4.3 - Edge case tests for app.py, run with Streamlit's AppTest
(headless, no browser needed). Run with:  python tests/test_edge_cases.py
(from the week8_project/ folder)

Tests the 5 cases listed in the task sheet:
  1. Deselect every filter -> friendly warning, no crash
  2. Set all sliders to minimum -> still returns a prediction
  3. Set all sliders to maximum -> still returns a prediction
  4. Delete final_model.pkl -> clear instruction, not a traceback
  5. Resize the browser window -> layout still readable
"""
import os
import shutil
import streamlit as st
from streamlit.testing.v1 import AppTest

APP = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'app.py')
MODEL_PATH = 'models/final_model.pkl'
BACKUP_PATH = 'models/final_model.pkl.bak'

results = []


def check(name, condition):
    status = 'PASS' if condition else 'FAIL'
    results.append((name, status))
    print(f'[{status}] {name}')


# --- Case 1: deselect every filter ---------------------------------
at = AppTest.from_file(APP).run()
at.sidebar.multiselect[0].set_value([]).run()  # Department -> none selected
at.sidebar.multiselect[1].set_value([]).run()  # Position -> none selected
check('Case 1: empty filters -> no exception', len(at.exception) == 0)
check('Case 1: empty filters -> friendly warning shown', len(at.warning) > 0)

# --- Case 2: all sliders at minimum, then Predict -------------------
at = AppTest.from_file(APP).run()
for s in at.slider:
    s.set_value(s.min)
at.run()
at.button[0].click().run()
check('Case 2: min sliders + predict -> no exception', len(at.exception) == 0)
check('Case 2: min sliders + predict -> shows a result',
      len(at.success) > 0 or len(at.error) > 0)

# --- Case 3: all sliders at maximum, then Predict --------------------
at = AppTest.from_file(APP).run()
for s in at.slider:
    s.set_value(s.max)
at.run()
at.button[0].click().run()
check('Case 3: max sliders + predict -> no exception', len(at.exception) == 0)
check('Case 3: max sliders + predict -> shows a result',
      len(at.success) > 0 or len(at.error) > 0)

# --- Case 4: model file missing --------------------------------------
# @st.cache_resource persists across AppTest runs in this same process
# (Cases 1-3 already cached a loaded model) - clear it first, otherwise
# this case would false-pass by serving the cached model instead of
# actually re-checking the file on disk.
st.cache_resource.clear()
shutil.move(MODEL_PATH, BACKUP_PATH)
try:
    at = AppTest.from_file(APP).run()
    # st.stop() inside a cached loader still surfaces as a clean stop,
    # not a Python exception - and the error message must be visible.
    check('Case 4: missing model -> no raw traceback (no exception)', len(at.exception) == 0)
    check('Case 4: missing model -> clear error message shown',
          any('Model file not found' in e.value for e in at.error))
finally:
    shutil.move(BACKUP_PATH, MODEL_PATH)

# --- Case 5: layout responsiveness (not testable headlessly) --------
# AppTest has no browser/viewport, so window resizing can't be
# simulated here. Verified instead by code review: st.set_page_config
# uses layout='wide', every chart/dataframe/table call passes
# use_container_width=True, and KPI cards use st.columns() - all of
# which reflow with the browser width rather than using fixed pixel
# widths. Confirm manually in-browser before the presentation.
results.append(('Case 5: responsive layout (manual browser check required)', 'MANUAL'))
print('[MANUAL] Case 5: responsive layout - verify by resizing the browser window yourself')

print('\n--- SUMMARY ---')
for name, status in results:
    print(f'{status:8s} {name}')

failed = [r for r in results if r[1] == 'FAIL']
if failed:
    raise SystemExit(f'{len(failed)} edge case(s) failed')
print('\nAll automated edge cases passed.')
