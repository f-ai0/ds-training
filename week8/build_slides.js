const pptxgen = require("pptxgenjs");

const NAVY = "21295C";
const DEEPBLUE = "065A82";
const TEAL = "1C7293";
const ICE = "CADCFC";
const WHITE = "FFFFFF";
const OFFWHITE = "F4F7FA";
const CORAL = "F96167";
const DARKTEXT = "1B2733";
const MUTED = "5C6B7A";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.3 x 7.5

function titleBar(slide, text, color) {
  slide.addText(text, {
    x: 0.6, y: 0.45, w: 12.1, h: 0.9,
    fontFace: "Cambria", fontSize: 30, bold: true,
    color: color || DARKTEXT, align: "left",
  });
}

function pageNum(slide, n, color) {
  slide.addText(String(n), {
    x: 12.6, y: 7.05, w: 0.5, h: 0.35,
    fontFace: "Calibri", fontSize: 10, color: color || MUTED, align: "right",
  });
}

function statCard(slide, x, y, w, h, num, label) {
  slide.addShape(pres.ShapeType.roundRect, {
    x, y, w, h, rectRadius: 0.12,
    fill: { color: OFFWHITE }, line: { type: "none" },
    shadow: { type: "outer", color: "9AA7B4", opacity: 0.25, blur: 6, offset: 2, angle: 90 },
  });
  slide.addText(num, { x: x + 0.25, y: y, w: w * 0.42, h, fontFace: "Cambria", fontSize: 34, bold: true, color: DEEPBLUE, valign: "middle" });
  slide.addText(label, { x: x + w * 0.44, y: y, w: w * 0.53, h, fontFace: "Calibri", fontSize: 12.5, color: MUTED, valign: "middle" });
}

// ================================================================ Slide 1 - Title
{
  const s = pres.addSlide();
  s.background = { color: NAVY };
  s.addShape(pres.ShapeType.ellipse, { x: 9.6, y: -2.2, w: 7, h: 7, fill: { color: DEEPBLUE, transparency: 55 }, line: { type: "none" } });
  s.addShape(pres.ShapeType.ellipse, { x: 11.4, y: 4.6, w: 4.2, h: 4.2, fill: { color: TEAL, transparency: 45 }, line: { type: "none" } });
  s.addText("WEEK 8  ·  CAPSTONE PROJECT", { x: 0.9, y: 2.05, w: 8, h: 0.4, fontFace: "Calibri", fontSize: 14, color: ICE, charSpacing: 3, bold: true });
  s.addText("Employee Attendance\nPredictor", { x: 0.85, y: 2.5, w: 9.8, h: 2.2, fontFace: "Cambria", fontSize: 44, bold: true, color: WHITE, lineSpacingMultiple: 1.05 });
  s.addText("Predicting absence risk from historical attendance patterns, with a live dashboard for supervisors.", { x: 0.9, y: 4.75, w: 8.2, h: 0.8, fontFace: "Calibri", fontSize: 16, color: ICE });
  s.addText("Data Science & Machine Learning Co-Op Training", { x: 0.9, y: 6.6, w: 8, h: 0.4, fontFace: "Calibri", fontSize: 12, color: ICE, italic: true });
  s.addNotes("Open with energy: 'Our attendance data sits in a spreadsheet nobody looks at until it's a problem. I built something that changes that.' Then move to the problem slide.");
}

// ================================================================ Slide 2 - Problem
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  titleBar(s, "The Problem");
  s.addText(
    "Supervisors can't easily tell who is at risk of being absent. The attendance data exists — it just sits in a spreadsheet nobody analyzes until after the fact.",
    { x: 0.6, y: 1.5, w: 6.6, h: 1.7, fontFace: "Calibri", fontSize: 16, color: DARKTEXT, lineSpacingMultiple: 1.3 }
  );
  s.addText("Who it affects", { x: 0.6, y: 3.35, w: 6, h: 0.4, fontFace: "Calibri", fontSize: 14, bold: true, color: TEAL });
  const rows = [
    ["Site supervisors", "need to plan coverage before a shift, not after"],
    ["HR staff", "need trends across positions, not a raw punch log"],
  ];
  let y = 3.85;
  rows.forEach(([h, d]) => {
    s.addShape(pres.ShapeType.ellipse, { x: 0.6, y: y + 0.06, w: 0.13, h: 0.13, fill: { color: CORAL }, line: { type: "none" } });
    s.addText([{ text: h + "  ", options: { bold: true, color: DARKTEXT } }, { text: d, options: { color: MUTED } }],
      { x: 0.9, y: y - 0.1, w: 6.2, h: 0.5, fontFace: "Calibri", fontSize: 14 });
    y += 0.62;
  });
  statCard(s, 7.7, 1.5, 4.9, 1.25, "30", "employees tracked");
  statCard(s, 7.7, 2.95, 4.9, 1.25, "16", "days of raw punch data");
  statCard(s, 7.7, 4.4, 4.9, 1.25, "9.7%", "of work-days end in an absence");
  s.addText(
    "Target: predict is_absent from attendance pattern. Suggested by the training plan — confirm your final problem choice with your supervisor.",
    { x: 0.6, y: 6.6, w: 12, h: 0.5, fontFace: "Calibri", fontSize: 11, italic: true, color: MUTED }
  );
  pageNum(s, 2);
  s.addNotes("Keep this non-technical. No model talk yet — just the business problem and who feels it.");
}

// ================================================================ Slide 3 - Approach
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  titleBar(s, "The Approach");
  s.addText("Data → Cleaning → Modeling → App, in one reproducible pipeline.", { x: 0.6, y: 1.35, w: 12, h: 0.5, fontFace: "Calibri", fontSize: 15, color: MUTED });

  const steps = [
    ["1", "Raw Data", "360 punch records\nfor 30 employees", DEEPBLUE],
    ["2", "Clean & Engineer", "Historical features only\n(no same-day leakage)", TEAL],
    ["3", "Model & Tune", "Baseline → compare →\nGridSearchCV", DEEPBLUE],
    ["4", "App & Dashboard", "Streamlit prediction +\nlive KPIs", TEAL],
  ];
  const boxW = 2.75, gap = 0.35, startX = 0.6, y = 2.5, h = 2.7;
  steps.forEach((step, i) => {
    const x = startX + i * (boxW + gap);
    s.addShape(pres.ShapeType.roundRect, { x, y, w: boxW, h, rectRadius: 0.12, fill: { color: OFFWHITE }, line: { type: "none" },
      shadow: { type: "outer", color: "9AA7B4", opacity: 0.22, blur: 6, offset: 2, angle: 90 } });
    s.addShape(pres.ShapeType.ellipse, { x: x + boxW / 2 - 0.35, y: y + 0.35, w: 0.7, h: 0.7, fill: { color: step[3] }, line: { type: "none" } });
    s.addText(step[0], { x: x + boxW / 2 - 0.35, y: y + 0.35, w: 0.7, h: 0.7, fontFace: "Cambria", fontSize: 22, bold: true, color: WHITE, align: "center", valign: "middle" });
    s.addText(step[1], { x: x + 0.15, y: y + 1.2, w: boxW - 0.3, h: 0.5, fontFace: "Calibri", fontSize: 15, bold: true, color: DARKTEXT, align: "center" });
    s.addText(step[2], { x: x + 0.15, y: y + 1.7, w: boxW - 0.3, h: 0.85, fontFace: "Calibri", fontSize: 11.5, color: MUTED, align: "center", lineSpacingMultiple: 1.2 });
    if (i < steps.length - 1) {
      s.addText("→", { x: x + boxW, y: y + h / 2 - 0.35, w: gap, h: 0.7, fontFace: "Calibri", fontSize: 24, bold: true, color: CORAL, align: "center", valign: "middle" });
    }
  });

  s.addText(
    "Key decision: predict from an employee's PAST attendance pattern, not same-day punch data — that's what makes the prediction usable before the day happens.",
    { x: 0.6, y: 5.75, w: 12, h: 0.7, fontFace: "Calibri", fontSize: 13, italic: true, color: TEAL, lineSpacingMultiple: 1.25 }
  );
  pageNum(s, 3);
  s.addNotes("One slide, one diagram — walk left to right across the four boxes in under a minute.");
}

// ================================================================ Slide 4 - Live Demo
{
  const s = pres.addSlide();
  s.background = { color: NAVY };
  s.addShape(pres.ShapeType.ellipse, { x: -2.5, y: 3.2, w: 6, h: 6, fill: { color: DEEPBLUE, transparency: 55 }, line: { type: "none" } });
  s.addText("LIVE DEMO", { x: 0.9, y: 0.9, w: 8, h: 0.4, fontFace: "Calibri", fontSize: 14, color: ICE, charSpacing: 3, bold: true });
  s.addText("Show, don't tell", { x: 0.85, y: 1.3, w: 10, h: 1.2, fontFace: "Cambria", fontSize: 38, bold: true, color: WHITE });
  s.addText("Have the app already running before you start talking.", { x: 0.9, y: 2.45, w: 9, h: 0.5, fontFace: "Calibri", fontSize: 15, color: ICE, italic: true });

  const items = [
    "Make a live prediction — show the probability, not just the label",
    "Explain the top drivers on the feature-importance chart",
    "Filter the dashboard by department and position",
    "Show a KPI card update live as filters change",
  ];
  let y = 3.4;
  items.forEach((t, i) => {
    s.addShape(pres.ShapeType.roundRect, { x: 0.9, y, w: 0.42, h: 0.42, rectRadius: 0.08, fill: { color: TEAL }, line: { type: "none" } });
    s.addText(String(i + 1), { x: 0.9, y, w: 0.42, h: 0.42, fontFace: "Calibri", fontSize: 15, bold: true, color: WHITE, align: "center", valign: "middle" });
    s.addText(t, { x: 1.5, y: y - 0.05, w: 10.5, h: 0.55, fontFace: "Calibri", fontSize: 15, color: WHITE, valign: "middle" });
    y += 0.75;
  });
  pageNum(s, 4, ICE);
  s.addNotes("4 minutes. Run the app, make a prediction, walk the feature-importance chart, then filter the dashboard live. Practice this transition twice before presenting.");
}

// ================================================================ Slide 5 - Results
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  titleBar(s, "Results");
  s.addText("Baseline vs. tuned model, on data with no same-day leakage.", { x: 0.6, y: 1.35, w: 12, h: 0.5, fontFace: "Calibri", fontSize: 15, color: MUTED });

  const tableRows = [
    [
      { text: "Model", options: { bold: true, color: WHITE, fill: { color: DEEPBLUE } } },
      { text: "CV F1", options: { bold: true, color: WHITE, fill: { color: DEEPBLUE } } },
      { text: "Test F1", options: { bold: true, color: WHITE, fill: { color: DEEPBLUE } } },
      { text: "Test AUC", options: { bold: true, color: WHITE, fill: { color: DEEPBLUE } } },
    ],
    [
      { text: "Baseline (majority class)" }, { text: "—" }, { text: "0.00" }, { text: "0.50" },
    ],
    [
      { text: "Random Forest" }, { text: "0.000" }, { text: "—" }, { text: "—" },
    ],
    [
      { text: "Logistic Regression (tuned)", options: { bold: true, fill: { color: ICE } } },
      { text: "0.194", options: { bold: true, fill: { color: ICE } } },
      { text: "0.21", options: { bold: true, fill: { color: ICE } } },
      { text: "0.55", options: { bold: true, fill: { color: ICE } } },
    ],
  ];
  s.addTable(tableRows, {
    x: 0.6, y: 2.05, w: 7.6, h: 2.0,
    fontFace: "Calibri", fontSize: 13, color: DARKTEXT, border: { type: "solid", color: "DCE3EA", pt: 1 },
    autoPage: false, valign: "middle",
  });

  statCard(s, 8.6, 2.05, 4.0, 1.0, "90.3%", "baseline accuracy — but misleading (F1 = 0)");
  statCard(s, 8.6, 3.2, 4.0, 1.0, "0.55", "tuned model Test AUC — a real, small lift");

  s.addShape(pres.ShapeType.roundRect, { x: 0.6, y: 4.5, w: 12.0, h: 1.85, rectRadius: 0.1, fill: { color: OFFWHITE }, line: { type: "none" } });
  s.addText("What the numbers mean in practice", { x: 0.9, y: 4.68, w: 11.4, h: 0.4, fontFace: "Calibri", fontSize: 13, bold: true, color: TEAL });
  s.addText(
    "The first version of this model scored 100% — that was data leakage (punch data from the SAME day as the absence). After fixing it to use only prior history, the honest result is a small lift over guessing (AUC 0.55). With only 360 records across 30 employees, that's expected — the model's direction is right, its ceiling is data volume, not the approach.",
    { x: 0.9, y: 5.08, w: 11.4, h: 1.2, fontFace: "Calibri", fontSize: 12.5, color: DARKTEXT, lineSpacingMultiple: 1.28 }
  );
  pageNum(s, 5);
  s.addNotes("Lead with the leakage story — it shows judgment, not just a score. Then give the honest AUC and explain why it's still the right deliverable.");
}

// ================================================================ Slide 6 - What I Learned
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  titleBar(s, "What I Learned");

  s.addShape(pres.ShapeType.roundRect, { x: 0.6, y: 1.55, w: 5.9, h: 4.9, rectRadius: 0.12, fill: { color: OFFWHITE }, line: { type: "none" },
    shadow: { type: "outer", color: "9AA7B4", opacity: 0.22, blur: 6, offset: 2, angle: 90 } });
  s.addText("Biggest challenge", { x: 0.95, y: 1.85, w: 5.2, h: 0.4, fontFace: "Calibri", fontSize: 15, bold: true, color: DEEPBLUE });
  s.addText(
    "A 100% accuracy score looked like success — it was actually data leakage. punch_count and hours_worked are 0 by construction on an absence day, so the model was reading the label off itself, not predicting anything.",
    { x: 0.95, y: 2.35, w: 5.2, h: 1.7, fontFace: "Calibri", fontSize: 13.5, color: DARKTEXT, lineSpacingMultiple: 1.3 }
  );
  s.addText("How I solved it", { x: 0.95, y: 4.1, w: 5.2, h: 0.4, fontFace: "Calibri", fontSize: 15, bold: true, color: DEEPBLUE });
  s.addText(
    "Rebuilt the features around each employee's PRIOR history only (past absence rate, past average hours) — the same information a supervisor would actually have before the day starts.",
    { x: 0.95, y: 4.6, w: 5.2, h: 1.7, fontFace: "Calibri", fontSize: 13.5, color: DARKTEXT, lineSpacingMultiple: 1.3 }
  );

  s.addShape(pres.ShapeType.roundRect, { x: 6.8, y: 1.55, w: 5.9, h: 4.9, rectRadius: 0.12, fill: { color: NAVY }, line: { type: "none" } });
  s.addText("What I'd do differently", { x: 7.15, y: 1.85, w: 5.2, h: 0.4, fontFace: "Calibri", fontSize: 15, bold: true, color: ICE });
  const items = [
    "Collect more history per employee before modeling — 16 days isn't enough to learn a real pattern",
    "Add real department data instead of deriving it from position",
    "Track a rolling window (last 5 days), not just all-time history",
  ];
  let y = 2.4;
  items.forEach((t) => {
    s.addShape(pres.ShapeType.ellipse, { x: 7.15, y: y + 0.08, w: 0.1, h: 0.1, fill: { color: CORAL }, line: { type: "none" } });
    s.addText(t, { x: 7.45, y: y - 0.12, w: 5.05, h: 0.85, fontFace: "Calibri", fontSize: 13.5, color: WHITE, lineSpacingMultiple: 1.25 });
    y += 1.0;
  });
  pageNum(s, 6);
  s.addNotes("Two minutes. Be specific about the leakage story again briefly, then pivot fast to forward-looking improvements.");
}

// ================================================================ Slide 7 - Anticipated Questions
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  titleBar(s, "Questions — Prepared Answers");

  const qa = [
    ["How accurate is it really?", "AUC 0.55 on held-out test data — a small, honest lift over the 0.50 random baseline. Not production-strong yet; the pipeline and process are the deliverable."],
    ["What happens if the data changes?", "src/pipeline.py re-derives every feature from raw punches — re-run it and src/train.py, and the model retrains on the new data automatically."],
    ["Could this work for a different department?", "Yes — department is a filter, not a separate model. It would need more historical rows per employee first."],
    ["Why this model over others?", "Logistic Regression beat Random Forest on cross-validated F1 (0.194 vs 0.000) — Random Forest never learned the minority class with this little absence data."],
    ["What would you build next with more time?", "More weeks of history, a rolling-window feature, and re-testing whether a tree model catches up once there's more signal."],
  ];
  let y = 1.5;
  qa.forEach(([q, a]) => {
    s.addShape(pres.ShapeType.roundRect, { x: 0.6, y, w: 12.0, h: 1.0, rectRadius: 0.08, fill: { color: OFFWHITE }, line: { type: "none" } });
    s.addText(q, { x: 0.85, y: y + 0.08, w: 11.5, h: 0.35, fontFace: "Calibri", fontSize: 13, bold: true, color: TEAL });
    s.addText(a, { x: 0.85, y: y + 0.42, w: 11.5, h: 0.52, fontFace: "Calibri", fontSize: 11.5, color: DARKTEXT, lineSpacingMultiple: 1.1 });
    y += 1.1;
  });
  pageNum(s, 7);
  s.addNotes("Practice saying each answer out loud once before presenting — don't read this slide verbatim live.");
}

// ================================================================ Slide 8 - Thank you
{
  const s = pres.addSlide();
  s.background = { color: NAVY };
  s.addShape(pres.ShapeType.ellipse, { x: 9.6, y: -2.2, w: 7, h: 7, fill: { color: DEEPBLUE, transparency: 55 }, line: { type: "none" } });
  s.addText("Thank You", { x: 0.9, y: 2.7, w: 10, h: 1.2, fontFace: "Cambria", fontSize: 44, bold: true, color: WHITE });
  s.addText("Questions & discussion", { x: 0.95, y: 3.75, w: 10, h: 0.6, fontFace: "Calibri", fontSize: 18, color: ICE });
  s.addText("Employee Attendance Predictor  ·  Week 8 Capstone", { x: 0.95, y: 6.6, w: 10, h: 0.4, fontFace: "Calibri", fontSize: 12, color: ICE, italic: true });
  pageNum(s, 8, ICE);
}

pres.writeFile({ fileName: "presentation.pptx" }).then(() => console.log("done"));
