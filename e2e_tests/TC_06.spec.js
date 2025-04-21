// Tescase ID: TC6
// Testcase Name: Toolbar auto-hide behavior
// Description: Verify that the toolbar remains visible when the user hovers over the chart, and does't auto-hide during a period of interactivity
// Input: Load the HTML file. Hover to trigger the toolbar, then stop interacting for a few seconds, and then remove theh mouse
// Expected: Load the HTML file. Hover to trigger the toolbar, then stop interacting for a few seconds, and then remove theh mouse

const { test, expect } = require("@playwright/test");
const path = require("path");
import { chartTypes } from "./chartTypes";

const chartVariants = Array.from({ length: 2 }, (_, i) => i + 1); // [1, 2]

chartTypes.forEach((chartType) => {
  for (const variant of chartVariants) {
    test.describe(`${chartType} - variant ${variant}`, () => {
      test(`TC09[${chartType} v${variant}]: Toolbar auto-hide behavior`, async ({
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

        // Confirm a known toolbar button (e.g., reset) is visible
        const resetButton = page.locator(".mpld3-resetbutton");
        await expect(resetButton).toBeVisible();

        // Wait for 3 seconds to simulate user inactivity
        await page.waitForTimeout(3000);
        await expect(resetButton).toBeVisible();
                
        //Move mouse away and check if toolbar disappears
        await page.mouse.move(-100, -100);
        await expect(resetButton).toBeVisible({timeout: 10000});


      });
    });
  }
});
