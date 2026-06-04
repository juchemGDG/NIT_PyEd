"""Jedi-basierte Code-Vervollständigung als Hintergrund-Thread."""
import threading

from PyQt6.QtCore import QObject, pyqtSignal

try:
    import jedi
    HAS_JEDI = True
except ImportError:
    HAS_JEDI = False


class JediCompleter(QObject):
    """Ruft jedi.Script.complete() in einem Daemon-Thread auf und emittiert die Ergebnisse."""

    completions_ready = pyqtSignal(list)  # list of (name: str, type: str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._lock = threading.Lock()
        self._seq = 0
        self._extra_paths: list[str] = []

    def set_extra_paths(self, paths: list[str]):
        """Zusätzliche sys.path-Einträge für jedi (z. B. MicroPython-Stubs)."""
        self._extra_paths = list(paths)

    def request(self, source: str, line: int, col: int, path: str | None = None):
        """Startet eine asynchrone Completion-Anfrage. line/col sind 0-basiert (wie QScintilla)."""
        if not HAS_JEDI:
            return
        with self._lock:
            self._seq += 1
            seq = self._seq
        extra = list(self._extra_paths)
        threading.Thread(
            target=self._run,
            args=(source, line + 1, col, path, extra, seq),
            daemon=True,
        ).start()

    def _run(self, source: str, line: int, col: int, path: str | None,
             extra_paths: list[str], seq: int):
        try:
            project_kwargs: dict = {}
            if extra_paths:
                project_kwargs["added_sys_path"] = extra_paths
            project = jedi.Project(".", **project_kwargs)
            script_kwargs: dict = {"project": project}
            if path:
                script_kwargs["path"] = path
            script = jedi.Script(source, **script_kwargs)
            completions = script.complete(line, col)
            results = [(c.name, c.type) for c in completions[:80]]
        except Exception:
            results = []

        with self._lock:
            if self._seq != seq:
                return  # veraltete Anfrage verwerfen
        self.completions_ready.emit(results)
