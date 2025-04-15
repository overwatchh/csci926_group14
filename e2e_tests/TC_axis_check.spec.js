const { test, expect } = require('@playwright/test');

const chartTypes = [
  '3d_plot',
  'area_chart',
  'bar_chart',
  'box_plot',
  'error_bar_chart',
  'heat_map',
  'histogram',
  'line_chart',
  'pie_chart',
  'polar_plot',
  'scatter_plot',
  'stacked_bar_chart'
];

const chartVariants = Array.from({ length: 12 }, (_, i) => i + 1);

for (const chartType of chartTypes) {
  for (const variant of chartVariants) {
    test.describe(`${chartType} - variant ${variant}`, () => {
      test(`TC1: [${chartType} v${variant}] X axis is displayed`, async ({ page }) => {
        const chartPath = `file:///C:/Users/ethan/csci926_group14/output/${chartType}.html`;
        await page.goto(chartPath);
        const xAxisLocator = page.locator('.x-axis');
        await expect(xAxisLocator).toBeVisible();
      });

      test(`TC2: [${chartType} v${variant}] Y axis is displayed`, async ({ page }) => {
        const chartPath = `file:///C:/Users/ethan/csci926_group14/output/${chartType}.html`;
        await page.goto(chartPath);
        const yAxisLocator = page.locator('.y-axis');
        await expect(yAxisLocator).toBeVisible();
      });
    });
  }
}
