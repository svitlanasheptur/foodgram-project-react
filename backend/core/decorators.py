def doc(docstring):
    """Декоратор для изменения строки документации функции."""
    def document(func):
        func.__doc__ = docstring
        return func
    return document
