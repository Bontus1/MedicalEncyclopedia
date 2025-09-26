# Medical Encyclopedia

A modern desktop encyclopedia for medical students and clinicians. The application
organizes terminology, foundational science, and clinical skills into a
navigable tree so you can rapidly browse concise explanations.

## Features

- **Hierarchical navigation** – browse topics grouped by discipline and drill
  down into subtopics like anatomical directions or phases of the cell cycle.
- **SQLite-backed content** – knowledge entries are stored in a lightweight
  database that is automatically created and seeded with sample content the
  first time you launch the app.
- **Powerful search** – filter the tree in real time to pinpoint the concept
  you need.
- **Polished interface** – a dark, minimal Qt design keeps the focus on the
  material.

## Getting Started

1. Create and activate a virtual environment (optional but recommended).
2. Install the dependencies:

   ```bash
   pip install PySide6
   ```

3. Launch the application:

   ```bash
   python main.py
   ```

The first launch seeds `medical_encyclopedia.db` with curated sample topics. You
can inspect or extend the dataset with any SQLite-compatible tool.

## Project Structure

```
.
├── main.py        # Qt application and database bootstrap
└── README.md      # Project documentation
```

The SQLite database file is generated at runtime and intentionally excluded from
version control.
