// Tescase ID: TC2
// Testcase Name: Chart title is visible
// Description: Ensure that the chart title is correctly displayed in the HTML output
// Input: A chart with title is set using plt.title() function
// Expected: The titile of the chart is displayed and exist in the DOM
const { test, expect } = require("@playwright/test");
const path = require("path");
import { chartTypes } from "./chartTypes";

const chartVariants = Array.from({ length: 2 }, (_, i) => i + 1); // [1, 2]
const chartTitles = [
  "Area Chart",
  "Bar Chart",
  "Box Plot",
  "Heatmap",
  "Histogram",
  "Line Chart",
  "Pie Chart",
  "Polar Plot",
  "Scatter Plot",
  "Stacked Bar Chart",
  "Horizontal Bar Chart",
  "Stem Plot",
];

chartTypes.forEach((chartType, chartIndex) => {
  for (const variant of chartVariants) {
    test.describe(`${chartType} - variant ${variant}`, () => {
      test(`TC02[${chartType} v${variant}]: Chart title is visible in DOM`, async ({
        page,
      }) => {
        const chartPath = path.join(
          __dirname,
          `../output/${chartType}_${variant}.html`
        );
        const chartUrl = "file://" + chartPath;

        await page.goto(chartUrl);

        // Look for the chart title (mpld3 renders titles as <text> in <svg>)
        const chartTitle = await page.locator(`text=${chartTitles[chartIndex]}`).first();

        // Assert at least one text element contains the expected title
        await expect(chartTitle).toBeVisible();
      });
    });
  }
});
