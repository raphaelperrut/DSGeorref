import { expect, test } from "@playwright/test";

test("executes the browser gate", async ({ page }) => {
  await page.setContent("<main><h1>Frontend tooling</h1></main>");

  await expect(page.getByRole("heading", { name: "Frontend tooling" })).toBeVisible();
});
