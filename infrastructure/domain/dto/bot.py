from infrastructure.domain.dto.base import DTO


class BotDTO(DTO):
    """ DTO for class BotSettings model """
    id: int
    status: str
    crypto_wallet: str
    alert_group: int
