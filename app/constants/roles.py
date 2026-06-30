from enum import Enum

class UserRole(str, Enum):
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    SUB_ADMIN = "sub_admin"
    MANAGER = "manager"
    TEAM_MEMBER = "team_member"