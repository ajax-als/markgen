import webapp2
import jinja2

class YaAction(object):
  """Abstract Class for Ya.Islands Actions"""

  OGP = "ogp"
  SCHEMA = "schema"
  
  def __init__(self):
    self._help_params = {}
    self._response = ""
    self._format = ""

  def handler(self, jinja_env=None, request=None):
    self._format = request.get("format", self.OGP)
    if self._format == self.OGP:
      self._help_params["ogp_checked"] = "checked"
      self._help_params["schema_checked"] = ""    
    else:
      self._help_params["ogp_checked"] = ""
      self._help_params["schema_checked"] = "checked"

    return self._format
    
  def _gen_ogp(self):
    pass

  def _gen_schema(self):
    pass