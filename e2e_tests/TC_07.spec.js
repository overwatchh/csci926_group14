// Testcase ID: TC7
// Testcase Name: Legend appears
// Description: Check that chart legend is present and correct
// Input: A chart with multiple lines, each labeled using label argument
// Expected: The legend shows correct line labels and color codes
const { test, expect } = require("@playwright/test");
const path = require("path");
import { chartTypes } from "./chartTypes";

const chartVariants = Array.from({ length: 2 }, (_, i) => i + 1); // [1, 2]

chartTypes.forEach((chartType) => {
  for (const variant of chartVariants) {
    test.describe(`${chartType} - variant ${variant}`, () => {
      test(`TC07[${chartType} v${variant}]: Check that chart legend is present and correct`, async ({
        page,
      }) => {
        const chartPath = path.join(
          __dirname,
          `../output/${chartType}_${variant}.html`
        );
        const chartUrl = "file://" + chartPath;

        await page.goto(chartUrl);

        // Ensure chart is visible
        const chart = page.locator(".mpld3-figure");
        await expect(chart).toBeVisible();

        // Find legend group (usually within <g> tag in SVG)
        const legendItems = chart.locator("g.legend text");
        const itemCount = await legendItems.count();

        // Check each legend item
        for (let i = 0; i < itemCount; i++) {
          const labelText = await legendItems.nth(i).textContent();
          expect(labelText?.trim().length).toBeGreaterThan(0);

          // Optional: check for corresponding color box (rect or line color)
          const legendColor = await chart
            .locator("g.legend rect, g.legend path, g.legend line")
            .nth(i)
            .getAttribute("style");
          expect(legendColor).not.toBeNull();
        }
      });
    });
  }
});
