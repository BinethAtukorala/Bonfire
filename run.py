import logging, traceback
from datetime import datetime

from lib import utils
from bot.bot import BonfireBot

# Main Program
def run(logger):
    TOKEN, PREFIX = utils.get_discord_config()

    logger.info("Starting Discord bot...")

    bot = BonfireBot(TOKEN, PREFIX)
    bot.run()

if __name__ == '__main__':

    try:
        # Setup Logging
        timeNow = datetime.now().strftime("%Y/%m/%d - %H:%M:%S")
        
        config = utils.get_config()

        if(config["app"]["logging"]):
            logging.basicConfig(
                handlers=[logging.FileHandler(filename=f"logs/{timeNow}.txt", 
                                                 encoding='utf-8', mode='a+'), 
                            logging.StreamHandler()],
                level=logging.INFO,
                format='[%(asctime)s] %(levelname)s:%(name)s - %(message)s'
                )
        else:
            logging.basicConfig(
                handlers=[logging.StreamHandler()],
                level=logging.INFO,
                format='[%(asctime)s] %(levelname)s:%(name)s - %(message)s'
                )
        logging.info(f"Bonfire bot logs - {timeNow}")

        run(logging.getLogger(__name__))
    
    except Exception as e:
        logging.error(f"{e}\n\n{traceback.format_exc()}")