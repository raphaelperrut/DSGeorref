import { mountFrontendShell } from "./contexts/operator_experience/contracts/frontend-shell";

const container = document.getElementById("root");
if (!container) throw new Error("Frontend shell root is missing");
mountFrontendShell(container);
