import { expect, test } from "@playwright/test";

test("the built shell bootstraps with the generated client and no backend", async ({ page }) => {
  const errors: string[] = [];
  const apiRequests: string[] = [];
  page.on("pageerror", error => errors.push(error.message));
  page.on("console", message => { if (message.type() === "error") errors.push(message.text()); });
  page.on("request", request => { if (request.url().includes("/api/")) apiRequests.push(request.url()); });
  const response = await page.goto("/");
  expect(response?.status()).toBe(200);
  await expect(page.getByRole("heading", { name: "DSGeorref" })).toBeVisible();
  // This value is read from the generated client at runtime, surviving the production bundle.
  await expect(page.getByRole("main")).toHaveAttribute("data-openapi-base-url", "/api/v1");
  expect(errors).toEqual([]);
  expect(apiRequests).toEqual([]);
});
