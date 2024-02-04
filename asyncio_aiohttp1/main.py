import aiohttp
import asyncio
from datetime import date, timedelta
import abc
import json


class APIInterface(abc.ABC):
    @abc.abstractmethod
    async def fetch_exchange_rate(self, start_date):
        pass


class NBPAPIImplementation(APIInterface):
    base_url = "http://api.nbp.pl/api/exchangerates/rates/c/"
    currencies = ["EUR", "USD"]

    async def fetch_exchange_rate(self, start_date):
        async with aiohttp.ClientSession() as session:
            rates = {}
            for currency in self.currencies:
                response = await session.get(f"{self.base_url}{currency}/last/10/?format=json")
                if response.ok == False:
                    raise ValueError(
                        f"Failed to fetch data for {currency} - status code: {response.status}")

                data = await response.json()
                for entry in data['rates']:
                    if entry['effectiveDate'] not in rates:
                        rates[entry['effectiveDate']] = {}

                    rates[entry['effectiveDate']][currency.upper()] = {
                        'sale': entry['ask'],
                        'purchase': entry['bid']
                    }
            return rates


class NBPAPI:
    def __init__(self, api_service: APIInterface):
        self.api_service = api_service

    async def get_exchange_rates(self):
        start_dates = [date.today() - timedelta(days=i) for i in range(10)]
        tasks = [self.api_service.fetch_exchange_rate(start_date)
                 for start_date in start_dates]
        results = await asyncio.gather(*tasks)

        cleaned_results = self.remove_duplicates(results)
        return cleaned_results

    def remove_duplicates(self, results):
        cleaned_results = {}
        for result in results:
            for date_key, values in result.items():
                if date_key not in cleaned_results:
                    cleaned_results[date_key] = values
                else:
                    cleaned_results[date_key].update(values)
        return cleaned_results


async def save_to_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file)


async def main():
    api_service = NBPAPIImplementation()
    api = NBPAPI(api_service)
    exchange_rates = await api.get_exchange_rates()
    await save_exchange_rates(exchange_rates)

    print(json.dumps([exchange_rates], indent=4))


async def save_exchange_rates(exchange_rates):
    filename = 'exchange_rates.json'
    await save_to_json([exchange_rates], filename)
    print("Data has been saved to the file exchange_rates.json")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
