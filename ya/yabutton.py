import webapp2
import jinja2
import os
from yaaction import YaAction

class YaButton(YaAction):
  """Class for Ya.Islands Button"""
  TEMPLATE_NAME = os.path.join('yandex', 'ya_button.html')
  
  def __init__(self):
    super(YaButton, self).__init__()

    self._url = ""

    self._help_params["xml_selected"] = ""
    self._help_params["button_selected"] = "selected"

    self._button_type = ""

    self._button_types = ("ApplyAction", "AskAction", "BuyAction", "CalculateAction", 
      "CheckAction", "CheckInAction", "CommunicateAction", "DownloadAction", 
      "FollowAction", "InstallAction", "ListenAction", "OrderAction", "PayAction", 
      "PlayAction", "ReadAction", "RegisterAction", "RentAction", "ReserveAction", 
      "ReviewAction", "ScheduleAction", "SearchAction", "SubscribeAction", 
      "TrackAction", "ViewAction", "WatchAction")


  def handler(self, jinja_env, request):
    self._url = request.get("url", "").strip()
    
    self._button_type = request.get("button_type", "ApplyAction")
    for cur_type in self._button_types:
      self._help_params[cur_type] = ""
    self._help_params[self._button_type] = "selected"

    self._format = super(YaButton, self).handler(jinja_env, request)
    if self._format == YaAction.OGP:
      self._gen_ogp()
    else:
      self._gen_schema()

    template = jinja_env.get_template(YaButton.TEMPLATE_NAME)
    return template.render(url=self._url, response=self._response, 
      **self._help_params)

    
  def _gen_ogp(self):
    if self._miss_req():
      return

    self._response      = '<html prefix="ya: http://webmaster.yandex.ru/vocabularies/">'
    self._response     += '\n  <meta property="ya:interaction" content="BUTTON"/>'
    self._response     += '\n  <meta property="ya:interaction:type" content="{0}"/>'.format(
      self._button_type)
    self._response     += '\n  <meta property="ya:interaction:url" content="{0}" />'.format(
      self._url)

    if self._button_type == "AskAction":
      self._response   += '\n  <meta property="ya:interaction:object" content="Accreditation" />'
    elif self._button_type == "CheckInAction":
      self._response   += '\n  <meta property="ya:interaction:object" content="Flight" />'
    elif self._button_type == "CommunicateAction":
      self._response   += '\n  <meta property="ya:interaction:instrument" content="EmailMessage" />'
  
  def _gen_schema(self):
    if self._miss_req():
      return

    self._response      = '<script type="application/ld+json"> {'
    self._response     += '\n  "@context": "http://schema.org"'
    self._response     += ',\n  "@type": "{0}"'.format(self._button_type)
    self._response     += ',\n  "url": "{0}"'.format(self._url)

    if self._button_type == "AskAction":
      self._response += ',\n  "object" : {'
      self._response += '\n    "@type" : "Accreditation"'
      self._response += '\n  }'
    elif self._button_type == "CheckInAction":
      self._response += ',\n  "object" : {'
      self._response += '\n    "@type" : "Flight"'
      self._response += '\n  }'
    elif self._button_type == "CommunicateAction":
      self._response += ',\n  "instrument" : {'
      self._response += '\n    "@type" : "EmailMessage"'
      self._response += '\n  }'

    self._response     += '\n}'
    self._response     += '\n</script>'

  def _miss_req(self):
    if self._url == '':
      self._response = 'Required fields: URL'
      return True

    return False


