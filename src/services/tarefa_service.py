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

    @staticmethod
    def _normalizar_titulo(titulo: str) -> str:
        return (titulo or "").strip()

    @staticmethod
    def _titulo_valido(titulo: str) -> bool:
        return bool(TarefaService._normalizar_titulo(titulo))

    @property
    def tarefas(self) -> List[Tarefa]:
        return list(self._tarefas)

    def carregar(self) -> None:
        dados = self._store.carregar()
        tarefas = [Tarefa.from_dict(d) for d in dados]
        tarefas_validas = [t for t in tarefas if t.titulo]
        self._tarefas = tarefas_validas

        # Remove registros "fantasmas" (títulos vazios/apenas espaços) do arquivo.
        if len(tarefas_validas) != len(tarefas):
            self.salvar()

    def salvar(self) -> None:
        # Defesa extra: nunca persiste tarefas vazias.
        self._tarefas = [t for t in self._tarefas if t.titulo]
        self._store.salvar([t.to_dict() for t in self._tarefas])

    def set_from_dicts(self, tarefas: List[Dict[str, Any]]) -> None:
        parsed = [Tarefa.from_dict(t) for t in tarefas]
        self._tarefas = [t for t in parsed if t.titulo]

    def to_dicts(self) -> List[Dict[str, Any]]:
        return [t.to_dict() for t in self._tarefas]

    def adicionar(self, titulo: str) -> bool:
        titulo = self._normalizar_titulo(titulo)
        if not titulo:
            return False

        if any(t.titulo == titulo for t in self._tarefas):
            return False

        self._tarefas.append(Tarefa(titulo=titulo, feito=False, id=None))
        self.salvar()
        return True

    def remover_por_indice(self, indice: int) -> None:
        if 0 <= indice < len(self._tarefas):
            self._tarefas.pop(indice)
            self.salvar()

    def alternar_status_por_indice(self, indice: int) -> None:
        if 0 <= indice < len(self._tarefas):
            atual = self._tarefas[indice]
            self._tarefas[indice] = replace(atual, feito=not atual.feito)
            self.salvar()
