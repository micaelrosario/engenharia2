import json
from pathlib import Path


class ArmazenamentoSimples:
    """Classe responsável por armazenar e gerenciar tarefas em um arquivo JSON."""

    def __init__(self, caminho_arquivo):
        self.caminho_arquivo = Path(caminho_arquivo)
        self.tarefas = []
        self.carregar()  # tenta carregar ao iniciar

    def carregar(self):
        """Carrega as tarefas do arquivo JSON, se existir e for válido."""
        if not self.caminho_arquivo.exists():
            self.tarefas = []
            return

        try:
            with self.caminho_arquivo.open("r", encoding="utf-8") as f:
                dados = json.load(f)
                # garante que é uma lista válida
                self.tarefas = dados if isinstance(dados, list) else []
        except (json.JSONDecodeError, OSError):
            self.tarefas = []

    def salvar(self):
        """Salva as tarefas em um arquivo JSON, criando diretórios se necessário."""
        pasta_pai = self.caminho_arquivo.parent

        # Caso o diretório pai seja um arquivo comum, gera o erro esperado nos testes
        if pasta_pai.exists() and not pasta_pai.is_dir():
            raise FileExistsError(f"O caminho pai '{pasta_pai}' é um arquivo, não um diretório.")

        # Cria diretórios pai, se necessário
        pasta_pai.mkdir(parents=True, exist_ok=True)

        with self.caminho_arquivo.open("w", encoding="utf-8") as f:
            json.dump(self.tarefas, f, ensure_ascii=False, indent=2)

    def adicionar(self, titulo):
        """Adiciona uma nova tarefa e salva imediatamente."""
        tarefa = {"titulo": titulo, "feito": False}
        self.tarefas.append(tarefa)
        self.salvar()
        return tarefa

    def remover(self, indice):
        """Remove uma tarefa pelo índice."""
        if 0 <= indice < len(self.tarefas):
            self.tarefas.pop(indice)
            self.salvar()

    def alternar_status(self, indice):
        """Alterna o estado 'feito' da tarefa."""
        if 0 <= indice < len(self.tarefas):
            self.tarefas[indice]["feito"] = not self.tarefas[indice]["feito"]
            self.salvar()
