import webapp2
import jinja2

class GmAction(object):
  """Abstract Class for Gmail Actions"""

  JSON_LD = "jsonld"
  MICRODATA = "microdata"
  
  def __init__(self):
    self._help_params = {}
    self._response = ""
    self._format = ""

  def handler(self, jinja_env=None, request=None):
    self._format = request.get("format", GmAction.JSON_LD)
    if self._format == GmAction.JSON_LD:
      self._help_params["json_checked"] = "checked"
      self._help_params["microdata_checked"] = ""    
    else:
      self._help_params["json_checked"] = ""
      self._help_params["microdata_checked"] = "checked"

    return self._format
    
  def _gen_jsonld(self):
    pass

  def _gen_microdata(self):
    pass