import logging

from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
import webapp2
from google.appengine.api import taskqueue

class IncomingMailHandler(InboundMailHandler):
    def receive(self, mail_message):
        logging.info(mail_message)



app = webapp2.WSGIApplication([IncomingMailHandler.mapping()], debug=True)
