import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import type { FrontendShellOptions } from "../../../contracts/frontend-shell/types";
import { FrontendShell } from "./shell";

/** Mount once per container. The caller owns its content and the returned teardown. */
export function mountFrontendShell(
  container: Element,
  options: FrontendShellOptions = {},
): () => void {
  const root = createRoot(container);
  root.render(<StrictMode><FrontendShell {...options} /></StrictMode>);
  return () => root.unmount();
}
