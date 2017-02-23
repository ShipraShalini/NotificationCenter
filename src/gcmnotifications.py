import json
import logging

import requests
from django.conf import settings

logger = logging.getLogger('notification')


class FcmNotifications(object):
    FCM_URL = "https://fcm.googleapis.com/fcm/send"
    HEADERS = {"Authorization": "key=" + settings.FCM_KEY, "Content-Type": "application/json"}

    @staticmethod
    def create_payload(fcm_list, payload):
        """
        creates payload to be sent for notification
        :param fcm_list: fcm_id to which the notification has to be sent
        :param payload: data to be sent
        :return: data
        """
        return json.dumps({
            'notification': payload,
            'registration_ids': fcm_list
        })

    def send_notification(self, fcm_list, payload):
        """
        sends notification ands logs
        :param fcm_list: fcm_id to which the notification has to be sent
        :param payload: data to be sent
        :return: None
        """
        data = self.create_payload(fcm_list=fcm_list, payload=payload)
        response = requests.post(self.FCM_URL, data=data, headers=self.HEADERS)
        logger.info(data)
        # return json.loads(response.content)['results']

    def send(self, fcm_list, data):
        """
        gets data for notification to be sent.
        since gcm can be sent to only 1000 ids at once, it  creates batches in case there are more
        :param fcm_list:
        :param data:
        :return:
        """
        # fcm = 'fliT7UokFEg:APA91bHKTs6V5t7ebmSPitwTvzcYFTMV3lkUp8oTIpn58udx85e2POUqdqkx4G4_J4M3R6H-elNdAEmeh3uraNk9XSvCk3p8228i5CAVBZdZYg2OQ4-sJDeXvegG4J0miU32znkot3jZ'
        length = len(fcm_list)
        if length > 1000:
            # response = []
            for start, end in zip(range(0, length, 1000), range(1000, length, 1000)):
                fcm_list_chunk = fcm_list[start:end]
                self.send_notification(fcm_list_chunk, payload=data)
        else:
            self.send_notification(fcm_list, payload=data)
