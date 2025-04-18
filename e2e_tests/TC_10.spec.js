// Tescase ID: TC10
// Testcase Name: Zoom tool visibility
// Description: Verify that the reset tool is included in the interactive chart toolbar
// Input: Load the mpld3 chart html with default interactive chart toolbar. Hover over the chart to trigger the toolbar to show
// Expected: The toolbar contains a zoom button that is visible and clickable
const { test, expect } = require("@playwright/test");
const path = require("path");
import { chartTypes } from "./chartTypes";

const chartVariants = Array.from({ length: 2 }, (_, i) => i + 1); // [1, 2]

chartTypes.forEach((chartType) => {
  for (const variant of chartVariants) {
    test.describe(`${chartType} - variant ${variant}`, () => {
      test(`TC10[${chartType} v${variant}]: Zoom tool visibility`, async ({
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

        // Wait for the zoom button to appear
        const zoomButton = page.locator(".mpld3-zoombutton");
        await expect(zoomButton).toBeVisible();

        // Click the reset button
        await zoomButton.click();

        // Assert the reset button has the 'pressed active' classes after being clicked
        await expect(zoomButton).toHaveClass(/active/); // the zoom functionality worked
        await expect(zoomButton).toHaveClass(/pressed/); // the zoom button is clicked
      });
    });
  }
});
