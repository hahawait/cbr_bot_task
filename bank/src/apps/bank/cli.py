from apps.base.cli import APIClient
from config import Config


class BankCli(APIClient):
    """
    Клиент для взаимодействия с ЦБ РФ
    """

    def __init__(self, config: Config):
        self.config = config
        super().__init__(base_url=config.bank_config.URL)

    async def get_exchange_rates(self) -> None:
        """ 
        Получение курсов валют
        :return: None 
        """
        return await self._make_request(
            method="GET",
            url=self.config.bank_config.EXCHANGE_RATES_ENDPOINT,
        )
