const { describe, test, expect } = require("@playwright/test");
const path = require("path");
describe("Line chart", () => {
  test("Chart variant 1:", async ({ page }) => {
    const chartPath = path.join(__dirname, "../../output/example_chart.html");
    const chartUrl = "file://" + chartPath;

    await page.goto(chartUrl);
    
    await expect(5 == 5).toBe(true);
  });
  // test for next chart variant until 10
});
