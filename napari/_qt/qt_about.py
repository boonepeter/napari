from qtpy import QtGui
from qtpy.QtCore import Qt
from qtpy.QtWidgets import (
    QVBoxLayout,
    QTextEdit,
    QDialog,
    QLabel,
    QPushButton,
    QHBoxLayout,
)

from ..utils import sys_info, citation_text


class QtAbout(QDialog):
    """Qt dialog window for displaying 'About napari' information.

    Attributes
    ----------
    citationCopyButton : napari._qt.qt_about.QtCopyToClipboardButton
        Button to copy citation information to the clipboard.
    citationTextBox : qtpy.QtWidgets.QTextEdit
        Text box containing napari citation information.
    citation_layout : qtpy.QtWidgets.QHBoxLayout
        Layout widget for napari citation information.
    infoCopyButton : napari._qt.qt_about.QtCopyToClipboardButton
        Button to copy napari version information to the clipboard.
    info_layout : qtpy.QtWidgets.QHBoxLayout
        Layout widget for napari version information.
    infoTextBox : qtpy.QtWidgets.QTextEdit
        Text box containing napari version information.
    layout : qtpy.QtWidgets.QVBoxLayout
        Layout widget for the entire 'About napari' dialog.
    """

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        # Description
        title_label = QLabel(
            "<b>napari: a multi-dimensional image viewer for python</b>"
        )
        title_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.layout.addWidget(title_label)

        # Add information
        self.infoTextBox = QTextEdit()
        self.infoTextBox.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.infoTextBox.setLineWrapMode(QTextEdit.NoWrap)
        # Add text copy button
        self.infoCopyButton = QtCopyToClipboardButton(self.infoTextBox)
        self.info_layout = QHBoxLayout()
        self.info_layout.addWidget(self.infoTextBox, 1)
        self.info_layout.addWidget(self.infoCopyButton, 0, Qt.AlignTop)
        self.info_layout.setAlignment(Qt.AlignTop)
        self.layout.addLayout(self.info_layout)

        self.infoTextBox.setText(sys_info(as_html=True))
        self.infoTextBox.setMinimumSize(
            self.infoTextBox.document().size().width() + 19,
            self.infoTextBox.document().size().height() + 10,
        )

        self.layout.addWidget(QLabel('<b>citation information:</b>'))
        self.citationTextBox = QTextEdit(citation_text)
        self.citationTextBox.setFixedHeight(64)
        self.citationCopyButton = QtCopyToClipboardButton(self.citationTextBox)
        self.citation_layout = QHBoxLayout()
        self.citation_layout.addWidget(self.citationTextBox, 1)
        self.citation_layout.addWidget(self.citationCopyButton, 0, Qt.AlignTop)
        self.layout.addLayout(self.citation_layout)

        self.setLayout(self.layout)

    @staticmethod
    def showAbout(qt_viewer):
        """Display the 'About napari' dialog box.

        Paramters
        ---------
        qt_viewer : QtViewer
            QtViewer instance that the `About napari` dialog box belongs to.
        """
        d = QtAbout()
        d.setObjectName('QtAbout')
        d.setStyleSheet(qt_viewer.styleSheet())
        d.setWindowTitle('About')
        d.setWindowModality(Qt.ApplicationModal)
        d.exec_()


class QtCopyToClipboardButton(QPushButton):
    """Button to copy text box information to the clipboard.

    Parameters
    ----------
    text_edit : qtpy.QtWidgets.QTextEdit
        The text box contents linked to copy to clipboard button.

    Attributes
    ----------
    text_edit : qtpy.QtWidgets.QTextEdit
        The text box contents linked to copy to clipboard button.
    """

    def __init__(self, text_edit):
        super().__init__()
        self.setObjectName("QtCopyToClipboardButton")
        self.text_edit = text_edit
        self.setToolTip("Copy to clipboard")
        self.clicked.connect(self.copyToClipboard)

    def copyToClipboard(self):
        """Copy text to the clipboard."""
        cb = QtGui.QGuiApplication.clipboard()
        cb.setText(str(self.text_edit.toPlainText()))
