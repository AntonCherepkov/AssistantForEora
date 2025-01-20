class ProjectSearchError(Exception):
    def __init__(self, message="Не найдено релевантного проекта!"):
        super().__init__(message)
