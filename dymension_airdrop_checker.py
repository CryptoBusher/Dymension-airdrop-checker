from time import sleep
import random
from sys import stderr

import requests
from pyfiglet import Figlet
from loguru import logger

import config

logger.remove()
logger.add(stderr, format="<white>{time:HH:mm:ss}</white> | <level>{level: <8}</level> | <white>{message}</white>")


f = Figlet(font='5lineoblique')
print(f.renderText('Busher'))
print('Telegram channel: @CryptoKiddiesClub')
print('Telegram chat: @CryptoKiddiesChat')
print('Twitter: @CryptoBusher\n')


def check_airdrop(_wallet: str, proxy: str = None):
    url = f"https://geteligibleuserrequest-xqbg2swtrq-uc.a.run.app/?address={_wallet.lower()}"

    if proxy:
        _proxies = {
            "http": proxy,
            "https": proxy
        }
        response = requests.get(url, proxies=_proxies)
    else:
        response = requests.get(url)

    if response.status_code == 200:
        logger.success(f"Wallet: {_wallet} | Response: {response.text}")
    else:
        logger.info(f"Wallet: {_wallet} | Response: {response.text}")


def fetch_sleep():
    delay = random.uniform(config.MIN_FETCH_DELAY_SEC, config.MAX_FETCH_DELAY_SEC)
    sleep(delay)


if __name__ == "__main__":
    with open("wallets.txt", "r") as file:
        wallets = [w.strip() for w in file]

    try:
        with open("proxies.txt", "r") as file:
            proxies = [p.strip() for p in file]
    except FileNotFoundError:
        proxies = []

    for i, wallet in enumerate(wallets):
        try:
            check_airdrop(wallet, proxies[i])
        except IndexError:
            check_airdrop(wallet)
        except Exception as e:
            print(f'Failed to check wallet {wallet}, reason: {e}')
        finally:
            fetch_sleep()
