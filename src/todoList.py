import json
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QListWidget, QMessageBox
)
from src.style import apply_app_style, style_buttons, style_task_input, style_task_list


# === Classe para lidar com armazenamento em JSON ===
class ArmazenamentoSimples:
    def __init__(self, caminho_arquivo: Path):
        self.caminho_arquivo = Path(caminho_arquivo)
        self.tarefas = []
        self.carregar() 

    def carregar(self):
        """Lê o arquivo JSON e carrega as tarefas."""
        if not self.caminho_arquivo.exists():
            self.tarefas = []
            return

        try:
            with self.caminho_arquivo.open("r", encoding="utf-8") as f:
                self.tarefas = json.load(f)
        except Exception:
            # Se o arquivo estiver corrompido ou ilegível, começa vazio
            self.tarefas = []

    def salvar(self):
        """Salva as tarefas em JSON no caminho especificado."""
        caminho_pai = self.caminho_arquivo.parent

        # Se o diretório pai for um arquivo, lançar erro
        if caminho_pai.exists() and caminho_pai.is_file():
            raise FileExistsError(f"O caminho pai '{caminho_pai}' é um arquivo, não um diretório.")

        # Cria pastas pai se necessário
        caminho_pai.mkdir(parents=True, exist_ok=True)

        # Salva o JSON com indentação e encoding UTF-8
        with self.caminho_arquivo.open("w", encoding="utf-8") as f:
            json.dump(self.tarefas, f, ensure_ascii=False, indent=4)

        # Verifica se o arquivo foi criado corretamente
        return self.caminho_arquivo.exists()

    def adicionar(self, titulo: str):
        """Adiciona uma nova tarefa à lista e salva."""
        if not titulo.strip():
            return
        self.tarefas.append({"titulo": titulo, "feito": False})
        self.salvar()

    def remover(self, indice: int):
        """Remove uma tarefa pelo índice."""
        if 0 <= indice < len(self.tarefas):
            self.tarefas.pop(indice)
            self.salvar()

    def alternar_status(self, indice: int):
        """Marca ou desmarca uma tarefa como concluída."""
        if 0 <= indice < len(self.tarefas):
            self.tarefas[indice]["feito"] = not self.tarefas[indice]["feito"]
            self.salvar()


# === Classe principal da aplicação ===
class AplicativoTarefas(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lista de Tarefas 📝")
        self.redimensionar_tela()
        self.armazenamento = ArmazenamentoSimples()
        self.configurar_ui()
        self.carregar_tarefas_salvas()

    def redimensionar_tela(self):
        """Define tamanho e posição padrão da janela."""
        self.resize(400, 500)
        self.setMinimumWidth(350)

    def configurar_ui(self):
        """Cria e estiliza os elementos da interface."""
        layout_principal = QVBoxLayout()
        layout_input = QHBoxLayout()

        # Campo de entrada
        self.campo_tarefa = QLineEdit()
        self.campo_tarefa.setPlaceholderText("Digite uma nova tarefa...")
        style_task_input(self.campo_tarefa)

        # Botões
        self.botao_adicionar = QPushButton("Adicionar")
        self.botao_remover = QPushButton("Remover")
        style_buttons([self.botao_adicionar, self.botao_remover])

        # Lista
        self.lista_tarefas = QListWidget()
        style_task_list(self.lista_tarefas)

        # Organização
        layout_input.addWidget(self.campo_tarefa)
        layout_input.addWidget(self.botao_adicionar)
        layout_principal.addLayout(layout_input)
        layout_principal.addWidget(self.lista_tarefas)
        layout_principal.addWidget(self.botao_remover)
        self.setLayout(layout_principal)

        # Eventos
        self.botao_adicionar.clicked.connect(self.adicionar_tarefa)
        self.botao_remover.clicked.connect(self.remover_tarefa)
        self.lista_tarefas.itemDoubleClicked.connect(self.alternar_status_tarefa)

    def carregar_tarefas_salvas(self):
        """Exibe na interface as tarefas que já estavam salvas."""
        self.lista_tarefas.clear()
        for t in self.armazenamento.tarefas:
            texto = t["titulo"]
            if t["feito"]:
                texto += " ✅"
            self.lista_tarefas.addItem(texto)

    def adicionar_tarefa(self):
        """Adiciona nova tarefa a partir do campo de entrada."""
        titulo = self.campo_tarefa.text().strip()
        if not titulo:
            QMessageBox.warning(self, "Aviso", "Digite uma tarefa antes de adicionar.")
            return
        self.armazenamento.adicionar(titulo)
        self.campo_tarefa.clear()
        self.carregar_tarefas_salvas()

    def remover_tarefa(self):
        """Remove a tarefa selecionada da lista."""
        indice = self.lista_tarefas.currentRow()
        if indice < 0:
            QMessageBox.warning(self, "Aviso", "Selecione uma tarefa para remover.")
            return
        self.armazenamento.remover(indice)
        self.carregar_tarefas_salvas()

    def alternar_status_tarefa(self, item):
        """Alterna o status de concluído ao dar duplo clique."""
        indice = self.lista_tarefas.row(item)
        self.armazenamento.alternar_status(indice)
        self.carregar_tarefas_salvas()


# === Execução da aplicação ===
if __name__ == "__main__":
    app = QApplication([])
    apply_app_style(app)
    janela = AplicativoTarefas()
    janela.show()
    app.exec_()
