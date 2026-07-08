from enum import Enum


class ResourceVisibility(str, Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    DEPARTMENT = "department"
    ROLE_BASED = "role_based"
    PRIVATE = "private"