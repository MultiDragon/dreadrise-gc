import logging

from shared.helpers.caching.ordered_popularities import run_ordered_popularities
from shared.helpers.database import connect
from shared.types.caching import CardPlayability

from ..constants import ScrapedFormats, Update, pd_data

logger = logging.getLogger('dreadrise.dist.pd.popularity')


def _postprocess_playability(cp: CardPlayability, fmt: str, full_deck_count: int) -> None:
    ratio = cp.deck_count / full_deck_count
    if ratio < 0.005:
        cp.playability = 'unplayed'
    elif ratio > 0.075:
        if cp.winrate > 0.55:
            cp.playability = 'good'
        else:
            cp.playability = 'staple'
    else:
        if cp.winrate > 0.55:
            cp.playability = 'playable'
        else:
            cp.playability = 'played'


def run_all_seasons() -> None:
    """
    Calculate the popularity of various PD cards across all seasons.
    :return: nothing
    """
    logger.info('Connecting...')
    client = connect('penny_dreadful')
    logger.info('Getting PD season data...')
    Update()
    run_ordered_popularities(client, _postprocess_playability, ScrapedFormats, ScrapedFormats + ['_all'])


def run_single_season() -> None:
    """
    Calculate the popularity of various PD cards across one season.
    :return: nothing
    """
    logger.info('Connecting...')
    client = connect('penny_dreadful')
    logger.info('Getting PD season data...')
    Update()
    season_num = pd_data['last_season']
    run_ordered_popularities(client, _postprocess_playability, ScrapedFormats, [f'pds{season_num}', '_all'])
