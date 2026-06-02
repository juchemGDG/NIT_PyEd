"""AIS-Chat-Panel – eingebettete Web-Ansicht von app.ais-chat.schule."""
from PyQt6.QtCore import QUrl
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget

from .config import AIS_CHAT_URL, THEME


class AisChatPanel(QWidget):
    """Seitliches Panel mit eingebetteter AIS-Chat-Webseite."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        self.setMinimumWidth(260)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        header = QWidget()
        header.setFixedHeight(36)
        header.setStyleSheet(
            f"background:{THEME['bg_panel']};"
            f"border-bottom:1px solid {THEME['border']};"
        )
        hlay = QHBoxLayout(header)
        hlay.setContentsMargins(10, 0, 10, 0)
        title_lbl = QLabel("🏫  AIS-Chat")
        title_lbl.setStyleSheet(
            f"color:{THEME['text']}; font-weight:bold; font-size:13px;"
        )
        hlay.addWidget(title_lbl)
        layout.addWidget(header)

        # Eingebettete Web-Ansicht
        self._view = QWebEngineView()
        self._view.setUrl(QUrl(AIS_CHAT_URL))
        layout.addWidget(self._view, stretch=1)
