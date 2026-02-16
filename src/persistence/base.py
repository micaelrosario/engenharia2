from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar

T = TypeVar("T")


class BaseStore(ABC, Generic[T]):
    @abstractmethod
    def carregar(self) -> List[T]:
        raise NotImplementedError

    @abstractmethod
    def salvar(self, itens: List[T]) -> None:
        raise NotImplementedError
