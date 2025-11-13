import json
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QListWidget, QMessageBox
)
from style import apply_app_style, style_buttons, style_task_input, style_task_list


# === Classe responsável por salvar e carregar tarefas ===
class ArmazenamentoSimples:
    """Gerencia o armazenamento de tarefas em arquivo JSON."""

    def __init__(self, caminho_arquivo: Path):
        self.caminho_arquivo = Path(caminho_arquivo)
        self.tarefas = []
        self.carregar()

    def carregar(self):
        """Carrega as tarefas do arquivo JSON, se existir."""
        if not self.caminho_arquivo.exists():
            self.tarefas = []
            return

        try:
            with self.caminho_arquivo.open("r", encoding="utf-8") as f:
                self.tarefas = json.load(f)
            # Garante que o conteúdo é uma lista
            if not isinstance(self.tarefas, list):
                self.tarefas = []
        except (json.JSONDecodeError, OSError): # pragma: no cover
            # Se o arquivo estiver corrompido ou ilegível, começa vazio
            self.tarefas = []

    def salvar(self):
        """Salva as tarefas em um arquivo JSON."""
        pasta_pai = self.caminho_arquivo.parent

        # Garante que o diretório pai existe e é válido
        if pasta_pai.exists() and not pasta_pai.is_dir():
            raise FileExistsError(f"O caminho pai '{pasta_pai}' é um arquivo, não um diretório.")

        pasta_pai.mkdir(parents=True, exist_ok=True)

        # Salva o JSON com indentação legível
        with self.caminho_arquivo.open("w", encoding="utf-8") as f:
            json.dump(self.tarefas, f, ensure_ascii=False, indent=4)

        return self.caminho_arquivo.exists()

    def adicionar(self, titulo: str):
        """Adiciona uma nova tarefa e salva no arquivo."""
        titulo = titulo.strip()
        if not titulo:
            return
        self.tarefas.append({"titulo": titulo, "feito": False})
        self.salvar()

    def remover(self, indice: int):
        """Remove uma tarefa pelo índice, se existir."""
        if 0 <= indice < len(self.tarefas):
            self.tarefas.pop(indice)
            self.salvar()

    def alternar_status(self, indice: int):
        """Alterna o status de conclusão de uma tarefa."""
        if 0 <= indice < len(self.tarefas):
            self.tarefas[indice]["feito"] = not self.tarefas[indice]["feito"]
            self.salvar()


# === Classe principal da aplicação ===
class AplicativoTarefas(QWidget):
    """Interface principal do aplicativo de lista de tarefas."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lista de Tarefas 📝")
        self.definir_tamanho_janela()
        self.armazenamento = ArmazenamentoSimples(Path("dados/tarefas.json"))
        self.configurar_interface()
        self.carregar_tarefas_salvas()

    def definir_tamanho_janela(self):
        """Define o tamanho e as restrições da janela."""
        self.resize(400, 500)
        self.setMinimumWidth(350)

    def configurar_interface(self):
        """Cria e organiza os elementos visuais da interface."""
        layout_principal = QVBoxLayout()
        layout_input = QHBoxLayout()

        # Campo de entrada de texto
        self.campo_tarefa = QLineEdit()
        self.campo_tarefa.setPlaceholderText("Digite uma nova tarefa...")
        style_task_input(self.campo_tarefa)

        # Botões
        self.botao_adicionar = QPushButton("Adicionar")
        self.botao_remover = QPushButton("Remover")
        style_buttons([self.botao_adicionar, self.botao_remover])

        # Lista de tarefas
        self.lista_tarefas = QListWidget()
        style_task_list(self.lista_tarefas)

        # Organização no layout
        layout_input.addWidget(self.campo_tarefa)
        layout_input.addWidget(self.botao_adicionar)
        layout_principal.addLayout(layout_input)
        layout_principal.addWidget(self.lista_tarefas)
        layout_principal.addWidget(self.botao_remover)
        self.setLayout(layout_principal)

        # Conexões de eventos
        self.botao_adicionar.clicked.connect(self.adicionar_tarefa)
        self.botao_remover.clicked.connect(self.remover_tarefa)
        self.lista_tarefas.itemDoubleClicked.connect(self.alternar_status_tarefa)

    def carregar_tarefas_salvas(self):
        """Atualiza a lista exibida com as tarefas armazenadas."""
        self.lista_tarefas.clear()
        for tarefa in self.armazenamento.tarefas:
            texto = tarefa["titulo"]
            if tarefa.get("feito"):
                texto += " ✅"
            self.lista_tarefas.addItem(texto)

    def adicionar_tarefa(self):
        """Adiciona uma nova tarefa usando o campo de texto."""
        titulo = self.campo_tarefa.text().strip()
        if not titulo:
            QMessageBox.warning(self, "Aviso", "Digite uma tarefa antes de adicionar.")
            return
        self.armazenamento.adicionar(titulo)
        self.campo_tarefa.clear()
        self.carregar_tarefas_salvas()

    def remover_tarefa(self):
        """Remove a tarefa selecionada."""
        indice = self.lista_tarefas.currentRow()
        if indice < 0:
            QMessageBox.warning(self, "Aviso", "Selecione uma tarefa para remover.")
            return
        self.armazenamento.remover(indice)
        self.carregar_tarefas_salvas()

    def alternar_status_tarefa(self, item):
        """Alterna o status de conclusão da tarefa clicada duas vezes."""
        indice = self.lista_tarefas.row(item)
        self.armazenamento.alternar_status(indice)
        self.carregar_tarefas_salvas()


# === Execução principal ===
if __name__ == "__main__": # pragma: no cover
    app = QApplication([])
    apply_app_style(app)
    janela = AplicativoTarefas()
    janela.show()
    app.exec_()
