// Tescase ID: TC9
// Testcase Name: Reset tool visibility
// Description: Verify that the reset tool is included in the interactive chart toolbar
// Input: Load the mpld3 chart html with default interactive chart toolbar. Hover over the chart to trigger the toolbar to show
// Expected: The toolbar contains a reset button that is visible and clickable
const { test, expect } = require("@playwright/test");
const path = require("path");
import { chartTypes } from "./chartTypes";

const chartVariants = Array.from({ length: 2 }, (_, i) => i + 1); // [1, 2]

chartTypes.forEach((chartType) => {
  for (const variant of chartVariants) {
    test.describe(`${chartType} - variant ${variant}`, () => {
      test(`TC09[${chartType} v${variant}]: Reset tool visibility`, async ({
        page,
      }) => {
        const chartPath = path.join(
          __dirname,
          `../output/${chartType}_${variant}.html`
        );
        const chartUrl = "file://" + chartPath;

        await page.goto(chartUrl);

        // Hover over the chart to trigger the toolbar to show
        const chartArea = await page.locator(".mpld3-figure");
        await chartArea.isVisible();
        await chartArea.hover();

        // Wait for the reset button to appear
        const resetButton = page.locator(
          ".mpld3-resetbutton"
        );
        await expect(resetButton).toBeVisible();

        // Click the reset button
        await resetButton.click();

        // Assert the reset button has the 'active' class after being clicked
        await expect(resetButton).toHaveClass(/active/); // reset functionality worked
      });
    });
  }
});
