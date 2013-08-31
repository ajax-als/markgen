import webapp2
import jinja2
import os
from yaaction import YaAction

class YaXML(YaAction):
  """Class for Ya.Islands XML form"""

  TEMPLATE_NAME = os.path.join('yandex', 'ya_xml.html')
  DEF_PROP_NUM = 5
  
  def __init__(self):
    super(YaXML, self).__init__()

    self._url = ""

    self._help_params["xml_selected"] = "selected"
    self._help_params["button_selected"] = ""

    self._def_num = 0
    self._fdef_name = ""
    self._fdef_value = ""

    self._def_names = []
    for i in xrange(YaXML.DEF_PROP_NUM):
      name = "def" + str(i) + "_name"
      value = "def" + str(i) + "_value"
      self._def_names.append((name, value))

  def handler(self, jinja_env, request):
    self._url = request.get("url", "").strip()

    self._def_num = 0
    for elem in self._def_names:
      name = request.get(elem[0], "").strip()
      value = request.get(elem[1], "").strip()

      self._help_params[elem[0]] = name
      self._help_params[elem[1]] = value

      if name != "":
        self._def_num += 1; 

        if self._def_num == 1:
          self._fdef_name = name
          self._fdef_value = value

    self._format = super(YaXML, self).handler(jinja_env, request)

    if self._format == YaAction.OGP:
      self._gen_ogp()
    else:
      self._gen_schema()

    template = jinja_env.get_template(YaXML.TEMPLATE_NAME)
    return template.render(url=self._url, response=self._response, 
      **self._help_params)

    
  def _gen_ogp(self):
    if self._miss_req():
      return

    self._response      = '<html prefix="ya: http://webmaster.yandex.ru/vocabularies/">\n'
    self._response     += '  <meta property="ya:interaction" content="XML_FORM"/>\n'
    self._response     += '  <meta property="ya:interaction:url" content="{0}" />\n'.format(
      self._url)

    for elem in self._def_names:
      if self._help_params[elem[0]] != "":
        self._response += '  <meta property="ya:interaction:property" content="{0}" />\n'.format(
          self._help_params[elem[0]])
        self._response += '  <meta property="ya:interaction:default_value" content="{0}" />\n'.format(
          self._help_params[elem[1]])

  
  def _gen_schema(self):
    def _add_def_property(name, value, indent):
      self._response += '\n'    
      self._response += indent + '"@type" : "FormProperty",\n'
      self._response += indent + '"name" : "{0}",\n'.format(name)
      self._response += indent + '"defaultValue" : "{0}"'.format(value)

    if self._miss_req():
      return

    self._response         = '<script type="application/ld+json"> {'
    self._response        += '\n  "@context": "http://schema.org"'
    self._response        += ',\n  "@type": "WebFormHandler"'
    self._response        += ',\n  "specificationUrl": "{0}"'.format(self._url)

    if self._def_num > 1:
      comma = False
      self._response      += ',\n  "defaultProperty" : ['

      for elem in self._def_names:
        if self._help_params[elem[0]] != "":
          if comma: 
            self._response += ','

          self._response   += '\n    {'
          _add_def_property(self._help_params[elem[0]], self._help_params[elem[1]], '      ')
          self._response   += '\n    }'
          comma = True

      self._response       += '\n  ]'
    elif self._def_num == 1:
        self._response     += ',\n  "defaultProperty" : {'
        _add_def_property(self._fdef_name, self._fdef_value, '    ')
        self._response     += '\n  }'
   
    self._response         += '\n}'
    self._response         += '\n</script>'

  def _miss_req(self):
    if self._url == '':
      self._response = 'Required fields: URL'
      return True

    return False


