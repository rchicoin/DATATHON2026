// Stream C slides 7-8 (repairs). Build: npm i pptxgenjs, set APPLY_THEME to the pptx skill's scripts/apply_theme.js, then node slides/build_c_slides.js
// Numbers come from results/c_repairs/findings.md (C-1, C-2, C-3).
const path = require("path");
const pptxgen = require(process.env.PPTXGENJS || "pptxgenjs");
const { applyTheme } = require(process.env.APPLY_THEME);

const THEME = {
  name: "Lululime",
  headFontFace: "Calibri",
  bodyFontFace: "Calibri",
  colors: {
    dk1: "0B0B0B", lt1: "FFFFFF", dk2: "52514E", lt2: "F4F3F0",
    accent1: "2A78D6", accent2: "EB6834", accent3: "1BAF7A", accent4: "EDA100",
    accent5: "6250D6", accent6: "E34948", hlink: "2A78D6", folHlink: "6250D6",
  },
};
const HEX = { ink: "0B0B0B", muted: "52514E", grid: "E4E3DF", blue: "2A78D6", orange: "EB6834", panel: "F4F3F0" };

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.title = "Lululime repairs: slides 7-8";
const C = pres.SchemeColor;

pres.defineSlideMaster({
  title: "CHART_PANEL",
  background: { color: "FFFFFF" },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 0.4, w: 12.1, h: 0.8,
        fontSize: 36, bold: true, color: C.text1, valign: "top", align: "left", margin: 0 }, text: "" } },
    { placeholder: { options: { name: "body", type: "body", x: 0.6, y: 1.2, w: 12.1, h: 0.45,
        fontSize: 16, color: C.text2, valign: "top", margin: 0 }, text: "" } },
    { placeholder: { options: { name: "source", type: "body", x: 0.6, y: 6.85, w: 10.6, h: 0.35,
        fontSize: 10, color: C.text2, valign: "top", margin: 0 }, text: "" } },
  ],
  slideNumber: { x: 12.2, y: 6.85, w: 0.5, h: 0.35, fontSize: 10, color: HEX.muted, align: "right" },
});

const AXIS = {
  catAxisLabelColor: HEX.muted, valAxisLabelColor: HEX.muted,
  catAxisLabelFontFace: "+mn-lt", valAxisLabelFontFace: "+mn-lt",
  catAxisLabelFontSize: 12, valAxisLabelFontSize: 11,
  dataLabelColor: HEX.ink, dataLabelFontFace: "+mn-lt", dataLabelFontSize: 12,
  catGridLine: { style: "none" },
  valAxisLineShow: false,
};

// Right-hand stat panel: big number + label, repeated
function statPanel(slide, items) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 8.9, y: 1.95, w: 3.8, h: 4.75, fill: { color: C.background2 }, line: { type: "none" },
    rectRadius: 0.12, objectName: "Stat panel" });
  let y = 2.1;
  items.forEach((it, i) => {
    slide.addText(it.big, { x: 9.2, y, w: 3.3, h: 0.75, fontSize: it.size || 40, bold: true,
      color: it.color, margin: 0, valign: "bottom", isTextBox: true, objectName: `Stat ${i + 1}` });
    slide.addText(it.label, { x: 9.2, y: y + 0.8, w: 3.3, h: 0.65, fontSize: 14, color: C.text1,
      margin: 0, valign: "top", isTextBox: true, objectName: `Stat ${i + 1} label` });
    y += 1.5;
  });
}

// ---------- Slide 7: churn (deck blueprint slide 7) ----------
pres.addSection({ title: "Repairs" });
const s7 = pres.addSlide({ masterName: "CHART_PANEL", sectionTitle: "Repairs" });
s7.addText("Repairs keep the best customers", { placeholder: "title" });
s7.addText("Repair users are mostly Gold members, and they stop shopping far less than similar customers",
  { placeholder: "body" });
s7.addChart(pres.charts.BAR, [
  { name: "Repair users", labels: ["Raw", "Matched on age +\npre-launch spend", "Matched, and still\nbuying after launch"],
    values: [0.147, 0.147, 0.148] },
  { name: "Similar non-users", labels: ["Raw", "Matched on age +\npre-launch spend", "Matched, and still\nbuying after launch"],
    values: [0.842, 0.811, 0.657] },
], {
  x: 0.5, y: 1.85, w: 8.1, h: 4.85, barDir: "col", barGrouping: "clustered", barGapWidthPct: 60,
  chartColors: [HEX.blue, HEX.orange],
  showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: "0%",
  valAxisMinVal: 0, valAxisMaxVal: 1, valAxisMajorUnit: 0.2, valAxisLabelFormatCode: "0%",
  valGridLine: { color: HEX.grid, size: 0.75 },
  showTitle: true, title: "Churned (no visit in 180 days)", titleFontSize: 12, titleColor: HEX.muted, titleFontFace: "+mn-lt",
  showLegend: true, legendPos: "t", legendFontSize: 12, legendColor: HEX.ink, legendFontFace: "+mn-lt",
  ...AXIS, objectName: "Churn chart",
});
statPanel(s7, [
  { big: "64% Gold", color: C.accent1, size: 36,
    label: "of active repair users are Gold members (vs 8% of other customers)" },
  { big: "5–9 pts", color: C.text1,
    label: "lower churn caused by repairs, after controls (churn model)" },
  { big: "24%", color: C.accent2,
    label: "churn when repairs take over 20 days, vs 11–13% when faster" },
]);
s7.addText("Matched = same age band × pre-launch spend quartile. No cannibalization: repair users' outerwear spend +10% after launch.",
  { placeholder: "source" });
s7.addNotes(
`Headline: free repairs are used by our best customers, and those customers stay.

- Who uses repairs: 64% of active repair users are Gold members, versus 8% of everyone else. Each brings in about 5 times as much yearly revenue.
- Churn: only 15% of repair users stopped shopping, versus 66% of similar customers (same age, same spending, still shopping after repairs launched).
- Honest caveat: loyal people are the ones who use repairs, so not all of that gap is caused by repairs. Our churn model controls for how engaged people already were, and it says repairs themselves cut churn by about 5 to 9 points.
- Speed matters: when repairs take over 20 days, 24% of those customers leave, versus 11–13% when repairs are faster.
- Leadership's jacket worry doesn't hold up: repair users bought 10% more outerwear after launch. The outerwear drop came from customers who never used repairs.`);

// ---------- Backup slide: money (feeds deck slide 8 / appendix A4) ----------
const s8 = pres.addSlide({ masterName: "CHART_PANEL", sectionTitle: "Repairs" });
s8.addText("Closing repairs is roughly break-even", { placeholder: "title" });
s8.addText("Yearly repair cost vs profit at risk if repairs close: forecast (dark) and what-ifs (light)",
  { placeholder: "body" });
s8.addChart(pres.charts.BAR, [
  { name: "Per year ($K)", labels: ["Cost saved by\nclosing", "At risk:\nforecast low", "At risk:\nforecast high",
    "What-if: 25%\nis causal", "What-if: 50%\nis causal"], values: [134, 77, 201, 366, 733] },
], {
  x: 0.5, y: 1.85, w: 8.1, h: 4.85, barDir: "col", barGapWidthPct: 55,
  chartColors: [HEX.blue, HEX.orange, HEX.orange, "F4B49A", "F4B49A"],
  showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: '"$"#,##0"K"',
  valAxisMinVal: 0, valAxisMaxVal: 800, valAxisMajorUnit: 200, valAxisLabelFormatCode: '"$"#,##0"K"',
  valGridLine: { color: HEX.grid, size: 0.75 }, showLegend: false,
  ...AXIS, objectName: "Cost vs profit chart",
});
statPanel(s8, [
  { big: "+$57K to −$67K", color: C.text1, size: 30,
    label: "net yearly effect of closing repairs: saves a little or loses a little" },
  { big: "<1%", color: C.accent1,
    label: "of revenue at stake either way: not the saving leadership expects" },
  { big: "77%", color: C.text1,
    label: "of company ARR comes from the 2,175 repair users ($5.1M of $6.7M)" },
]);
s8.addText("At risk = churn-model forecast per repair user (boosted trees / logistic) × their ARR × 57% margin. What-ifs use the 51-pt matched gap.",
  { placeholder: "source" });
s8.addNotes(
`Headline: closing repairs wouldn't save the money leadership expects. It's roughly break-even.

- Repairs cost about $134K a year.
- Our churn model forecasts, customer by customer, how many repair users would leave if repairs closed, and what profit they'd take with them: between $77K and $201K a year.
- So closing repairs would somewhere between save about $57K and lose about $67K a year. That's under 1% of revenue either way.
- The lighter bars are what-ifs: if repairs explained a quarter or half of the loyalty gap, the loss would be much bigger. The model says that's unlikely, so we don't lean on them.
- Bottom line: repairs aren't a money drain. They keep our Gold members, cost about what they earn back, and become clearly profitable if we make them faster and cheaper.`);

(async () => {
  const out = path.join(__dirname, "c_repairs_slides_7-8.pptx");
  await pres.writeFile({ fileName: out });
  await applyTheme(out, THEME);
  console.log("wrote", out);
})();
