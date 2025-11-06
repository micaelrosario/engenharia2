import sys
import json
from pathlib import Path

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QListWidget,
    QLabel,
    QListWidgetItem,
    QHBoxLayout,
    QMessageBox,
)
from PyQt5.QtGui import QPixmap, QBrush, QFont
from PyQt5.QtCore import Qt, QSize

from style import (
    estilo_botoes,
    paleta_escura,
    apply_app_style,
    style_buttons,
    style_task_input,
    style_task_list,
)


DEFAULT_DATA = Path("tasks.json")


class SimpleStore:
    """Pequena camada de persistência interna (arquivo JSON).

    Estrutura do arquivo:
      { "tasks": [ {id, title, done}, ... ], "trash": [ {id,title,done}, ... ] }
    """

    def __init__(self, path: Path | str = DEFAULT_DATA):
        self.path = Path(path)
        self.tasks: list[dict] = [] #instancia a lista de tarefas
        self.trash: list[dict] = [] #instancia a lista da lixeira
        self.load()

    #Função para carregar os dados
    def load(self) -> None:
        if not self.path.exists():
            self.tasks = []
            self.trash = []
            return
        try:
            with self.path.open("r", encoding="utf-8") as f:
                data = json.load(f)
                self.tasks = data.get("tasks", [])
                self.trash = data.get("trash", [])
        except Exception:
            self.tasks = []
            self.trash = []

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w", encoding="utf-8") as f:
            json.dump({"tasks": self.tasks, "trash": self.trash}, f, ensure_ascii=False, indent=2)

    def _next_id(self) -> int:
        ids = [t.get("id", 0) for t in self.tasks + self.trash]
        return (max(ids) + 1) if ids else 1

    def find(self, task_id: int) -> dict | None:
        for t in self.tasks:
            if t.get("id") == task_id:
                return t
        return None

    def add(self, title: str) -> dict:
        t = {"id": self._next_id(), "title": title, "done": False}
        self.tasks.append(t)
        self.save()
        return t

    def remove(self, task_id: int) -> bool:
        for t in list(self.tasks):
            if t.get("id") == task_id:
                self.tasks.remove(t)
                self.trash.append(t)
                self.save()
                return True
        return False

    def restore(self, task_id: int) -> bool:
        for t in list(self.trash):
            if t.get("id") == task_id:
                self.trash.remove(t)
                self.tasks.append(t)
                self.save()
                return True
        return False

    def toggle(self, task_id: int) -> bool:
        for t in self.tasks:
            if t.get("id") == task_id:
                t["done"] = not bool(t.get("done"))
                self.save()
                return True
        return False

    def set_all(self, done: bool) -> None:
        """Marca todas as tarefas como done (True/False) e salva."""
        for t in self.tasks:
            t["done"] = bool(done)
        self.save()

    def clear(self) -> None:
        self.trash.extend(self.tasks)
        self.tasks = []
        self.save()


class ToDoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.store = SimpleStore()

        # Janela maior para melhor visibilidade
        self.setWindowTitle("To-Do List Dark")
        self.resize(900, 700)

        self.layout = QVBoxLayout(self)

        # Avatar (opcional)
        self.avatar_label = QLabel(alignment=Qt.AlignCenter)
        avatar_path = Path("avatar.png")
        if avatar_path.exists():
            pix = QPixmap(str(avatar_path)).scaledToWidth(140, Qt.SmoothTransformation)
            self.avatar_label.setPixmap(pix)
        else:
            self.avatar_label.setText("To-Do")
            f = QFont()
            f.setPointSize(26)
            f.setBold(True)
            self.avatar_label.setFont(f)
        self.layout.addWidget(self.avatar_label)

        # Input + add button
        h = QHBoxLayout()
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Digite uma nova tarefa...")
        # estilos do input aplicados por style.py
        # (fallbacks dentro da função lidam com ausência de propriedades)
        # self.task_input terá altura e fonte aplicadas por style_task_input
        self.add_button = QPushButton("Adicionar")
        h.addWidget(self.task_input)
        h.addWidget(self.add_button)
        self.layout.addLayout(h)

        # Lista
        self.task_list = QListWidget()
        self.layout.addWidget(self.task_list)

        # Ações
        h2 = QHBoxLayout()
        self.delete_button = QPushButton("Excluir")
        self.complete_button = QPushButton("Selecionar tudo")
        self.trash_button = QPushButton("Lixeira")
        self.clear_button = QPushButton("Limpar tudo")
        # Ordem: Selecionar tudo, Excluir, Limpar e Lixeira
        h2.addWidget(self.complete_button)
        h2.addWidget(self.delete_button)
        h2.addWidget(self.clear_button)
        h2.addWidget(self.trash_button)
        self.layout.addLayout(h2)

        # aplicar estilos via helpers do style.py
        try:
            style_task_input(self.task_input)
            style_buttons([self.add_button, self.delete_button, self.complete_button, self.trash_button, self.clear_button])
            style_task_list(self.task_list, bg_color="#ffffff")
        except Exception:
            pass

        # conexões
        self.add_button.clicked.connect(self.lida_adicao)
        self.task_input.returnPressed.connect(self.lida_adicao)
        self.delete_button.clicked.connect(self.handle_delete)
        self.complete_button.clicked.connect(self.handle_complete)
        self.trash_button.clicked.connect(self.show_trash)
        self.clear_button.clicked.connect(self.handle_clear)
        self.task_list.itemDoubleClicked.connect(self.handle_toggle)
        # itemChanged será usado para escutar mudanças nos checkboxes
        self.task_list.itemChanged.connect(self.lida_item_alterado)
        # flag para evitar loops quando atualizamos programaticamente os itens
        self._suspend_item_change = False
        self.task_list.currentItemChanged.connect(lambda cur, prev: self.atualizar_botoes_de_acao())
        self.apply_styles()
        self.refresh()

    def apply_styles(self):
        # reaplica estilos caso necessário
        try:
            style_buttons([self.add_button, self.delete_button, self.complete_button, self.trash_button, self.clear_button])
            style_task_input(self.task_input)
            style_task_list(self.task_list)
        except Exception:
            pass


    def refresh(self):
        # atualiza lista com itens checkable (checkboxes)
        self._suspend_item_change = True
        self.task_list.clear()
        for t in self.store.tasks:
            # mostrar apenas o título (sem número) para evitar confusão na ordem
            text = f"{t['title']}"
            item = QListWidgetItem(text)
            # permitir checkbox
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            item.setCheckState(Qt.Checked if t.get("done") else Qt.Unchecked)
            # fonte e strikeout para indicar concluído
            font = item.font()
            font.setPointSize(13)
            font.setStrikeOut(bool(t.get("done")))
            item.setFont(font)
            item.setSizeHint(QSize(item.sizeHint().width(), 36))
            item.setData(Qt.UserRole, t.get("id"))
            item.setForeground(QBrush(Qt.black))
            self.task_list.addItem(item)
        self._suspend_item_change = False

    def lida_adicao(self):
        title = self.task_input.text().strip()
        if not title:
            return
        self.store.add(title)
        self.task_input.clear()
        self.refresh()

    def _selected_task_id(self) -> int | None:
        it = self.task_list.currentItem()
        if not it:
            return None
        return it.data(Qt.UserRole)

    def handle_delete(self):
        tid = self._selected_task_id()
        if tid is None:
            # mostrar diálogo com texto em preto (override do estilo escuro)
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Excluir")
            msg.setText("Selecione uma tarefa primeiro.")
            # força cor do texto e dos botões para preto
            msg.setStyleSheet("QLabel{ color: #000000; } QPushButton{ color: #000000; }")
            msg.exec_()
            return
        self.store.remove(tid)
        self.refresh()

    def handle_complete(self):
        # Se existir alguma tarefa não concluída, marcar todas como concluídas.
        # Caso contrário, desmarcar todas.
        tasks = self.store.tasks
        if not tasks:
            QMessageBox.information(self, "Selecionar tudo", "Não há tarefas.")
            return
        any_undone = any(not bool(t.get("done")) for t in tasks)
        self.store.set_all(any_undone)
        self.refresh()

    def atualizar_botoes_de_acao(self):
        # O botão "Selecionar tudo" atua globalmente — habilita se houver tarefas
        try:
            self.complete_button.setText("Selecionar tudo")
            self.complete_button.setEnabled(len(self.store.tasks) > 0)
        except Exception:
            pass

    def handle_toggle(self, item: QListWidgetItem):
        tid = item.data(Qt.UserRole)
        if tid is None:
            return
        self.store.toggle(tid)
        self.refresh()

    def lida_item_alterado(self, item: QListWidgetItem) -> None:
        """Chamado quando o checkbox do item muda (usuário interage).

        Evitamos loops com a flag _suspend_item_change.
        """
        if getattr(self, "_suspend_item_change", False):
            return
        tid = item.data(Qt.UserRole)
        if tid is None:
            return
        checked = item.checkState() == Qt.Checked
        t = self.store.find(tid)
        if not t:
            return
        # se o estado atual difere, fazemos toggle na store
        if bool(t.get("done")) != checked:
            self.store.toggle(tid)
        # refletir visual (strikeout)
        f = item.font()
        f.setStrikeOut(checked)
        item.setFont(f)

    def show_trash(self):
        self.trash_window = QWidget()
        self.trash_window.setWindowTitle("Lixeira")
        # janela de lixeira maior (herda tema escuro da aplicação)
        self.trash_window.resize(600, 460)
        try:
            # aplica a paleta escura localmente para garantir visual consistente
            self.trash_window.setPalette(paleta_escura())
        except Exception:
            pass
        layout = QVBoxLayout(self.trash_window)
        lw = QListWidget()
        # aplicar estilo de lista: fundo branco no centro da janela de lixeira
        try:
            style_task_list(lw, bg_color="#ffffff")
        except Exception:
            pass
        for t in self.store.trash:
            # exibir apenas o título na lixeira para evitar numeração confusa
            text = f"{t['title']}"
            it = QListWidgetItem(text)
            it.setData(Qt.UserRole, t.get("id"))
            it.setForeground(QBrush(Qt.black))
            font = it.font()
            font.setPointSize(12)
            it.setFont(font)
            lw.addItem(it)
        btn_restore = QPushButton("Restaurar")
        btn_delete_perm = QPushButton("Excluir permanentemente")
        # aplicar estilo de botões escuros consistentes
        try:
            style_buttons([btn_restore, btn_delete_perm])
        except Exception:
            pass
        hb = QHBoxLayout()
        hb.addWidget(btn_restore)
        hb.addWidget(btn_delete_perm)
        layout.addWidget(lw)
        layout.addLayout(hb)

        def do_restore():
            it = lw.currentItem()
            if not it:
                return
            tid = it.data(Qt.UserRole)
            self.store.restore(tid)
            # atualizar lista
            lw.takeItem(lw.row(it))
            self.refresh()

        def do_delete_perm():
            it = lw.currentItem()
            if not it:
                return
            tid = it.data(Qt.UserRole)
            # remover definitivamente
            self.store.trash = [x for x in self.store.trash if x.get("id") != tid]
            self.store.save()
            lw.takeItem(lw.row(it))

        btn_restore.clicked.connect(do_restore)
        btn_delete_perm.clicked.connect(do_delete_perm)

        self.trash_window.show()

    def handle_clear(self):
        # usar um QMessageBox customizado com texto preto para o tema escuro
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle("Limpar")
        msg.setText("Mover todas as tarefas para a lixeira?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        try:
            msg.setStyleSheet("QLabel{ color: #000000; } QPushButton{ color: #000000; }")
        except Exception:
            pass
        resp = msg.exec_()
        if resp == QMessageBox.Yes:
            self.store.clear()
            self.refresh()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # aplica estilo global (fonte + paleta)
    try:
        apply_app_style(app, base_font_pt=11)
    except Exception:
        # fallback: set font directly
        gf = QFont()
        gf.setPointSize(11)
        app.setFont(gf)
    window = ToDoApp()
    window.show()
    sys.exit(app.exec_())
