const { describe, test, expect } = require("@playwright/test");
const { console } = require("inspector");
const path = require("path");

describe("Chart Rendering and Basic Display", () => {
  test("check chart title is visible", async ({ page }) => {
    const chartPath = path.join(__dirname, "../output/example_chart.html");
    const chartUrl = "file://" + chartPath;
    console.log("chartUrl", chartUrl);

    await page.goto(chartUrl);

    const title = await page.locator("text=Test Chart").first();
    await expect(title).toBeVisible();
  });
});

describe("Chart Interactivity", () => {
  test("zoom in/out works correctly", async ({ page }) => {
    const chartPath = path.join(__dirname, "../output/example_chart.html");
    const chartUrl = "file://" + chartPath;

    await page.goto(chartUrl);

    const initialDataPoints = await page.locator("circle").count();

    await page.mouse.wheel(0, -100); // Zoom in
    await page.waitForTimeout(500);

    const zoomedInDataPoints = await page.locator("circle").count();
    expect(zoomedInDataPoints).toBe(initialDataPoints); // Should remain the same

    await page.mouse.wheel(0, 100); // Zoom out
    await page.waitForTimeout(500);

    const zoomedOutDataPoints = await page.locator("circle").count();
    expect(zoomedOutDataPoints).toBe(initialDataPoints); // Should still be the same
  });
});

describe("Zoom and Axis Range", () => {
  test("check axes range after zoom", async ({ page }) => {
    const chartPath = path.join(__dirname, "../output/example_chart.html");
    const chartUrl = "file://" + chartPath;

    await page.goto(chartUrl);

    const initialXMin = await page.locator("text=1").first();
    const initialXMax = await page.locator("text=3").first();

    await page.mouse.wheel(0, -100); // Zoom in
    await page.waitForTimeout(500);

    const zoomedInXMin = await page.locator("text=1").first();
    const zoomedInXMax = await page.locator("text=3").first();

    expect(initialXMin).not.toEqual(zoomedInXMin);
    expect(initialXMax).not.toEqual(zoomedInXMax);
  });
});

describe("Chart Rendering After Reload", () => {
  test("check chart renders after reload", async ({ page }) => {
    const chartPath = path.join(__dirname, "../output/example_chart.html");
    const chartUrl = "file://" + chartPath;

    await page.goto(chartUrl);

    await page.reload();

    const title = await page.locator("text=Test Chart").first();
    await expect(title).toBeVisible();
  });
});
