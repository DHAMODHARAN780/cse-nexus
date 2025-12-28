def format_date(date):
    if not date:
        return ""
    return date.strftime("%d %b %Y, %H:%M")

def get_file_extension(filename):
    return filename.rsplit('.', 1)[1].lower() if '.' in filename else ""
