import json
import logging

from datetime import datetime

logger = logging.getLogger('notification')

def send_notification(user_ids, payload):
    data = {"notification sent to users": user_ids, "with payload": payload, "time": str(datetime.utcnow())}
    logger.info(json.dumps(data))
