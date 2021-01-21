from PyQt5 import QtWidgets
from oai_kpa_power import ClientGUIWindow
import sys

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    app = QtWidgets.QApplication(sys.argv)
    w = ClientGUIWindow(uniq_name="oai_kpa_power", widget='False')
    w.show()

    sys.exit(app.exec_())