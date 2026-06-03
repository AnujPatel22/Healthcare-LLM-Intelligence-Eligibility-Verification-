const { chromium } = require("playwright");
const path = require("path");

const base = process.env.APP_URL || "http://localhost:5174";
const out = path.resolve(__dirname, "..", "..", "docs", "screenshots");

async function screenshot(page, name) {
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(out, `${name}.png`), fullPage: true });
}

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });

  await page.goto(base, { waitUntil: "networkidle" });
  await page.waitForSelector("#root");
  await screenshot(page, "dashboard");

  await page.locator('.nav button[title="Eligibility"]').click();
  await page.getByRole("button", { name: "Run check" }).click();
  await page.getByText("ACTIVE").waitFor({ timeout: 10000 });
  await screenshot(page, "eligibility-verification");

  await page.locator('.nav button[title="Claims"]').click();
  await page.getByRole("button", { name: "Validate" }).click();
  await page.getByText("Mock grounded explanation").waitFor({ timeout: 10000 });
  await screenshot(page, "claim-validation");

  await page.locator('.nav button[title="Rules"]').click();
  await page.getByRole("button", { name: "Search" }).click();
  await page.getByText("RULE-APEX-IMG-001").waitFor({ timeout: 10000 });
  await screenshot(page, "rule-explorer");

  await page.locator('.nav button[title="Codebooks"]').click();
  await page.getByRole("button", { name: "Search" }).click();
  await page.getByText("70553").first().waitFor({ timeout: 10000 });
  await screenshot(page, "codebook-search");

  await page.locator('.nav button[title="Scaling"]').click();
  await page.getByText("20,000+").first().waitFor({ timeout: 10000 });
  await screenshot(page, "scaling-benchmarks");

  await browser.close();
})();
