class EntityNotFoundError(Exception):
    pass

class UserNotFoundError(EntityNotFoundError):
    pass

class NodeNotFoundError(EntityNotFoundError):
    pass

class RootNotFoundError(EntityNotFoundError):
    pass

class FileEntryNotFoundError(EntityNotFoundError):
    pass

