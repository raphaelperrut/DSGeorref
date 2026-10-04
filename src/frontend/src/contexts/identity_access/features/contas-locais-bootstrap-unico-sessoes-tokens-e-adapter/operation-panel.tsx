import { useId, useState, type ComponentProps, type ReactNode } from "react";
import type { Outcome } from "./use-identity-access";

export function Field({ label, ...props }: ComponentProps<"input"> & { label: string }) {
  const id = useId();
  return <label htmlFor={id}>{label}<input id={id} {...props} /></label>;
}
export function Feedback({ outcome, children }: { outcome: Outcome<unknown> | undefined; children?: ReactNode }) {
  if (!outcome) return null;
  if (outcome.phase === "pending") return <p role="status">Enviando pedido…</p>;
  if (outcome.phase === "success") return <div role="status">{children}</div>;
  const problem = outcome.problem;
  return <div role="alert" className="identity-error">
    <p>{outcome.message}</p>
    {problem && <>
      <strong>{problem.status === 401 ? "Autenticação recusada" : problem.status === 403 ? "Autorização recusada" : problem.title}</strong>
      {problem.code === "bootstrap_already_completed" && <p>Bootstrap já realizado; nova execução rejeitada.</p>}
      <dl>
        <dt>type</dt><dd>{problem.type}</dd><dt>title</dt><dd>{problem.title}</dd>
        <dt>status</dt><dd>{problem.status}</dd>
        {problem.detail !== undefined && <><dt>detail</dt><dd>{problem.detail}</dd></>}
        {problem.instance !== undefined && <><dt>instance</dt><dd>{problem.instance}</dd></>}
      </dl>
    </>}
  </div>;
}
export function OperationPanel({ title, action, children, result, outcome, disabled, submit }: {
  title: string; action: string; children: ReactNode; result?: ReactNode;
  outcome?: Outcome<unknown> | undefined; disabled: boolean;
  submit: (values: FormData, key: string) => Promise<boolean>;
}) {
  const [key, setKey] = useState(() => crypto.randomUUID());
  return <section aria-label={title}>
    <h3>{title}</h3>
    <form aria-label={title} onInput={() => setKey(crypto.randomUUID())} onSubmit={event => {
      event.preventDefault();
      if (disabled) return;
      const form = event.currentTarget;
      // Unchanged retries retain their key. Editing the payload creates a new intention.
      void submit(new FormData(form), key).then(success => {
        if (success) { form.reset(); setKey(crypto.randomUUID()); }
      });
    }}>
      <fieldset disabled={disabled}>{children}<button type="submit">{action}</button></fieldset>
    </form>
    <Feedback outcome={outcome}>{result}</Feedback>
  </section>;
}
