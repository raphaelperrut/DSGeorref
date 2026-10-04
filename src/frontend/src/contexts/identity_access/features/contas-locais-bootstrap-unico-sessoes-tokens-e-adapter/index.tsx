import { mountFrontendShell } from "../../../operator_experience/contracts/frontend-shell";
import { IdentitySurface } from "./identity-surface";

export { IdentitySurface } from "./identity-surface";
/** Public feature entrypoint; foundation owns the shell and generated transport. */
export function mountIdentitySurface(container: Element): () => void {
  return mountFrontendShell(container, { children: <IdentitySurface /> });
}
