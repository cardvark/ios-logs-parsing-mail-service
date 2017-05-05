import logging

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

        if hasattr(mail_message, 'attachments'):
            for filename, content in mail_message.attachments:
                incoming_filename = filename
                incoming_content = content.decode()
                logging.info(filename)
                logging.info(content.decode())

            mail.send_mail_to_admins(
                sender='noreply@ios-logs-email.appspotmail.com',
                subject=incoming_subject + ' logs report',
                body=incoming_content[:100]
                )







app = webapp2.WSGIApplication([IncomingMailHandler.mapping()], debug=True)
