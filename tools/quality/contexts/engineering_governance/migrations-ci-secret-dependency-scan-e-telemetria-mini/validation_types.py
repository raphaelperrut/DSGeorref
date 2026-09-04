from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class Finding:
    code: str
    artifact: str
    detail: str

    def as_dict(self) -> dict[str, str]:
        return {"artifact": self.artifact, "code": self.code, "detail": self.detail}
