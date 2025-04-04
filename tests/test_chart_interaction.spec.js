const {describe, test, expect } = require('@playwright/test');
const path = require('path');

describe('Chart Rendering and Basic Display', () => {
  
  test('check chart title is visible', async ({ page }) => {
    const chartPath = path.join(__dirname, '../output/example_chart.html');
    const chartUrl = 'file://' + chartPath;
  
    await page.goto(chartUrl);
  
    const title = await page.locator('text=Test Chart').first();
    await expect(title).toBeVisible();
  });

  test('check chart data points are visible', async ({ page }) => {
    const chartPath = path.join(__dirname, '../output/example_chart.html');
    const chartUrl = 'file://' + chartPath;
  
    await page.goto(chartUrl);
  
    const dataPoints = await page.locator('circle').count();
    expect(dataPoints).toBeGreaterThan(2);
  });

  test('check for axes labels', async ({ page }) => {
    const chartPath = path.join(__dirname, '../output/example_chart.html');
    const chartUrl = 'file://' + chartPath;
  
    await page.goto(chartUrl);
  
    const xAxisLabel = await page.locator('text=X Axis').first();
    const yAxisLabel = await page.locator('text=Y Axis').first();
  
    await expect(xAxisLabel).toBeVisible();
    await expect(yAxisLabel).toBeVisible();
  });
});

describe('Chart Interactivity', () => {
  
  test('hover over data point to show tooltip', async ({ page }) => {
    const chartPath = path.join(__dirname, '../output/example_chart.html');
    const chartUrl = 'file://' + chartPath;
  
    await page.goto(chartUrl);
  
    const firstDataPoint = await page.locator('circle').first();
    await firstDataPoint.hover();
  
    const tooltip = await page.locator('.mpld3-tooltip').first();
    await expect(tooltip).toBeVisible();
  });

  test('zoom in/out works correctly', async ({ page }) => {
    const chartPath = path.join(__dirname, '../output/example_chart.html');
    const chartUrl = 'file://' + chartPath;
  
    await page.goto(chartUrl);
  
    const initialDataPoints = await page.locator('circle').count();
  
    await page.mouse.wheel(0, -100);  // Zoom in
    await page.waitForTimeout(500);  
    
    const zoomedInDataPoints = await page.locator('circle').count();
    expect(zoomedInDataPoints).toBe(initialDataPoints);  // Should remain the same
  
    await page.mouse.wheel(0, 100);  // Zoom out
    await page.waitForTimeout(500);
  
    const zoomedOutDataPoints = await page.locator('circle').count();
    expect(zoomedOutDataPoints).toBe(initialDataPoints);  // Should still be the same
  });

  test('check for interactive buttons', async ({ page }) => {
    const chartPath = path.join(__dirname, '../output/example_chart.html');
    const chartUrl = 'file://' + chartPath;
  
    await page.goto(chartUrl);
  
    const zoomInButton = await page.locator('button[aria-label="Zoom In"]');
    await expect(zoomInButton).toBeVisible();
  
    const legend = await page.locator('.mpld3-legend').first();
    await expect(legend).toBeVisible();
  });
});

describe('Zoom and Axis Range', () => {

  test('check axes range after zoom', async ({ page }) => {
    const chartPath = path.join(__dirname, '../output/example_chart.html');
    const chartUrl = 'file://' + chartPath;

    await page.goto(chartUrl);

    const initialXMin = await page.locator('text=1').first();
    const initialXMax = await page.locator('text=3').first();

    await page.mouse.wheel(0, -100);  // Zoom in
    await page.waitForTimeout(500);

    const zoomedInXMin = await page.locator('text=1').first();
    const zoomedInXMax = await page.locator('text=3').first();

    expect(initialXMin).not.toEqual(zoomedInXMin);
    expect(initialXMax).not.toEqual(zoomedInXMax);
  });

});

describe('Chart Rendering After Reload', () => {

  test('check chart renders after reload', async ({ page }) => {
    const chartPath = path.join(__dirname, '../output/example_chart.html');
    const chartUrl = 'file://' + chartPath;

    await page.goto(chartUrl);
    
    await page.reload();

    const title = await page.locator('text=Test Chart').first();
    await expect(title).toBeVisible();
  });

});

