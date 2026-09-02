import { getByRole } from "@testing-library/dom";
import { describe, expect, it } from "vitest";

describe("frontend test gate", () => {
  it("executes Testing Library under Vitest", () => {
    document.body.innerHTML = '<output role="status">tooling-ready</output>';

    expect(getByRole(document.body, "status").textContent).toBe("tooling-ready");
  });
});
