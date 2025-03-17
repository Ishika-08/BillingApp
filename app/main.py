import sys
from PySide6.QtWidgets import QApplication
from app.ui import BillingUI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BillingUI()
    window.show()
    sys.exit(app.exec())
