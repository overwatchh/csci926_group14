const { test, expect } = require('@playwright/test');
const path = require('path');
const fs = require('fs');
const math = require('mathjs');

const testCasesDir = path.join(__dirname, '../../output');

// Map of HTML file names to their corresponding math function expressions
const formulas = {
  'line_01.html': 'x * sin(x)',
  'line_02.html': 'min(x, 5)',
  'line_03.html': 'sqrt(x)',
  'line_04.html': 'log(x + 1)',
  'line_05.html': '1 - exp(-x)',
  'line_06.html': 'x - (x^3)/6',
  'line_07.html': 'floor(x)',
  'line_08.html': 'mod(x, 3)',
  'line_09.html': 'abs(sin(x))',
  'line_10.html': 'x / (1 + x)',
};

// Get list of test files in the directory
const testFiles = fs.readdirSync(testCasesDir).filter(file => file.startsWith('line'));

for (const file of testFiles) {

  test(`Function plot validation for ${file}`, async ({ page }) => {
    const filePath = path.join(testCasesDir, file);
    const fileUrl = `file://${filePath}`;
    const funcExpr = formulas[file];

    await page.goto(fileUrl);

    const svg = await page.locator('svg').first();
    await expect(svg).toBeVisible();

    // Extract the plot data from mpld3
    const data = await page.evaluate(() => {
      // This assumes mpld3 is used and data is in line objects
      const figure = window.mpld3?.figures?.[0];
      if (!figure) return null;

      // Assuming first line has the data
      const lineData = figure.data;

      return lineData.data01;
    });

    expect(data).not.toBeNull();
    expect(Array.isArray(data)).toBe(true);

    const parsedFunc = math.parse(funcExpr);
    const compiledFunc = parsedFunc.compile();

    for (const point of data) {
      const x = point[0];
      const expectedY = point[1];
      const calculatedY = compiledFunc.evaluate({ x });

      // Allow small floating point error
      expect(Math.abs(calculatedY - expectedY)).toBeLessThan(0.01);
    }
  });
}
