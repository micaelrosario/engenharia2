from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtCore import Qt


# === Estilo dos botões com efeito hover ===
def estilo_botoes():
    return """
        QPushButton {
            background-color: #2d2d2d;
            color: white;
            border: 2px solid #444;
            border-radius: 8px;
            padding: 10px 14px;
            min-height: 40px;
            font-size: 13pt;
        }
        QPushButton:hover {
            background-color: #3d3d3d;
            color: white;
            border: 2px solid #00aaff;
        }
    """


# === Paleta de cores para tema escuro ===
def paleta_escura():
    paleta = QPalette()
    paleta.setColor(QPalette.Window, QColor(30, 30, 30))        # Cor do fundo da janela
    paleta.setColor(QPalette.WindowText, Qt.white)              # Cor do texto geral
    paleta.setColor(QPalette.Base, QColor(20, 20, 20))          # Fundo dos campos de texto
    paleta.setColor(QPalette.Text, Qt.black)                    # Texto digitado nos campos
    paleta.setColor(QPalette.Button, QColor(45, 45, 45))        # Cor dos botões
    paleta.setColor(QPalette.ButtonText, Qt.white)              # Texto dos botões
    paleta.setColor(QPalette.Highlight, QColor(0, 170, 255))    # Cor de destaque (seleção)
    paleta.setColor(QPalette.HighlightedText, Qt.white)         # Texto em destaque
    return paleta


# === Aplica tema global e fonte base ===
def apply_app_style(app, base_font_pt: int = 11):
    """Aplica paleta e fonte global à aplicação Qt."""
    if not app:
        raise ValueError("Objeto 'app' inválido: aplicação Qt não fornecida.")
    
    f = QFont()
    f.setPointSize(base_font_pt)
    app.setFont(f)

    paleta = paleta_escura()
    app.setPalette(paleta)


# === Aplica estilo consistente aos botões ===
def style_buttons(buttons, min_height: int = 44, font_pt: int = 13):
    """Aplica estilo consistente a uma lista de botões."""
    if not buttons:
        return
    
    for b in buttons:
        if b is None:
            continue
        bf = b.font() or QFont()
        bf.setPointSize(font_pt)
        b.setFont(bf)
        b.setMinimumHeight(min_height)
        b.setStyleSheet(estilo_botoes())


# === Estilo do campo de entrada de tarefas ===
def style_task_input(inp, height: int = 44, font_pt: int = 14):
    """Aplica altura e fonte ao campo de entrada."""
    if inp is None:
        return
    
    inp.setFixedHeight(height)
    f = inp.font() or QFont()
    f.setPointSize(font_pt)
    inp.setFont(f)


# === Estilo da lista de tarefas ===
def style_task_list(lst, font_pt: int = 13, item_height: int = 36, bg_color: str = "#ffffff"):
    """Aplica estilo visual à lista de tarefas."""
    if lst is None:
        return
    
    f = lst.font() or QFont()
    f.setPointSize(font_pt)
    lst.setFont(f)

    # padding e cor de fundo (personalizável)
    lst.setStyleSheet(
        f"""
        QListWidget {{
            padding: 6px;
            background: {bg_color};
        }}
        QListWidget::item {{
            padding: 8px 6px;
            height: {item_height}px;
        }}
        """
    )
