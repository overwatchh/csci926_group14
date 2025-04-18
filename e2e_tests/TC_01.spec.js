// Tescase ID: TC1
// Testcase Name: Chart loads successfully
// Description: Verify that the chart renders without any errors on page load
// Input: Load the generated .html file in browser
// Expected: The page loads completely
const { test, expect } = require("@playwright/test");
const path = require("path");
import { chartTypes } from "./chartTypes";

const chartVariants = Array.from({ length: 2 }, (_, i) => i + 1); // [1, 2]

for (const chartType of chartTypes) {
  for (const variant of chartVariants) {
    test.describe(`${chartType} - variant ${variant}`, () => {
      test(`TC01[${chartType} v${variant}]: should load chart HTML file without errors`, async ({
        page,
      }) => {
        const chartPath = path.join(
          __dirname,
          `../output/${chartType}_${variant}.html`
        );
        const chartUrl = "file://" + chartPath;

        await page.goto(chartUrl);

        // Wait for any chart elements (e.g., SVG) to be present
        // one for chart and one for toolbar
        await expect(page.locator("svg")).toHaveCount(2);

        // Check if there are no error messages
        const errorLogs = [];
        page.on("pageerror", (error) => {
          errorLogs.push(error.message);
        });

        // Wait for the page to finish loading
        await page.waitForLoadState("load");

        // Assert no errors captured
        expect(errorLogs.length).toBe(0);
      });
    });
  }
}
