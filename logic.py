# logic.py

def is_valid_title(title):
    return bool(title and title.strip())

def is_valid_rating(rating):
    if isinstance(rating, int):
        return 1 <= rating <= 5
    if isinstance(rating, str) and rating.isdigit():
        return 1 <= int(rating) <= 5
    return False