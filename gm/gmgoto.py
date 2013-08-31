import webapp2
import jinja2
import os
from gmaction import GmAction

class GmGoto(GmAction):
  """Class for Gmail Go-To Actions"""
  TEMPLATE_NAME = os.path.join('google', 'gm_goto.html')
  
  def __init__(self):
    super(GmGoto, self).__init__()

    self._description = ""
    self._url = ""
    self._name = ""

    self._help_params["oneclick_selected"] = ""
    self._help_params["rsvp_selected"] = ""
    self._help_params["review_selected"] = ""
    self._help_params["goto_selected"] = "selected"

  def handler(self, jinja_env, request):
    self._description = request.get("description", "").strip()
    self._url = request.get("url", "").strip()
    self._name = request.get("name", "").strip()

    self._format = super(GmGoto, self).handler(request=request)
    if self._format == GmAction.JSON_LD:
      self._gen_jsonld()
    else:
      self._gen_microdata()

    template = jinja_env.get_template(GmGoto.TEMPLATE_NAME)

    return template.render(description=self._description, url=self._url, 
      name=self._name, response=self._response, **self._help_params)
    
  def _gen_jsonld(self):
    if self._miss_req():
      return

    self._response    = '<script type="application/ld+json">\n{\n'
    self._response   += '  "@context": "http://schema.org",\n'
    self._response   += '  "@type": "EmailMessage",\n'
    self._response   += '  "action": {\n'
    self._response   += '    "@type": "ViewAction",\n'

    if self._name != '':
      self._response += '    "name": "{0}",\n'.format(self._name)

    self._response   += '    "url": "{0}"\n  }},\n'.format(self._url)

    if self._description != '':
      self._response  += '  "description": "{0}"\n'.format(self._description)

    self._response    += '}\n</script>\n'

  def _gen_microdata(self):
    if self._miss_req():
      return

    self._response    = '<div itemscope itemtype="http://schema.org/EmailMessage">\n'
    self._response   += '  <div itemprop="action" itemscope itemtype="http://schema.org/ViewAction">\n'
    
    if self._name != '':
      self._response += '    <meta itemprop="name" content="{0}"/>\n'.format(self._name)

    self._response   += '    <link itemprop="url" href="{0}"/>\n'.format(self._url)
    
    self._response   += '  </div>\n'

    if self._description != '':
      self._response += '  <meta itemprop="description" content="{0}"/>\n'.format(self._description)

    self._response   += '</div>'

  def _miss_req(self):
    if self._url == '':
      self._response = 'Required fields: URL'
      return True

    return False
