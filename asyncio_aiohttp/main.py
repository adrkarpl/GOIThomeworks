import aiohttp
import asyncio
from datetime import date, timedelta
import abc
import json
import argparse


class APIInterface(abc.ABC):
    @abc.abstractmethod
    async def fetch_exchange_rate(self, start_date):
        pass


class NBPAPIImplementation(APIInterface):
    base_url = "http://api.nbp.pl/api/exchangerates/rates/c/"
    currencies = ["EUR", "USD"]

    async def fetch_exchange_rate(self, currency, start_date):
        async with aiohttp.ClientSession() as session:
            response = await session.get(f"{self.base_url}{currency}/last/10/?format=json")
            if response.ok == False:
                raise ValueError(
                    f"Failed to fetch data for {currency} - status code: {response.status}")

            data = await response.json()
            rates = {}
            for entry in data['rates']:
                if entry['effectiveDate'] == start_date.strftime("%Y-%m-%d"):
                    rates[currency.upper()] = {
                        'sale': entry['ask'],
                        'purchase': entry['bid']
                    }
                    break
            return rates


class NBPAPI:
    def __init__(self, api_service: APIInterface):
        self.api_service = api_service

    async def get_exchange_rates(self, start_date, currencies):
        tasks = [self.api_service.fetch_exchange_rate(
            currency, start_date) for currency in currencies]
        results = await asyncio.gather(*tasks)
        return {start_date.strftime("%Y-%m-%d"): {currency: rate for currency_rate in results for currency, rate in currency_rate.items()}}

    def get_start_dates(self, days_ago):
        today = date.today()
        return [today - timedelta(days=i) for i in range(min(days_ago, 10))]


async def save_to_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file)


async def main():
    parser = argparse.ArgumentParser(description='Fetch exchange rates.')
    parser.add_argument(
        'days_ago', type=int, help='Number of days ago from which to fetch exchange rates.')
    parser.add_argument('--currencies', nargs='+',
                        default=["EUR", "USD"], help='Currencies to fetch exchange rates for.')
    args = parser.parse_args()

    if args.days_ago > 10:
        print("You can request data for up to 10 days ago. Fetching data from 10 days ago.")
        days_ago = 10
    else:
        days_ago = args.days_ago

    api_service = NBPAPIImplementation()
    api = NBPAPI(api_service)
    start_dates = api.get_start_dates(days_ago)
    exchange_rates = {}
    for start_date in start_dates:
        rates = await api.get_exchange_rates(start_date, args.currencies)
        exchange_rates.update(rates)
    await save_exchange_rates(exchange_rates)

    print(json.dumps(exchange_rates, indent=4))


async def save_exchange_rates(exchange_rates):
    filename = 'exchange_rates.json'
    await save_to_json(exchange_rates, filename)
    print("Data has been saved to the file exchange_rates.json")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
