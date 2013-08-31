import webapp2
import jinja2
import os
from gmaction import GmAction

class GmOneClick(GmAction):
  """Class for Gmail One-Click Actions"""
  TEMPLATE_NAME = os.path.join('google', 'gm_one_click.html')

  CONFIRM_ACTION = "confirm"
  SAVE_ACTION = "save"

  HTTP_GET = "get"
  HTTP_POST = "post"
  
  def __init__(self):
    super(GmOneClick, self).__init__()
    self._action = ""
    self._method = ""
    
    self._name = ""
    self._url = ""
    self._description = ""
    self._req_needed = False
    
    self._handler_empty = False
    self._action_empty = False
    self._mess_emty = False

    self._help_params["oneclick_selected"] = "selected"
    self._help_params["rsvp_selected"] = ""
    self._help_params["review_selected"] = ""
    self._help_params["goto_selected"] = ""


  def handler(self, jinja_env, request):
    self._action = request.get("action", GmOneClick.CONFIRM_ACTION)
    if self._action == GmOneClick.CONFIRM_ACTION:
      self._help_params["confirm_selected"] = "selected"
      self._help_params["save_selected"] = ""
    else: #save action
      self._help_params["confirm_selected"] = ""
      self._help_params["save_selected"] = "selected"

    self._method = request.get("method", GmOneClick.HTTP_GET)
    if self._method == GmOneClick.HTTP_GET:
      self._help_params["get_selected"] = "selected"
      self._help_params["post_selected"] = ""
    else: #http post
      self._help_params["get_selected"] = ""
      self._help_params["post_selected"] = "selected"

    self._name = request.get("name", "").strip()    
    self._url = request.get("url", "").strip()
    self._description = request.get("description", "").strip()

    self._req_needed = bool(request.get("confirmation", False))
    if self._req_needed:
      self._help_params["req_checked"] = "checked"
    else:
      self._help_params["req_checked"] = ""

    self._format = super(GmOneClick, self).handler(request=request)
    if self._format == GmAction.JSON_LD:
      self._gen_jsonld()
    else:
      self._gen_microdata()

    template = jinja_env.get_template(GmOneClick.TEMPLATE_NAME)
    return template.render(name = self._name, url = self._url, 
      description = self._description, response = self._response, 
      **self._help_params)

  def _gen_jsonld(self):
    self._check_empty()

    if self._mess_empty: return

    self._response          = '<script type="application/ld+json">\n{\n'
    self._response         += '  "@context": "http://schema.org",\n'
    self._response         += '  "@type": "EmailMessage"'

    if self._description != "":
      self._response       += ',\n  "description": "{0}"'.format(self._description)

    if not self._action_empty:
      self._response       += ',\n  "action": {\n'

      if self._action == GmOneClick.CONFIRM_ACTION:
        self._response     += '    "@type": "ConfirmAction"'
      else:
        self._response     += '    "@type": "SaveAction"'

      if self._name != "":
        self._response     += ',\n    "name" : "{0}"'.format(self._name)

      if not self._handler_empty:  
        self._response     += ',\n    "handler": {\n'
        self._response     += '      "@type": "HttpActionHandler"'

        if self._url != "":
          self._response   += ',\n      "url": "{0}"'.format(self._url)

        if self._req_needed:
          self._response   += ',\n      "requiresConfirmation": "http://schema.org/True"'

        if self._method == GmOneClick.HTTP_GET:
          self._response   += ',\n      "method" : "http://schema.org/HttpRequestMethod/GET"'
        else:
           self._response   += ',\n      "method" : "http://schema.org/HttpRequestMethod/POST"'

        self._response     += '\n    }'

      self._response       += '\n  }'

    self._response         += '\n}\n'
    self._response         += '</script>'
  
  def _gen_microdata(self):
    self._check_empty()

    if self._mess_empty: return

    self._response        = '<div itemscope itemtype="http://schema.org/EmailMessage">\n'

    if self._description != "":
      self._response     += '  <meta itemprop="description" content="{0}"/>\n'.format(
      self._description)

    if not self._action_empty:
      self._response     += '  <div itemprop="action" itemscope '

      if self._action == GmOneClick.CONFIRM_ACTION:
        self._response   += 'itemtype="http://schema.org/ConfirmAction">\n'
      else:
        self._response   += 'itemtype="http://schema.org/SaveAction">\n'
      
      if self._name != "":
        self._response   += '    <meta itemprop="name" content="{0}"/>\n'.format(
          self._name)

      if not self._handler_empty:
        self._response   += '    <div itemprop="handler" itemscope '
        self._response   += 'itemtype="http://schema.org/HttpActionHandler">\n'

        if self._url != "":
          self._response += '      <link itemprop="url" href="{0}"/>\n'.format(
            self._url)

        if self._req_needed:
          self._response += '      <meta itemprop="requiresConfirmation" '
          self._response += 'content="http://schema.org/True"/>\n'

        if self._method == GmOneClick.HTTP_GET:
          self._response += '      <meta itemprop="method" content="http://schema.org/HttpRequestMethod/GET"/>\n'
        else:
          self._response += '      <meta itemprop="method" content="http://schema.org/HttpRequestMethod/POST"/>\n'

        self._response   += '    </div>\n'
      self._response     += '  </div>\n'
    self._response       += '</div>\n'      

  def _check_empty(self):
    self._response = "No required properties needed."

    self._handler_empty = (self._url == "") and (not self._req_needed)
    self._action_empty  = self._handler_empty and (self._name == "")
    self._mess_empty    = self._action_empty and (self._description == "") 
