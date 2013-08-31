import webapp2
import jinja2
import os
from gmaction import GmAction

class GmRsvp(GmAction):
  """Class for Gmail RSVP Actions"""
  TEMPLATE_NAME = os.path.join('google', 'gm_rsvp.html')
  
  def __init__(self):
    super(GmRsvp, self).__init__()

    self._start_date = ""
    self._end_date = ""

    self._event_name = ""

    self._location_name = ""
    self._street_address = ""
    self._address_locality = ""
    self._address_region = ""
    self._postal_code = ""
    self._address_country = ""

    self._yes_url = ""
    self._no_url = ""
    self._maybe_url = ""

    self._help_params["oneclick_selected"] = ""
    self._help_params["rsvp_selected"] = "selected"
    self._help_params["review_selected"] = ""
    self._help_params["goto_selected"] = ""


  def handler(self, jinja_env, request):
    self._start_date = request.get("start_date", "").strip()
    self._end_date = request.get("end_date", "").strip()

    self._event_name = request.get("event_name", "").strip()

    self._location_name = request.get("location_name", "").strip()
    self._street_address = request.get("street_address", "").strip()
    self._address_locality = request.get("address_locality", "").strip()
    self._address_region = request.get("address_region", "").strip()
    self._postal_code = request.get("postal_code", "").strip()
    self._address_country = request.get("address_country", "").strip()

    self._yes_url = request.get("yes_url", "").strip()
    self._no_url = request.get("no_url", "").strip()
    self._maybe_url = request.get("maybe_url", "").strip()

    self._format = super(GmRsvp, self).handler(jinja_env, request)
    
    if self._format == GmAction.JSON_LD:
      self._gen_jsonld()
    else:
      self._gen_microdata()

    template = jinja_env.get_template(GmRsvp.TEMPLATE_NAME)
    return template.render(start_date = self._start_date, 
      end_date = self._end_date, event_name = self._event_name, 
      location_name = self._location_name, street_address = self._street_address, 
      address_locality = self._address_locality, address_region = self._address_region,
      postal_code = self._postal_code, address_country = self._address_country,
      yes_url = self._yes_url, no_url = self._no_url, maybe_url = self._maybe_url,
      response = self._response, **self._help_params)

  def _gen_jsonld(self):
    def _add_handler_json(url, schema_type, comma_ahead):
      if url == "": return False

      if comma_ahead: 
        self._response += ','
      
      self._response += '\n    {\n'
      self._response += '      "@type": "RsvpAction",\n'
      self._response += '      "handler": {\n'
      self._response += '        "@type": "HttpActionHandler",\n'
      self._response += '        "url": "{0}"\n'.format(url)
      self._response += '      },\n'
      self._response += '      "attendance": "{0}"\n'.format(schema_type)
      self._response += '    }'

      return True


    if self._miss_req():
      return

    self._response        = '<script type="application/ld+json">\n{\n'
    self._response       += '  "@context": "http://schema.org",\n'
    self._response       += '  "@type": "Event",\n'
    self._response       += '  "name": "{0}",\n'.format(self._event_name)
    self._response       += '  "startDate": "{0}"'.format(self._start_date)
    
    if self._end_date != '':
      self._response     += ',\n  "endDate": "{0}"'.format(self._end_date)

    if not self._loc_empty():
      self._response     += ',\n  "location": {\n'
      self._response     += '    "@type": "Place",\n'
      self._response     += '    "address": {\n'
      self._response     += '      "@type": "PostalAddress"'

      if self._location_name != "":
        self._response   += ',\n      "name": "{0}"'.format(self._location_name)

      if self._street_address != "":
        self._response   += ',\n      "streetAddress": "{0}"'.format(self._street_address)

      if self._address_locality != "":
        self._response   += ',\n      "addressLocality": "{0}"'.format(self._address_locality)

      if self._address_region != "":
        self._response   += ',\n      "addressRegion": "{0}"'.format(self._address_region)

      if self._postal_code != "":
        self._response   += ',\n      "postalCode": "{0}"'.format(self._postal_code)

      if self._address_country != "":
        self._response   += ',\n      "addressCountry": "{0}"'.format(self._address_country)

      self._response     += '\n    }\n  }' 

    self._response       += ',\n  "action": ['

    comma_ahead = False
    comma_ahead = _add_handler_json(self._yes_url, 
      "http://schema.org/RsvpAttendance/Yes", comma_ahead)
    comma_ahead = _add_handler_json(self._no_url, 
      "http://schema.org/RsvpAttendance/No", comma_ahead)
    _add_handler_json(self._maybe_url, 
      "http://schema.org/RsvpAttendance/Maybe", comma_ahead)

    self._response     += '\n  ]\n}\n</script>\n'

  def _gen_microdata(self):
    def _add_handler_microdata(url, schema_type):
      if url == "": return False

      self._response += '  <div itemprop="action" itemscope '
      self._response += 'itemtype="http://schema.org/RsvpAction">\n'
      self._response += '    <div itemprop="handler" itemscope '
      self._response += 'itemtype="http://schema.org/HttpActionHandler">\n'
      self._response += '      <link itemprop="url" href="{0}"/>\n'.format(url)
      self._response += '    </div>\n'
      self._response += '    <link itemprop="attendance" href="{0}"/>"\n'.format(
        schema_type)
      self._response += '  </div>\n'

      return True


    if self._miss_req():
      return

    self._response      = '<div itemscope itemtype="http://schema.org/Event">\n'
    self._response     += '  <meta itemprop="name" content="{0}"/>\n'.format(
      self._event_name)
    self._response     += '  <meta itemprop="startDate" content="{0}"/>\n'.format(
      self._start_date)

    if self._end_date != '':
      self._response   += '  <meta itemprop="endDate" content="{0}"/>\n'.format(
      self._end_date)

    if not self._loc_empty():
      self._response   += '  <div itemprop="location" itemscope itemtype="http://schema.org/Place">\n'
      self._response   += '    <div itemprop="address" itemscope itemtype="http://schema.org/PostalAddress">\n'

      if self._location_name != '':
        self._response += '      <meta itemprop="name" content="{0}"/>\n'.format(
          self._location_name)

      if self._street_address != '':
        self._response += '      <meta itemprop="streetAddress" content="{0}"/>\n'.format(
          self._street_address)

      if self._address_locality != '':
        self._response += '      <meta itemprop="addressLocality" content="{0}"/>\n'.format(
          self._address_locality)

      if self._address_region != '':
        self._response += '      <meta itemprop="addressRegion" content="{0}"/>\n'.format(
          self._address_region)

      if self._postal_code != '':
        self._response += '      <meta itemprop="postalCode" content="{0}"/>\n'.format(
          self._postal_code)

      if self._address_country != '':
        self._response += '      <meta itemprop="addressCountry" content="{0}"/>\n'.format(
          self._address_country)

      self._response   += '    </div>\n'
      self._response   += '  </div>\n'

    _add_handler_microdata(self._yes_url, "http://schema.org/RsvpAttendance/Yes")
    _add_handler_microdata(self._no_url, "http://schema.org/RsvpAttendance/No")
    _add_handler_microdata(self._maybe_url, "http://schema.org/RsvpAttendance/Maybe")

    self._response   += '</div>\n'

  def _miss_req(self):
    self._response = "Required properties: "
    result = False

    if self._event_name == '':
      self._response += "event name, "
      result = True

    if self._start_date == '':
      self._response += "start date, "
      result = True

    if self._yes_url == '' and self._no_url == '' and self._maybe_url == '':
      self._response += "at least one of handler urls"
      result = True

    return result

  def _loc_empty(self):
    return (self._location_name == "" and self._street_address == ""
    and self._address_locality == "" and self._address_region == ""
    and self._postal_code == "" and self._address_country == "")