import html
import os
import sqlite3
from typing import Dict, Optional

from PySide6 import QtCore, QtGui, QtWidgets


class DatabaseManager:
    """Handle SQLite persistence for the encyclopedia."""

    def __init__(self, database_path: str = "medical_encyclopedia.db") -> None:
        self.database_path = database_path
        should_seed = not os.path.exists(database_path)
        self.connection = sqlite3.connect(self.database_path)
        self.connection.row_factory = sqlite3.Row
        self._create_schema()
        if should_seed:
            self._populate_sample_data()

    def _create_schema(self) -> None:
        with self.connection:
            self.connection.execute(
                """
                CREATE TABLE IF NOT EXISTS topics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT NOT NULL,
                    parent_id INTEGER,
                    FOREIGN KEY(parent_id) REFERENCES topics(id)
                )
                """
            )

    def _populate_sample_data(self) -> None:
        sample_data = {
            "Terminology": {
                "description": (
                    "Core anatomical and clinical vocabulary that defines spatial"
                    " relationships and common language in healthcare."
                ),
                "children": {
                    "Directions": {
                        "description": (
                            "Directional terms describe the location of structures"
                            " relative to one another."
                        ),
                        "children": {
                            "Anterior (ventral)": {
                                "description": (
                                    "Toward the front surface of the body; often used"
                                    " interchangeably with ventral in human anatomy."
                                )
                            },
                            "Posterior (dorsal)": {
                                "description": (
                                    "Toward the back surface of the body, opposite of"
                                    " anterior."
                                )
                            },
                            "Superior (cranial)": {
                                "description": (
                                    "Toward the head or upper part of the body;"
                                    " indicates a position above another structure."
                                )
                            },
                            "Inferior (caudal)": {
                                "description": (
                                    "Toward the feet or lower part of the body;"
                                    " indicates a position below another structure."
                                )
                            },
                            "Medial": {
                                "description": (
                                    "Closer to the median plane of the body or a"
                                    " structure."
                                )
                            },
                            "Lateral": {
                                "description": (
                                    "Farther from the median plane of the body or a"
                                    " structure."
                                )
                            },
                            "Proximal": {
                                "description": (
                                    "Closer to the point of origin or attachment;"
                                    " frequently used when discussing limbs."
                                )
                            },
                            "Distal": {
                                "description": (
                                    "Farther from the point of origin or attachment;"
                                    " opposite of proximal."
                                )
                            },
                        },
                    },
                    "Anatomical Regions": {
                        "description": (
                            "Named body regions provide consistent reference"
                            " points for examinations and procedures."
                        ),
                        "children": {
                            "Ventral Cavity": {
                                "description": (
                                    "The anterior body cavity that houses thoracic,"
                                    " abdominal, and pelvic organs."
                                )
                            },
                            "Dorsal Cavity": {
                                "description": (
                                    "Posterior body cavity containing the cranial and"
                                    " vertebral spaces."
                                )
                            },
                            "Quadrants": {
                                "description": (
                                    "Abdominal surface divided into right/left upper"
                                    " and lower quadrants for assessment."
                                )
                            },
                            "Surface Landmarks": {
                                "description": (
                                    "External anatomical markers such as the sternal"
                                    " angle and iliac crest used for orientation."
                                )
                            },
                        },
                    },
                    "Clinical Abbreviations": {
                        "description": (
                            "Shortened forms and acronyms commonly encountered in"
                            " clinical documentation."
                        ),
                        "children": {
                            "PRN": {
                                "description": (
                                    "Pro re nata; indicates a medication is given as"
                                    " needed based on patient symptoms."
                                )
                            },
                            "NPO": {
                                "description": (
                                    "Nil per os; instructs that the patient should"
                                    " refrain from oral intake."
                                )
                            },
                            "Stat": {
                                "description": (
                                    "Immediately; denotes urgency in orders and"
                                    " interventions."
                                )
                            },
                        },
                    },
                },
            },
            "Cellular Biology": {
                "description": (
                    "Foundational processes that govern cell structure, function,"
                    " and replication."
                ),
                "children": {
                    "Cell Cycle": {
                        "description": (
                            "A regulated sequence of growth (G1), DNA synthesis"
                            " (S), preparation for mitosis (G2), and division"
                            " (M). Checkpoints ensure fidelity."
                        ),
                        "children": {
                            "G1 Phase": {
                                "description": (
                                    "Cell grows, produces organelles, and monitors"
                                    " the environment before committing to DNA"
                                    " replication."
                                )
                            },
                            "S Phase": {
                                "description": (
                                    "DNA replication occurs, producing identical"
                                    " sister chromatids for each chromosome."
                                )
                            },
                            "G2 Phase": {
                                "description": (
                                    "Cell continues to grow and synthesizes proteins"
                                    " required for mitosis; DNA is checked for damage."
                                )
                            },
                            "M Phase": {
                                "description": (
                                    "Mitosis and cytokinesis separate duplicated"
                                    " chromosomes and divide the cytoplasm into two"
                                    " daughter cells."
                                )
                            },
                        },
                    },
                    "Organelles": {
                        "description": (
                            "Membrane-bound structures with specialized functions"
                            " essential to cell physiology."
                        ),
                        "children": {
                            "Mitochondria": {
                                "description": (
                                    "Powerhouses of the cell generating ATP through"
                                    " oxidative phosphorylation; contain their own DNA."
                                )
                            },
                            "Endoplasmic Reticulum": {
                                "description": (
                                    "Network responsible for protein synthesis (rough"
                                    " ER) and lipid metabolism (smooth ER)."
                                )
                            },
                            "Golgi Apparatus": {
                                "description": (
                                    "Modifies, sorts, and packages proteins and"
                                    " lipids for secretion or delivery to organelles."
                                )
                            },
                            "Lysosomes": {
                                "description": (
                                    "Acidic vesicles containing hydrolytic enzymes"
                                    " for intracellular digestion and recycling."
                                )
                            },
                        },
                    },
                    "Cell Signaling": {
                        "description": (
                            "Communication pathways that allow cells to sense and"
                            " respond to their environment."
                        ),
                        "children": {
                            "Autocrine": {
                                "description": (
                                    "Signals released and received by the same cell,"
                                    " often regulating growth."
                                )
                            },
                            "Paracrine": {
                                "description": (
                                    "Signals travel short distances to nearby cells"
                                    " to coordinate local responses."
                                )
                            },
                            "Endocrine": {
                                "description": (
                                    "Hormones enter the bloodstream to influence"
                                    " distant target cells."
                                )
                            },
                            "Second Messengers": {
                                "description": (
                                    "Intracellular signaling molecules such as cAMP"
                                    " and calcium that amplify receptor activation."
                                )
                            },
                        },
                    },
                },
            },
            "Clinical Skills": {
                "description": (
                    "Practical competencies that underpin patient assessment and"
                    " care delivery."
                ),
                "children": {
                    "History Taking": {
                        "description": (
                            "Structured approach to gathering subjective"
                            " information including chief complaint, history of"
                            " present illness, and review of systems."
                        )
                    },
                    "Physical Examination": {
                        "description": (
                            "Systematic evaluation of the body using inspection,"
                            " palpation, percussion, and auscultation."
                        ),
                        "children": {
                            "Cardiovascular Exam": {
                                "description": (
                                    "Assessment of heart sounds, jugular venous"
                                    " pressure, and peripheral pulses to evaluate"
                                    " cardiac function."
                                )
                            },
                            "Respiratory Exam": {
                                "description": (
                                    "Evaluation of breathing patterns, lung sounds,"
                                    " and percussion tones to detect pulmonary"
                                    " pathology."
                                )
                            },
                            "Neurologic Exam": {
                                "description": (
                                    "Series of tests assessing cranial nerves, motor"
                                    " function, sensation, reflexes, and coordination."
                                )
                            },
                        },
                    },
                    "Procedural Basics": {
                        "description": (
                            "Essential bedside skills such as venipuncture,"
                            " arterial line placement, and basic suturing."
                        )
                    },
                },
            },
        }

        def insert_topic(name: str, description: str, parent_id: Optional[int]) -> int:
            cursor = self.connection.execute(
                "INSERT INTO topics (name, description, parent_id) VALUES (?, ?, ?)",
                (name, description, parent_id),
            )
            return cursor.lastrowid

        def insert_children(nodes: Dict[str, Dict], parent_id: Optional[int] = None) -> None:
            for title, payload in nodes.items():
                description = payload.get(
                    "description",
                    "No description has been provided for this entry yet.",
                )
                topic_id = insert_topic(title, description, parent_id)
                children = payload.get("children")
                if children:
                    insert_children(children, topic_id)

        insert_children(sample_data)
        self.connection.commit()

    def fetch_children(self, parent_id: Optional[int]) -> list[sqlite3.Row]:
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
        cursor = self.connection.execute("SELECT * FROM topics WHERE id = ?", (topic_id,))
        return cursor.fetchone()

    def close(self) -> None:
        self.connection.close()


class MedicalEncyclopediaWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.database = DatabaseManager()
        self.setWindowTitle("Medical Encyclopedia")
        self.resize(1000, 650)
        self._setup_palette()
        self._setup_ui()
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

        self.search_bar = QtWidgets.QLineEdit()
        self.search_bar.setPlaceholderText("Search topics...")
        self.search_bar.textChanged.connect(self._filter_topics)
        header_layout.addWidget(self.search_bar)

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
            """
        )

    def _populate_tree(self) -> None:
        self.topic_tree.clear()
        root_topics = self.database.fetch_children(None)
        for row in root_topics:
            item = self._create_tree_item(row)
            self.topic_tree.addTopLevelItem(item)
        self.topic_tree.expandToDepth(0)
        if self.topic_tree.topLevelItemCount() > 0:
            self.topic_tree.setCurrentItem(self.topic_tree.topLevelItem(0))

    def _create_tree_item(self, topic_row: sqlite3.Row) -> QtWidgets.QTreeWidgetItem:
        item = QtWidgets.QTreeWidgetItem([topic_row["name"]])
        item.setData(0, QtCore.Qt.ItemDataRole.UserRole, topic_row["id"])
        for child in self.database.fetch_children(topic_row["id"]):
            item.addChild(self._create_tree_item(child))
        return item

    def _display_selected_topic(self) -> None:
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
