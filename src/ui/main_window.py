from __future__ import annotations

from pathlib import Path

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QListWidget,
    QMessageBox,
)

try:
    # Quando importado como pacote (src.ui.main_window)
    from ..services.simple_store import ArmazenamentoSimples
except ImportError:  # pragma: no cover
    # Quando executado com a pasta src no sys.path
    from services.simple_store import ArmazenamentoSimples

try:
    # Quando importado como pacote
    from ..style import style_buttons, style_task_input, style_task_list
except ImportError:  # pragma: no cover
    # Quando executado com a pasta src no sys.path
    from style import style_buttons, style_task_input, style_task_list


class AplicativoTarefas(QWidget):
    """Interface principal do aplicativo de lista de tarefas."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lista de Tarefas 📝")
        self._definir_tamanho_janela()
        self.armazenamento = ArmazenamentoSimples(Path("dados/tarefas.json"))
        self._configurar_interface()
        self._carregar_tarefas_salvas()

    def _definir_tamanho_janela(self) -> None:
        self.resize(400, 500)
        self.setMinimumWidth(350)

    def _configurar_interface(self) -> None:
        layout_principal = QVBoxLayout()
        layout_input = QHBoxLayout()

        self.campo_tarefa = QLineEdit()
        self.campo_tarefa.setPlaceholderText("Digite uma nova tarefa...")
        style_task_input(self.campo_tarefa)

        self.botao_adicionar = QPushButton("Adicionar")
        self.botao_remover = QPushButton("Remover")
        style_buttons([self.botao_adicionar, self.botao_remover])

        self.lista_tarefas = QListWidget()
        style_task_list(self.lista_tarefas)

        layout_input.addWidget(self.campo_tarefa)
        layout_input.addWidget(self.botao_adicionar)
        layout_principal.addLayout(layout_input)
        layout_principal.addWidget(self.lista_tarefas)
        layout_principal.addWidget(self.botao_remover)
        self.setLayout(layout_principal)

        self.botao_adicionar.clicked.connect(self._adicionar_tarefa)
        self.botao_remover.clicked.connect(self._remover_tarefa)
        self.lista_tarefas.itemDoubleClicked.connect(self._alternar_status_tarefa)

    def _carregar_tarefas_salvas(self) -> None:
        self.lista_tarefas.clear()
        for tarefa in self.armazenamento.tarefas:
            texto = str(tarefa.get("titulo", ""))
            if tarefa.get("feito"):
                texto += " ✅"
            self.lista_tarefas.addItem(texto)

    def _adicionar_tarefa(self) -> None:
        titulo = self.campo_tarefa.text().strip()
        if not titulo:
            QMessageBox.warning(self, "Aviso", "Digite uma tarefa antes de adicionar.")
            return
        self.armazenamento.adicionar(titulo)
        self.campo_tarefa.clear()
        self._carregar_tarefas_salvas()

    def _remover_tarefa(self) -> None:
        indice = self.lista_tarefas.currentRow()
        if indice < 0:
            QMessageBox.warning(self, "Aviso", "Selecione uma tarefa para remover.")
            return
        self.armazenamento.remover(indice)
        self._carregar_tarefas_salvas()

    def _alternar_status_tarefa(self, item) -> None:
        indice = self.lista_tarefas.row(item)
        self.armazenamento.alternar_status(indice)
        self._carregar_tarefas_salvas()
