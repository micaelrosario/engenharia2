from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from .base import BaseStore


class JsonListStore(BaseStore[Dict[str, Any]]):
    """Persistência simples: salva/carrega uma lista de dicionários em JSON."""

    def __init__(self, caminho_arquivo: Path, default: Optional[List[Dict[str, Any]]] = None):
        self.caminho_arquivo = Path(caminho_arquivo)
        self._default = default if default is not None else []

    def carregar(self) -> List[Dict[str, Any]]:
        if not self.caminho_arquivo.exists():
            return list(self._default)

        try:
            with self.caminho_arquivo.open("r", encoding="utf-8") as f:
                dados = json.load(f)
        except (json.JSONDecodeError, OSError):
            return list(self._default)

        if not isinstance(dados, list):
            return list(self._default)

        # Garante formato básico (lista de dicts). Itens inválidos são ignorados.
        return [item for item in dados if isinstance(item, dict)]

    def salvar(self, itens: List[Dict[str, Any]]) -> None:
        pasta_pai = self.caminho_arquivo.parent

        if pasta_pai.exists() and not pasta_pai.is_dir():
            raise FileExistsError(
                f"O caminho pai '{pasta_pai}' é um arquivo, não um diretório."
            )

        pasta_pai.mkdir(parents=True, exist_ok=True)

        with self.caminho_arquivo.open("w", encoding="utf-8") as f:
            json.dump(itens, f, ensure_ascii=False, indent=4)
