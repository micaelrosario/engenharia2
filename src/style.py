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


def apply_app_style(app, base_font_pt: int = 11):
    """Aplica paleta e fonte global à aplicação Qt."""
    try:
        f = QFont()
        f.setPointSize(base_font_pt)
        app.setFont(f)
    except Exception:
        pass
    try:
        app.setPalette(paleta_escura())
    except Exception:
        pass


def style_buttons(buttons, min_height: int = 44, font_pt: int = 13):
    """Aplica estilo consistente a uma lista de botões."""
    for b in buttons:
        try:
            b.setMinimumHeight(min_height)
            bf = b.font() or QFont()
            bf.setPointSize(font_pt)
            b.setFont(bf)
            b.setStyleSheet(estilo_botoes())
        except Exception:
            pass


def style_task_input(inp, height: int = 44, font_pt: int = 14):
    try:
        inp.setFixedHeight(height)
        f = inp.font() or QFont()
        f.setPointSize(font_pt)
        inp.setFont(f)
    except Exception:
        pass


def style_task_list(lst, font_pt: int = 13, item_height: int = 36, bg_color: str = "#ffffff"):
    try:
        f = lst.font() or QFont()
        f.setPointSize(font_pt)
        lst.setFont(f)
        # padding e fundo (bg_color pode ser alterado)
        lst.setStyleSheet(f"QListWidget {{ padding: 6px; background: {bg_color}; }} QListWidget::item {{ padding: 8px 6px; height: {item_height}px; }}")
    except Exception:
        pass