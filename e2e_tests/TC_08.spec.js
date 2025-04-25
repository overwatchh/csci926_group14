// Testcase ID: TC8
// Testcase Name: Chart container is within viewport
// Description: Ensure the chart container is fully visible within the viewport without requiring scrolling
// Input: Load the chart HTML at default window size (1280 x 720)
// Expected: The chart container is within the visible browser area. No scroll needed to see it fully

const { test, expect } = require("@playwright/test");
const path = require("path");
import { chartTypes } from "./chartTypes";

const chartVariants = Array.from({ length: 2 }, (_, i) => i + 1); // [1, 2]

chartTypes.forEach((chartType) => {
  for (const variant of chartVariants) {
    test.describe(`${chartType} - variant ${variant}`, () => {
      test.use({ viewport: { width: 1280, height: 720 } }); // Set window size

      test(`TC08[${chartType} v${variant}]: Chart container is within viewport`, async ({
        page,
      }) => {
        const chartPath = path.join(
          __dirname,
          `../output/${chartType}_${variant}.html`
        );
        const chartUrl = "file://" + chartPath;

        await page.goto(chartUrl);

        // Get chart bounding box and viewport size
        const chart = page.locator(".mpld3-figure");
        await expect(chart).toBeVisible();

        const box = await chart.boundingBox();
        const viewport = page.viewportSize();

        // Assert chart is fully within viewport (no overflow)
        expect(box.x).toBeGreaterThanOrEqual(0);
        expect(box.y).toBeGreaterThanOrEqual(0);
        expect(box.x + box.width).toBeLessThanOrEqual(viewport.width);
        expect(box.y + box.height).toBeLessThanOrEqual(viewport.height);

        // Optionally: ensure no scrollbars by checking page content size
        const body = await page.evaluate(() => ({
          scrollWidth: document.body.scrollWidth,
          scrollHeight: document.body.scrollHeight,
        }));

        expect(body.scrollWidth).toBeLessThanOrEqual(viewport.width);
        expect(body.scrollHeight).toBeLessThanOrEqual(viewport.height);
      });
    });
  }
});
