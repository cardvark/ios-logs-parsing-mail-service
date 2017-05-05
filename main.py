import logging

from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
import webapp2
from google.appengine.api import taskqueue

class IncomingMailHandler(InboundMailHandler):
    def receive(self, mail_message):
        logging.info('Received a message')
        logging.info('from: ' + mail_message.sender)
        logging.info(mail_message)
        if hasattr(mail_message, 'attachments'):
            for filename, content in mail_message.attachments:
                logging.info(filename)
                logging.info(content.decode())



app = webapp2.WSGIApplication([IncomingMailHandler.mapping()], debug=True)
