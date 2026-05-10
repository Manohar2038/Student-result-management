def validate_student(data):
    """Validate payload for creating a student."""
    if not data:
        return False, "Request body is empty or not JSON"

    required = ['name', 'roll_number', 'department', 'semester']
    missing  = [f for f in required if not data.get(f)]
    if missing:
        return False, f"Missing required fields: {', '.join(missing)}"

    try:
        sem = int(data['semester'])
        if not (1 <= sem <= 8):
            return False, "Semester must be between 1 and 8"
    except (ValueError, TypeError):
        return False, "Semester must be an integer"

    return True, None


def validate_result(data):
    """Validate payload for updating a result."""
    if not data:
        return False, "Request body is empty or not JSON"

    required = ['gpa', 'grade']
    missing  = [f for f in required if f not in data]
    if missing:
        return False, f"Missing required fields: {', '.join(missing)}"

    try:
        gpa = float(data['gpa'])
        if not (0.0 <= gpa <= 10.0):
            return False, "GPA must be between 0.0 and 10.0"
    except (ValueError, TypeError):
        return False, "GPA must be a number"

    if data['grade'] not in ['A', 'B', 'C', 'D', 'F']:
        return False, "Grade must be one of A, B, C, D, F"

    return True, None


def validate_bulk(records):
    """Validate a list of records for bulk update."""
    if not isinstance(records, list) or not records:
        return False, "Provide a non-empty JSON array"

    for i, rec in enumerate(records):
        for field in ['id', 'gpa', 'grade']:
            if field not in rec:
                return False, f"Record at index {i} missing field '{field}'"

    return True, None
