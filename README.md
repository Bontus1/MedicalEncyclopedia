# Medical Encyclopedia

A modern desktop encyclopedia for medical students and clinicians. The application
organizes terminology, foundational science, and clinical skills into a
navigable tree so you can rapidly browse concise explanations.

## Features

- **Hierarchical navigation** – browse topics grouped by discipline and drill
  down into subtopics like anatomical directions or phases of the cell cycle.
- **SQLite-backed content** – knowledge entries are stored in a lightweight
  database that you can import directly from an existing `.db`, `.sqlite`, or
  `.sqlite3` file.
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

4. Click **Import Database…** in the top toolbar and choose the SQLite database
   that contains your encyclopedia content. The topics tree will populate once a
   valid database is loaded.

## Project Structure

```
.
├── main.py        # Qt application and database bootstrap
└── README.md      # Project documentation
```

The SQLite database file is generated at runtime and intentionally excluded from
version control.

## Preparing a Compatible SQLite Database

The application expects a single table named `topics` that models the
hierarchical encyclopedia tree. You can create a compatible database with the
following schema:

```sql
CREATE TABLE topics (
    id INTEGER PRIMARY KEY,
    parent_id INTEGER REFERENCES topics(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT ""
);
CREATE INDEX idx_topics_parent_id ON topics(parent_id);
```

Each row represents one topic:

- `id` – unique identifier for the topic.
- `parent_id` – `NULL` for root topics or the `id` of the parent topic for
  nested entries.
- `name` – the label shown in the navigation tree and search.
- `description` – rich text content displayed in the detail panel. Use newline
  characters to separate paragraphs; HTML tags are automatically escaped.

Populate the table by inserting your own topics. For example, the SQL below
creates a minimal database with one category and a child topic:

```sql
INSERT INTO topics (id, parent_id, name, description) VALUES
    (1, NULL, 'Anatomy', 'Overview of anatomical terminology.'),
    (2, 1, 'Anatomical Position', 'The standard reference position for the body.');
```

Save the database as `encyclopedia.sqlite` (or any `.db`, `.sqlite`, or
`.sqlite3` file). When you launch the application, choose this file via **Import
Database…** to browse the content.
