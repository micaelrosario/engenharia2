import json
from pathlib import Path


class ArmazenamentoSimples:
    """Classe responsável por armazenar e gerenciar tarefas em um arquivo JSON."""

    def __init__(self, caminho_arquivo):
        self.caminho_arquivo = Path(caminho_arquivo)
        self.tarefas = []
        self.carregar()  # Sempre tenta carregar ao iniciar

    def carregar(self):
        """Carrega as tarefas do arquivo JSON, se existir."""
        if not self.caminho_arquivo.exists():
            self.tarefas = []
            return

        try:
            with self.caminho_arquivo.open("r", encoding="utf-8") as f:
                self.tarefas = json.load(f)
            if not isinstance(self.tarefas, list):
                # Se o arquivo não contém uma lista, zera o conteúdo
                self.tarefas = []
        except (json.JSONDecodeError, OSError):
            self.tarefas = []

    def salvar(self):
        """Salva as tarefas em arquivo JSON, criando diretórios se necessário."""
        pasta_pai = self.caminho_arquivo.parent

        # Se o pai for um arquivo, lança erro conforme os testes esperam
        if pasta_pai.exists() and not pasta_pai.is_dir():
            raise FileExistsError(f"O caminho pai '{pasta_pai}' é um arquivo, não um diretório.")

        try:
            pasta_pai.mkdir(parents=True, exist_ok=True)
        except Exception:
            # Caso aconteça algo inesperado, apenas propaga
            raise

        with self.caminho_arquivo.open("w", encoding="utf-8") as f:
            json.dump(self.tarefas, f, ensure_ascii=False, indent=2)

    def adicionar(self, titulo):
        """Adiciona uma nova tarefa e salva automaticamente."""
        nova_tarefa = {"titulo": titulo, "feito": False}
        self.tarefas.append(nova_tarefa)
        self.salvar()

    def remover(self, indice):
        """Remove uma tarefa da lista e salva as alterações."""
        if 0 <= indice < len(self.tarefas):
            self.tarefas.pop(indice)
            self.salvar()

    def alternar_status(self, indice):
        """Alterna o estado 'feito' de uma tarefa."""
        if 0 <= indice < len(self.tarefas):
            self.tarefas[indice]["feito"] = not self.tarefas[indice]["feito"]
            self.salvar()
