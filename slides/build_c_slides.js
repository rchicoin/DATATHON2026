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

// ---------- Slide 7: churn ----------
pres.addSection({ title: "Repairs" });
const s7 = pres.addSlide({ masterName: "CHART_PANEL", sectionTitle: "Repairs" });
s7.addText("Repair users stay far longer", { placeholder: "title" });
s7.addText("Share who stopped shopping (no visit in 180 days), customers active in the year before repairs launched",
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
  showLegend: true, legendPos: "t", legendFontSize: 12, legendColor: HEX.ink, legendFontFace: "+mn-lt",
  ...AXIS, objectName: "Churn chart",
});
statPanel(s7, [
  { big: "15% vs 66%", color: C.accent1, size: 36,
    label: "churn: repair users vs similar customers still buying after launch" },
  { big: "−51 pts", color: C.text1,
    label: "churn gap we carry into the cost test (our conservative estimate)" },
  { big: "24%", color: C.accent2,
    label: "churn when repairs take over 20 days, vs 11–13% when faster" },
]);
s7.addText("Matched = same age band and pre-launch spend quartile. 1,702 repair users vs 4,992 non-users. Counting purchase visits only changes the gap by <1 pt.",
  { placeholder: "source" });
s7.addNotes(
`Headline: customers who use free repairs are far less likely to stop shopping with us.

- Raw numbers look extreme (15% vs 84%), but that's unfair: loyal customers are the ones who bring clothes in.
- So we only compared customers who were shopping before repairs existed, with the same age and spending level. Repair users still churn 15% vs 81%.
- More than half of those non-users had left before repairs even launched, so we also required them to still be buying afterwards. The gap is still 15% vs 66%: 51 points. That's the number we carry forward.
- Turnaround matters: when repairs take over 20 days, churn doubles to 24%. That's a cheap thing to fix.
- Caveat: this shows repair users stay, not that repairs alone make them stay. The next slide tests how much that matters.`);

// ---------- Slide 8: cost vs profit at risk ----------
const s8 = pres.addSlide({ masterName: "CHART_PANEL", sectionTitle: "Repairs" });
s8.addText("Scrapping repairs costs more than it saves", { placeholder: "title" });
s8.addText("Yearly repair cost vs profit lost if repairs explain 25%, 50% or 100% of the churn gap",
  { placeholder: "body" });
s8.addChart(pres.charts.BAR, [
  { name: "Per year ($K)", labels: ["Cost saved by\nscrapping", "Profit lost if\n25% is causal",
    "Profit lost if\n50% is causal", "Profit lost if\n100% is causal"], values: [134, 366, 733, 1465] },
], {
  x: 0.5, y: 1.85, w: 8.1, h: 4.85, barDir: "col", barGapWidthPct: 55,
  chartColors: [HEX.blue, HEX.orange, HEX.orange, HEX.orange],
  showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: '"$"#,##0"K"',
  valAxisMinVal: 0, valAxisMaxVal: 1600, valAxisMajorUnit: 400, valAxisLabelFormatCode: '"$"#,##0"K"',
  valGridLine: { color: HEX.grid, size: 0.75 }, showLegend: false,
  ...AXIS, objectName: "Cost vs profit chart",
});
statPanel(s8, [
  { big: "9%", color: C.accent1,
    label: "scrapping only pays off if repairs cause less than 9% of the churn gap" },
  { big: "77%", color: C.text1,
    label: "of company ARR comes from the 2,175 repair users ($5.1M of $6.7M)" },
  { big: "+10%", color: C.accent1,
    label: "repair users' outerwear spend after launch: no sign of cannibalization" },
]);
s8.addText("Cost = repair cost Nov 2025 – Oct 2026. Profit lost = repair users' ARR × 51-pt churn gap × share caused × 56% margin. Outerwear: 12 months before vs after launch.",
  { placeholder: "source" });
s8.addNotes(
`Headline: repairs cost about $134K a year, but they protect much more profit than that.

- Repair users are only 2,175 customers but bring in 77% of our repeat revenue.
- We can't prove exactly how much of their loyalty is caused by repairs, so we tested three cases. Even if repairs explain only a quarter of the gap, scrapping them loses about $366K of profit to save $134K.
- Break-even is 9%: repairs would have to explain almost none of the loyalty for cutting them to save money.
- Leadership's other worry was that repairs stop people buying new jackets. Outerwear did fall 12% store-wide, but repair users bought 10% MORE outerwear; the whole drop came from customers who never used repairs.
- Recommendation: keep free repairs, and set a target of repairs back within 20 days.`);

(async () => {
  const out = path.join(__dirname, "c_repairs_slides_7-8.pptx");
  await pres.writeFile({ fileName: out });
  await applyTheme(out, THEME);
  console.log("wrote", out);
})();
