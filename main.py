import hydra 
import logging

from src import Config, Debug
from models import Queue, QueueFactory


@hydra.main(config_path="src/config", config_name="config")
def main(config: Config):
    log = Debug(__name__, config, logging.INFO).__run__()
    queue = QueueFactory(config)
    results = queue.simulate()
    log.info("Simulation run successfully !")
    queue.values()


if __name__ == '__main__':
    main()