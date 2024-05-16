def tryParseFloat(value):
    try:
        _val = float(value)
        return True
    except ValueError:
        return False

def do_with_lock(lock, function, *args):
    with lock:
        return function(*args)