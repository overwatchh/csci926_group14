// Testcase ID: TC4
// Testcase Name: Data integrity after rendering
// Description: Verify that rendered graph data matches original input data within acceptable error margin
// Input: Load generated HTML file and corresponding test data JSON
// Expected: No significant mismatch between input and visualized data
const { test, expect } = require("@playwright/test");
const path = require("path");
const fs = require("fs");
import { chartTypes } from "./chartTypes";

const chartVariants = Array.from({ length: 2 }, (_, i) => i + 1); // [1, 2]

for (const chartType of chartTypes) {
  for (const variant of chartVariants) {
    test.describe(`${chartType} - variant ${variant}`, () => {
      test(`TC03[${chartType} v${variant}]: should have correct data points in generated HTML`, async ({
        page,
      }) => {
        // Paths for both chart and test data
        const chartPath = path.join(
          __dirname,
          `../output/${chartType}_${variant}.html`
        );
        const dataPath = path.join(
          __dirname,
          `../test_data/${chartType}_${variant}.json`
        );
        
        // Verify test data file exists
        expect(fs.existsSync(dataPath)).toBe(true);
        
        // Load test data
        const testData = JSON.parse(fs.readFileSync(dataPath, 'utf-8'));
        
        // Load chart
        await page.goto(`file://${chartPath}`);
        
        // Wait for mpld3 to be available
        await page.waitForFunction(() => window.mpld3 && window.mpld3.figures.length > 0);

        // Extract data from mpld3 figure
        const figureData = await page.evaluate(() => {
          return window.mpld3.figures[0];
        });
        
        expect(figureData).not.toBeNull();

        // Chart-specific verification logic
        switch (chartType) {
          case 'line_chart':
            for (let i = 0; i < testData.y.length; i++) {
                expect(figureData.data.data01[i][1]).toBeCloseTo(testData.y[i], 5);
              }
            break;

          case 'area_chart':
            for (let i = 1; i < testData.y.length; i++) {
                expect(figureData.props.axes[0].collections[0].paths[0][0][i][1]).toBeCloseTo(testData.y[i-1], 5);
              }
            break;

          case 'stem_plot':
            for (let i = 0; i < testData.y.length; i++) {
                expect(figureData.data.data01[i][1]).toBeCloseTo(testData.y[i], 5);
              }
            break;
            
          case 'scatter_plot':
            for (let i = 0; i < testData.y.length; i++) {
                expect(figureData.data.data01[i][1]).toBeCloseTo(testData.y[i], 5);
              }
            break;

          case 'polar_plot':
            for (let i = 0; i < testData.r.length; i++) {
                expect(figureData.data.data01[i][1]).toBeCloseTo(testData.r[i], 5);
              }
            break;
            
          default:
            // Keep null checks for unsupported chart types
            expect(figureData.data.data01).not.toBeNull();
        }
      });
    });
  }
}