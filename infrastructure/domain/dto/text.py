from infrastructure.domain.dto.base import DTO


class BotTextDTO(DTO):
    id: str
    text: str
    image: str | None
