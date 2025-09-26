import html
import os
import sqlite3
from typing import Optional

from PySide6 import QtCore, QtGui, QtWidgets


class DatabaseManager:
    """Handle SQLite persistence for the encyclopedia."""

    def __init__(self) -> None:
        self.connection: Optional[sqlite3.Connection] = None
        self.database_path: Optional[str] = None

    def connect(self, database_path: str) -> None:
        if not os.path.exists(database_path):
            raise FileNotFoundError(f"Database not found: {database_path}")

        connection = sqlite3.connect(database_path)
        connection.row_factory = sqlite3.Row

        try:
            self._validate_schema(connection)
        except Exception:
            connection.close()
            raise

        self.close()
        self.connection = connection
        self.database_path = database_path

    def _validate_schema(self, connection: sqlite3.Connection) -> None:
        cursor = connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='topics'"
        )
        if cursor.fetchone() is None:
            raise ValueError(
                "The selected database is missing the required 'topics' table."
            )

        # Run a lightweight query to ensure the table is readable.
        connection.execute("SELECT 1 FROM topics LIMIT 1")

    def is_connected(self) -> bool:
        return self.connection is not None

    def fetch_children(self, parent_id: Optional[int]) -> list[sqlite3.Row]:
        if not self.connection:
            return []

        if parent_id is None:
            cursor = self.connection.execute(
                "SELECT * FROM topics WHERE parent_id IS NULL ORDER BY name COLLATE NOCASE"
            )
        else:
            cursor = self.connection.execute(
                "SELECT * FROM topics WHERE parent_id = ? ORDER BY name COLLATE NOCASE",
                (parent_id,),
            )
        return cursor.fetchall()

    def fetch_topic(self, topic_id: int) -> sqlite3.Row:
        if not self.connection:
            raise RuntimeError("No database connection is available.")

        cursor = self.connection.execute("SELECT * FROM topics WHERE id = ?", (topic_id,))
        return cursor.fetchone()

    def close(self) -> None:
        if self.connection is not None:
            self.connection.close()
        self.connection = None
        self.database_path = None


class MedicalEncyclopediaWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.database = DatabaseManager()
        self.setWindowTitle("Medical Encyclopedia")
        self.resize(1000, 650)
        self._setup_palette()
        self._setup_ui()
        self._update_database_status()
        self._populate_tree()

    def _setup_palette(self) -> None:
        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor("#181826"))
        palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor("#f2f2f5"))
        palette.setColor(QtGui.QPalette.Base, QtGui.QColor("#1f1f32"))
        palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor("#23233a"))
        palette.setColor(QtGui.QPalette.Text, QtGui.QColor("#f2f2f5"))
        palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor("#4d7cff"))
        palette.setColor(QtGui.QPalette.HighlightedText, QtGui.QColor("#ffffff"))
        palette.setColor(QtGui.QPalette.Button, QtGui.QColor("#202033"))
        palette.setColor(QtGui.QPalette.ButtonText, QtGui.QColor("#ffffff"))
        self.setPalette(palette)

    def _setup_ui(self) -> None:
        container = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(container)

        header_layout = QtWidgets.QHBoxLayout()
        title = QtWidgets.QLabel("Medical Encyclopedia")
        title_font = QtGui.QFont("Segoe UI", 20, QtGui.QFont.Bold)
        title.setFont(title_font)
        header_layout.addWidget(title)
        header_layout.addStretch()

        self.database_label = QtWidgets.QLabel()
        self.database_label.setObjectName("databaseStatusLabel")
        header_layout.addWidget(self.database_label)

        self.import_button = QtWidgets.QPushButton("Import Database…")
        self.import_button.clicked.connect(self._import_database)
        header_layout.addWidget(self.import_button)

        self.search_bar = QtWidgets.QLineEdit()
        self.search_bar.setPlaceholderText("Search topics...")
        self.search_bar.textChanged.connect(self._filter_topics)
        header_layout.addWidget(self.search_bar, 1)

        layout.addLayout(header_layout)

        splitter = QtWidgets.QSplitter(QtCore.Qt.Orientation.Horizontal)
        splitter.setHandleWidth(2)

        self.topic_tree = QtWidgets.QTreeWidget()
        self.topic_tree.setHeaderHidden(True)
        self.topic_tree.itemSelectionChanged.connect(self._display_selected_topic)
        self.topic_tree.setIndentation(18)
        self.topic_tree.setAnimated(True)
        splitter.addWidget(self.topic_tree)

        detail_container = QtWidgets.QWidget()
        detail_layout = QtWidgets.QVBoxLayout(detail_container)
        detail_layout.setContentsMargins(12, 0, 0, 0)

        self.topic_title = QtWidgets.QLabel("Select a topic to view details")
        self.topic_title.setWordWrap(True)
        self.topic_title.setFont(QtGui.QFont("Segoe UI", 18, QtGui.QFont.Bold))
        detail_layout.addWidget(self.topic_title)

        self.topic_body = QtWidgets.QTextBrowser()
        self.topic_body.setOpenExternalLinks(True)
        self.topic_body.setStyleSheet(
            "QTextBrowser { border: none; background-color: #1b1b2b;"
            " padding: 16px; border-radius: 12px; font-size: 14px; line-height: 1.6; }"
        )
        detail_layout.addWidget(self.topic_body)

        splitter.addWidget(detail_container)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)

        layout.addWidget(splitter)
        self.setCentralWidget(container)

        # Ensure a status bar is available for import feedback.
        self.statusBar()

        self.setStyleSheet(
            """
            QLineEdit {
                border: 1px solid #2e2e4f;
                border-radius: 8px;
                padding: 8px 12px;
                background-color: #1f1f32;
                color: #f2f2f5;
            }
            QTreeWidget {
                border: none;
                background-color: #1b1b2b;
                color: #e0e0f1;
            }
            QTreeWidget::item:selected {
                background-color: #2f3a63;
                color: #ffffff;
            }
            QLabel {
                color: #f2f2f5;
            }
            QSplitter::handle {
                background-color: #25253b;
            }
            QWidget {
                background-color: #181826;
            }
            #databaseStatusLabel {
                color: #9aa0c6;
                font-size: 12px;
            }
            """
        )

    def _populate_tree(self) -> None:
        self.search_bar.blockSignals(True)
        self.search_bar.clear()
        self.search_bar.blockSignals(False)
        self.topic_tree.clear()
        if not self.database.is_connected():
            self.topic_tree.setDisabled(True)
            self.search_bar.setDisabled(True)
            self.topic_title.setText("No database loaded")
            self.topic_body.setHtml(
                "<p>Import an existing medical encyclopedia database to browse topics.</p>"
            )
            return

        self.topic_tree.setEnabled(True)
        self.search_bar.setEnabled(True)
        root_topics = self.database.fetch_children(None)
        for row in root_topics:
            item = self._create_tree_item(row)
            self.topic_tree.addTopLevelItem(item)
        self.topic_tree.expandToDepth(0)
        if self.topic_tree.topLevelItemCount() > 0:
            self.topic_tree.setCurrentItem(self.topic_tree.topLevelItem(0))
        else:
            self.topic_title.setText("No topics available")
            self.topic_body.setHtml(
                "<p>The imported database does not contain any topics yet.</p>"
            )

    def _create_tree_item(self, topic_row: sqlite3.Row) -> QtWidgets.QTreeWidgetItem:
        item = QtWidgets.QTreeWidgetItem([topic_row["name"]])
        item.setData(0, QtCore.Qt.ItemDataRole.UserRole, topic_row["id"])
        for child in self.database.fetch_children(topic_row["id"]):
            item.addChild(self._create_tree_item(child))
        return item

    def _display_selected_topic(self) -> None:
        if not self.database.is_connected():
            return
        items = self.topic_tree.selectedItems()
        if not items:
            return
        item = items[0]
        topic_id = item.data(0, QtCore.Qt.ItemDataRole.UserRole)
        if topic_id is None:
            return
        topic = self.database.fetch_topic(int(topic_id))
        if topic is None:
            return
        self.topic_title.setText(topic["name"])
        self.topic_body.setHtml(self._format_description(topic["description"]))

    def _format_description(self, text: str) -> str:
        paragraphs = [html.escape(p.strip()) for p in text.split("\n") if p.strip()]
        if not paragraphs:
            return "<p>No description available.</p>"
        return "".join(
            f"<p style='margin-bottom:12px'>{paragraph}</p>" for paragraph in paragraphs
        )

    def _filter_topics(self, text: str) -> None:
        if not self.database.is_connected():
            return
        query = text.strip().lower()
        for index in range(self.topic_tree.topLevelItemCount()):
            item = self.topic_tree.topLevelItem(index)
            self._filter_tree_item(item, query)
        if not query:
            self.topic_tree.expandToDepth(0)

    def _filter_tree_item(self, item: QtWidgets.QTreeWidgetItem, query: str) -> bool:
        match = not query or query in item.text(0).lower()
        child_match = False
        for i in range(item.childCount()):
            child = item.child(i)
            child_visible = self._filter_tree_item(child, query)
            child_match = child_match or child_visible
        should_show = match or child_match
        item.setHidden(not should_show)
        if should_show and query:
            parent = item.parent()
            while parent:
                parent.setHidden(False)
                parent.setExpanded(True)
                parent = parent.parent()
        if query and match:
            item.setExpanded(True)
        return should_show

    def _import_database(self) -> None:
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Select Encyclopedia Database",
            str(QtCore.QDir.homePath()),
            "SQLite Databases (*.db *.sqlite *.sqlite3);;All Files (*)",
        )
        if not file_path:
            return

        try:
            self.database.connect(file_path)
        except FileNotFoundError:
            QtWidgets.QMessageBox.warning(
                self,
                "Database Not Found",
                "The selected file could not be located.",
            )
            return
        except ValueError as error:
            QtWidgets.QMessageBox.critical(
                self,
                "Invalid Database",
                str(error),
            )
            return
        except sqlite3.Error as error:
            QtWidgets.QMessageBox.critical(
                self,
                "Database Error",
                f"Unable to open the selected database.\n\n{error}",
            )
            return

        self.statusBar().showMessage(f"Loaded database: {file_path}", 5000)
        self._update_database_status()
        self._populate_tree()

    def _update_database_status(self) -> None:
        if self.database.is_connected() and self.database.database_path:
            name = os.path.basename(self.database.database_path)
            self.database_label.setText(f"Loaded: {name}")
        else:
            self.database_label.setText("No database loaded")

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:  # noqa: N802
        self.database.close()
        super().closeEvent(event)


def main() -> None:
    app = QtWidgets.QApplication([])
    app.setApplicationName("Medical Encyclopedia")
    window = MedicalEncyclopediaWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
