def format_date(date):
    if not date:
        return ""
    return date.strftime("%d %b %Y, %H:%M")

def get_file_extension(filename):
    return filename.rsplit('.', 1)[1].lower() if '.' in filename else ""

def get_file_url(path):
    from flask import url_for
    if not path:
        return ""
    if path.startswith('http'):
        return path
        
    # Handle paths starting with uploads/ (custom route)
    if path.startswith('uploads/'):
        return url_for('common.uploaded_file', filename=path[8:])
    
    # Handle paths starting with static/ (default behavior)
    if path.startswith('static/'):
        return url_for('static', filename=path[7:])
        
    # Default to static
    return url_for('static', filename=path)
