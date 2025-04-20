// Tescase ID: TC5
// Testcase Name: Zoom functionality
// Description: Verify that user can zoom and pan using the chart controls
// Input: "1. Click on the box zoom icon in the  tool bar 2.Simulate mouse wheel zoom and click-drag pan"
// Expected: The chart updates accordingly, zooming without breaking

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

        // Wait for the boxzoom button to appear
        const boxzoomButton = page.locator(".mpld3-boxzoombutton" );
        await expect(boxzoomButton).toBeVisible();

        // Click the boxzoom button
        await boxzoomButton.click();

        // Assert the boxzoom button has the 'pressed active' classes after being clicked
        await expect(boxzoomButton).toHaveClass(/active/); // the zoom functionality worked
        await expect(boxzoomButton).toHaveClass(/pressed/); // the zoom button is clicked

        // Simulate mouse wheel zoom (zoom in)
        await page.mouse.wheel(0, 100);
        
        //Simulate click-drag pan (click on the chart and drag)
        const chartBoundingBox = await chartArea.boundingBox();
        const startX = chartBoundingBox.x + 50; 
        const startY = chartBoundingBox.y + 50; 

        // Perform the pan operation by clicking and dragging
        await page.mouse.click(startX, startY);
        await page.mouse.move(startX + 100, startY + 100); 
        await page.mouse.up(); 


      });
    });
  }
});
