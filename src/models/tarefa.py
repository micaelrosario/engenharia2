from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass(frozen=True, slots=True)
class Tarefa:
    """Modelo de tarefa.

    `id` é opcional para manter compatibilidade com o formato atual do JSON
    (que pode não conter id). Quando `id` é None, ele não é persistido.
    """

    titulo: str
    feito: bool = False
    id: Optional[int] = None

    def __post_init__(self) -> None:
        titulo = (self.titulo or "").strip()
        object.__setattr__(self, "titulo", titulo)
        object.__setattr__(self, "feito", bool(self.feito))

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Tarefa":
        titulo = str(data.get("titulo", "")).strip()
        feito = bool(data.get("feito", False))
        raw_id = data.get("id")
        task_id = int(raw_id) if isinstance(raw_id, int) else None
        return Tarefa(titulo=titulo, feito=feito, id=task_id)

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {"titulo": self.titulo, "feito": self.feito}
        if self.id is not None:
            d["id"] = self.id
        return d
