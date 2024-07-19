from apps.bank.cli import BankCli
from apps.bank.service import BankService

from config import Config


def get_bank_service(config: Config) -> BankService:
    """Зависимость для получения сервиса банка"""
    return BankService(
        cli=BankCli(config),
        config=config,
    )
