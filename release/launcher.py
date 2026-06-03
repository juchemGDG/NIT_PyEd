"""Entry point used by PyInstaller builds."""
import multiprocessing
multiprocessing.freeze_support()

from nit_code.main import main


if __name__ == "__main__":
    main()
