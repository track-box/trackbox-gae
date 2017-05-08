# -*- coding: utf-8 -*-
import logging

from google.appengine.api import mail, app_identity
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
import webapp2

import parse_gpx
import main

def send_mail(to, subject, body):
    sender_address = 'trackbox@{}.appspotmail.com'.format(app_identity.get_application_id())
    message = mail.EmailMessage(
            sender=sender_address,
            subject=subject)
    message.to = to
    message.bcc = "trackbox0@gmail.com"
    message.body = body
    message.send()


class LogSenderHandler(InboundMailHandler):
    def receive(self, mail_message):
        logging.info("Received a message from: " + mail_message.sender)

        try:
            name = mail_message.subject
            if name is None: name = "track"

            if mail_message.attachments is None:
                raise Exception("track file not found")

            filename, payload = mail_message.attachments[0]
            logging.info(filename)

            track_data = parse_gpx.parse(payload.decode())
            track_json = {
                "name": name,
                "track": track_data
            }
            logging.info(name + " " + str(len(track_data)) + " points")

            if not track_data:
                raise Exception("track data not found")

            track_id = main.create_track_json(track_json)
            edit_id = main.create_edit_json(track_json, track_id)
            logging.info("created:" + track_id + " " + edit_id)

            send_mail(
                mail_message.sender,
                "航跡を共有しました - TrackBox",
                """航跡を共有しました。

「{}」
公開用リンク https://track-box.github.io/track/#{}
編集用リンク https://track-box.github.io/edit/#{}

by TrackBox
""".format(name, track_id, edit_id))

        except Exception as e:
            send_mail(
                mail_message.sender,
                "TrackBox Error",
                str(e))

app = webapp2.WSGIApplication([LogSenderHandler.mapping()], debug=True)

