import motor.motor_asyncio
import logging
from pymongo.read_preferences import ReadPreference
from .event import Event

LOG = logging.getLogger(__name__)


DB_CLASSES = [
    Event
]


def init_db(db_config):
    db = get_db(db_config)
    map_db_collection_with_class(db, DB_CLASSES)
    return db


def get_db(db_config):
    """
    creates connection with dabatase and gets db object to connect.
    """
    connection = motor.motor_asyncio.AsyncIOMotorClient(
        host=db_config.uri,
        # secondarypreferred has proved to be a good practice,
        # as it enabled minimal contention on the node that should
        # be critical and handle writes. Oftentimes delay of event
        # propagation is in the milliseconds.
        readPreference="secondaryPreferred",
    )
    db = connection[db_config.db_name]
    return db


def map_db_collection_with_class(db, db_classes):
    """
    maps database-collection with classes
    """
    for db_class in db_classes:
        name = db_class._collection
        if name:
            setattr(db, name, db_class(getattr(db, name)))
