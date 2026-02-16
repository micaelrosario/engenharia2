from dataclasses import dataclass

@dataclass
class Tarefa:
    id: int
    titulo: str
    feito: bool = False
