import { mountFrontendShell } from "../../../operator_experience/contracts/frontend-shell";
import { ProjectAccessSurface } from "./surface";

export { ProjectAccessSurface } from "./surface";
export function mountProjectAccess(container: Element): () => void {
  return mountFrontendShell(container, { children: <ProjectAccessSurface /> });
}
