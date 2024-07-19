from apps.bank.cli import BankCli
from apps.bank.schemas import Valute

from config import Config


class BankService:
    def __init__(self, config: Config, cli: BankCli):
        self.config = config
        self.cli = cli

    async def get_exchange_rates(self) -> list[tuple[str, str, dict]]:
        async with self.cli as cli:
            xml_data = await cli.get_exchange_rates()
        return [
            (
                f"valute:{valute.get('ID')}",
                "$",
                Valute(
                    ID=valute.get('ID'),
                    NumCode=int(valute.find('NumCode').text),
                    CharCode=valute.find('CharCode').text,
                    Nominal=int(valute.find('Nominal').text),
                    Name=valute.find('Name').text,
                    Value=float(valute.find('Value').text.replace(',', '.')),
                    VunitRate=float(valute.find('VunitRate').text.replace(',', '.'))
                ).model_dump()
            )
            for valute in xml_data.findall('Valute')
        ]
