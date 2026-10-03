import type { FrontendShellOptions } from "../../../contracts/frontend-shell/types";
import { client } from "../../../contracts/openapi/generated/client.gen";

export function FrontendShell({ children }: FrontendShellOptions) {
  return (
    <main data-openapi-base-url={client.getConfig().baseUrl}>
      <h1>DSGeorref</h1>
      {children}
    </main>
  );
}
