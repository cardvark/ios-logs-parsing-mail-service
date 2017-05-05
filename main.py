import logging
import eventparse

from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
from google.appengine.api import mail
import webapp2
from google.appengine.api import taskqueue

class IncomingMailHandler(InboundMailHandler):
    def receive(self, mail_message):
        logging.info('Received a message')
        logging.info('from: ' + mail_message.sender)
        logging.info(mail_message)

        incoming_subject = mail_message.subject
        incoming_sender = mail_message.sender
        incoming_body = mail_message.body
        plaintext_bodies = mail_message.bodies('text/plain')
        for content_type, body in plaintext_bodies:
            decoded_body = body.decode()

        if hasattr(mail_message, 'attachments'):
            for filename, content in mail_message.attachments:
                incoming_filename = filename
                incoming_content = content.decode()
                logging.info(filename)
                logging.info(content.decode())

            return_body = eventparse.parse_events(incoming_content)
            logging.info(return_body)

            mail.send_mail_to_admins(
                sender='noreply@ios-logs-email.appspotmail.com',
                subject=incoming_subject + ' logs report',
                body=return_body
                )

        # if incoming_sender == 'test@example.com':
        #     # body_content = incoming_body.decode()
        #     # logging.info(incoming_body.decode())
        #     # logging.info(repr(decoded_body))
        #     # logging.info(decoded_body)
        #     logging.info(eventparse.parse_events(decoded_body))






app = webapp2.WSGIApplication([IncomingMailHandler.mapping()], debug=True)
