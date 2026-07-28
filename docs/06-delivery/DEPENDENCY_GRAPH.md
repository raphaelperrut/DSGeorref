# Epic dependency graph

The machine-readable graph is `DEPENDENCY_GRAPH.json`. An edge `A → B` means epic A blocks epic B. The repository validator rejects missing references and cycles.

Execution order is governed by dependencies and gates, not by document order alone. The Tech Lead may pull independent epics forward only when their contracts and file scopes do not collide.
