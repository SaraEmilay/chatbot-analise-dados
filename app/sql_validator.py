import sqlparse

def validate_sql(query: str) -> tuple[bool, str]:
    try:
        parsed = sqlparse.parse(query)[0]
        stmt_type = parsed.get_type()
        if stmt_type != 'SELECT':
            return False, "Apenas SELECT permitido"

        if 'limit' not in query.lower():
            query += " LIMIT 1000"

        return True, query
    except Exception as e:
        return False, str(e)
