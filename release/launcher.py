"""Entry point used by PyInstaller builds."""
import multiprocessing
import sys

multiprocessing.freeze_support()

# ──────────────────────────────────────────────────────────────────────────────
# Fork-Bomb-Schutz
# In einem PyInstaller-Bundle ist sys.executable die App selbst (kein Python).
# Wird sie versehentlich als Interpreter gestartet ("App -i", "App -m mpremote",
# "App -c ..."), darf sie NICHT die GUI öffnen – sonst startet sich die App
# rekursiv immer wieder neu (Endlosschleife, kann den Rechner zum Absturz
# bringen). In diesem Fall sofort und sauber beenden.
# ──────────────────────────────────────────────────────────────────────────────
if getattr(sys, "frozen", False) and len(sys.argv) > 1 and sys.argv[1] in ("-i", "-m", "-c"):
    sys.stderr.write(
        "NIT_Code wurde fälschlich als Python-Interpreter aufgerufen "
        f"({' '.join(sys.argv[1:])}). Beende, um eine Endlosschleife zu verhindern.\n"
    )
    sys.exit(0)

from nit_code.main import main


if __name__ == "__main__":
    main()
