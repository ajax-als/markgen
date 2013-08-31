import webapp2
import string
import jinja2
import os

from gm.gmgoto import GmGoto
from gm.gmrsvp import GmRsvp
from gm.gmoneclick import GmOneClick
from gm.gmreview import GmReview
from ya.yaxml import YaXML
from ya.yabutton import YaButton


class GmActionsHandler(webapp2.RequestHandler):
  def __init__(self, request, response):
    webapp2.RequestHandler.__init__(self, request, response)
    self.goto_action = GmGoto()
    self.rsvp_action = GmRsvp()
    self.one_click_action = GmOneClick()
    self.review_action = GmReview()

  def get(self):
    template = ""
    markup = self.request.get("gm_action_type")
    if markup == "one_click":
      template = self.one_click_action.handler(jinja_environment, self.request)
    elif markup == "rsvp":
      template = self.rsvp_action.handler(jinja_environment, self.request)
    elif markup == "review":
      template = self.review_action.handler(jinja_environment, self.request)
    elif markup == "go_to":
      template = self.goto_action.handler(jinja_environment, self.request)
    else:
      return self.redirect('/gm_actions?gm_action_type=one_click')
    
    self.response.write(template)
    
class YaActionsHandler(webapp2.RequestHandler):
  def __init__(self, request, response):
    webapp2.RequestHandler.__init__(self, request, response)
    self.XML = YaXML()
    self.Button = YaButton()

  def get(self):
    template = ""
    markup = self.request.get("ya_action_type")
    if markup == "xml_form":
      template = self.XML.handler(jinja_environment, self.request)
    elif markup == "button":
      template = self.Button.handler(jinja_environment, self.request)
    else:
      return self.redirect('/ya_actions?ya_action_type=xml_form')
    
    self.response.write(template)
  
app = webapp2.WSGIApplication([('/', YaActionsHandler),
  ('/gm_actions', GmActionsHandler),
  ('/ya_actions', YaActionsHandler)],
  debug=False)

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), "html")))
