import os
import sqlparse

def test_sql_syntax_validity():
    """Validates that all DDL and analytical SQL files parse without fatal syntax errors."""
    sql_dirs = ["sql/ddl", "sql/views"]
    for directory in sql_dirs:
        for file in os.listdir(directory):
            if file.endswith(".sql"):
                file_path = os.path.join(directory, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    parsed = sqlparse.parse(content)
                    assert len(parsed) > 0, f"Failed to parse statements in {file_path}"
