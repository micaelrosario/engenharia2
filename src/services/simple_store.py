from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

try:
    # Quando importado como pacote (src.services.simple_store)
    from ..persistence.json_store import JsonListStore
except ImportError:  # pragma: no cover
    # Quando executado com a pasta src no sys.path
    from persistence.json_store import JsonListStore

try:
    from .tarefa_service import TarefaService
except ImportError:  # pragma: no cover
    from services.tarefa_service import TarefaService


class ArmazenamentoSimples:
    """Camada de backend para tarefas (sem UI).

    Mantém compatibilidade com o projeto atual: `tarefas` é uma lista de dicionários
    com chaves como `titulo`, `feito` (e opcionalmente `id`).
    """

    def __init__(self, caminho_arquivo: Path):
        self.caminho_arquivo = Path(caminho_arquivo)
        self._store = JsonListStore(self.caminho_arquivo, default=[])
        self._service = TarefaService(self._store)
        self.carregar()

    @property
    def tarefas(self) -> List[Dict[str, Any]]:
        return self._service.to_dicts()

    @tarefas.setter
    def tarefas(self, value: List[Dict[str, Any]]) -> None:
        self._service.set_from_dicts(value)

    def carregar(self) -> None:
        self._service.carregar()

    def salvar(self) -> bool:
        self._service.salvar()
        return self.caminho_arquivo.exists()

    def adicionar(self, titulo: str) -> bool:
        return self._service.adicionar(titulo)

    def remover(self, indice: int) -> None:
        self._service.remover_por_indice(indice)

    def alternar_status(self, indice: int) -> None:
        self._service.alternar_status_por_indice(indice)
