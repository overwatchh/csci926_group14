// Tescase ID: TC11
// Testcase Name: Test the X axis is displayed correctly
// Description: Confirm that the X axis element is visible in all 12 kinds of charts with 2 variants
// Input: Open each chart’s HTML, locate the X axis DOM element (e.g. .x-axis).
// Expected: The X axis is correctly rendered and visible for every chart and variant.
const { test, expect } = require("@playwright/test");
const path = require("path");
import { chartTypes } from "./chartTypes";

const chartVariants = Array.from({ length: 2 }, (_, i) => i + 1); // [1, 2]

for (const chartType of chartTypes) {
  for (const variant of chartVariants) {
    test.describe(`${chartType} - variant ${variant}`, () => {
      test(`TC1[${chartType} v${variant}]: X axis is displayed`, async ({
        page,
      }) => {
        const chartPath = path.join(
          __dirname,
          `../output/${chartType}_${variant}.html`
        );
        const chartUrl = "file://" + chartPath;

        await page.goto(chartUrl);
        const xAxisLocator = page.locator(".mpld3-xaxis");
        await expect(xAxisLocator.first()).toBeVisible();
      });
    });
  }
}
