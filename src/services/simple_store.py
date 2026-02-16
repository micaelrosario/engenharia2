from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

try:
    # Quando importado como pacote (src.services.simple_store)
    from ..persistence.json_store import JsonListStore
except ImportError:  # pragma: no cover
    # Quando executado com a pasta src no sys.path
    from persistence.json_store import JsonListStore


class ArmazenamentoSimples:
    """Camada de backend para tarefas (sem UI).

    Mantém compatibilidade com o projeto atual: `tarefas` é uma lista de dicionários
    com chaves como `titulo`, `feito` (e opcionalmente `id`).
    """

    def __init__(self, caminho_arquivo: Path):
        self.caminho_arquivo = Path(caminho_arquivo)
        self._store = JsonListStore(self.caminho_arquivo, default=[])
        self.tarefas: List[Dict[str, Any]] = []
        self.carregar()

    def carregar(self) -> None:
        self.tarefas = self._store.carregar()

    def salvar(self) -> bool:
        self._store.salvar(self.tarefas)
        return self.caminho_arquivo.exists()

    def adicionar(self, titulo: str) -> None:
        titulo = titulo.strip()
        if not titulo:
            return
        self.tarefas.append({"titulo": titulo, "feito": False})
        self.salvar()

    def remover(self, indice: int) -> None:
        if 0 <= indice < len(self.tarefas):
            self.tarefas.pop(indice)
            self.salvar()

    def alternar_status(self, indice: int) -> None:
        if 0 <= indice < len(self.tarefas):
            atual = bool(self.tarefas[indice].get("feito"))
            self.tarefas[indice]["feito"] = not atual
            self.salvar()
