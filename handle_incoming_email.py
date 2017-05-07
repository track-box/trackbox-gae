import logging

from google.appengine.api import mail, app_identity
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
import webapp2


def send_mail(to_address):
    sender_address = 'trackbox@{}.appspotmail.com'.format(app_identity.get_application_id())
    message = mail.EmailMessage(
            sender=sender_address,
            subject="test")
    message.to = to_address
    message.body = """test
    """
    message.send()

class LogSenderHandler(InboundMailHandler):
    def receive(self, mail_message):
        logging.info("Received a message from: " + mail_message.sender)

        send_mail(mail_message.sender)


app = webapp2.WSGIApplication([LogSenderHandler.mapping()], debug=True)

