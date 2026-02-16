from __future__ import annotations

from dataclasses import replace
from typing import Any, Dict, List

from src.models.tarefa import Tarefa
from src.persistence.base import BaseStore


class TarefaService:
    """Regras de negócio para tarefas (independente de UI).

    - Mantém as tarefas em memória como `List[Tarefa]`.
    - Persiste usando um `BaseStore` que salva/carrega `List[dict]`.

    Nesta etapa, o formato persistido continua compatível com o JSON atual:
    `{titulo: str, feito: bool}` (id é opcional).
    """

    def __init__(self, store: BaseStore[Dict[str, Any]]):
        self._store = store
        self._tarefas: List[Tarefa] = []

    @property
    def tarefas(self) -> List[Tarefa]:
        return list(self._tarefas)

    def carregar(self) -> None:
        dados = self._store.carregar()
        self._tarefas = [Tarefa.from_dict(d) for d in dados if isinstance(d, dict)]

    def salvar(self) -> None:
        self._store.salvar([t.to_dict() for t in self._tarefas])

    def set_from_dicts(self, tarefas: List[Dict[str, Any]]) -> None:
        self._tarefas = [Tarefa.from_dict(t) for t in tarefas if isinstance(t, dict)]

    def to_dicts(self) -> List[Dict[str, Any]]:
        return [t.to_dict() for t in self._tarefas]

    def adicionar(self, titulo: str) -> None:
        titulo = (titulo or "").strip()
        if not titulo:
            return
        self._tarefas.append(Tarefa(titulo=titulo, feito=False, id=None))
        self.salvar()

    def remover_por_indice(self, indice: int) -> None:
        if 0 <= indice < len(self._tarefas):
            self._tarefas.pop(indice)
            self.salvar()

    def alternar_status_por_indice(self, indice: int) -> None:
        if 0 <= indice < len(self._tarefas):
            atual = self._tarefas[indice]
            self._tarefas[indice] = replace(atual, feito=not atual.feito)
            self.salvar()
