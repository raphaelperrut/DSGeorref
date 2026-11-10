/// <reference types="vite/client" />

import { mountIdentitySurface } from "./contexts/identity_access/features/contas-locais-bootstrap-unico-sessoes-tokens-e-adapter";
import { mountFrontendShell } from "./contexts/operator_experience/contracts/frontend-shell";

const container = document.getElementById("root");
if (!container) throw new Error("Frontend shell root is missing");
if (import.meta.env.VITE_IDENTITY_DEV) {
  mountIdentitySurface(container);
} else {
  mountFrontendShell(container);
}
