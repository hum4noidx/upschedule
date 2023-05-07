from datetime import datetime
from typing import Optional

from infrastructure.domain.dto.base import DTO


class UserDTO(DTO):
    """ DTO for User model """
    user_id: int
    full_name: str
    username: Optional[str]
    registered_at: datetime
    is_vip: bool
    is_admin: bool
    is_blocked: bool
