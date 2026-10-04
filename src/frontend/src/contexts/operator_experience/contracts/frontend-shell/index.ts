/** Consumers compose here and reuse the single generated transport. */
export { mountFrontendShell } from "../../adapters/web/bootstrap/mount";
export type { FrontendShellOptions } from "./types";
export { client } from "../openapi/generated/client.gen";
export * as api from "../openapi/generated/sdk.gen";
