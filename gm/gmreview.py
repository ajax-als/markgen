import webapp2
import jinja2
import os
from gmaction import GmAction

class GmReview(GmAction):
  """Class for Gmail Review Actions"""
  TEMPLATE_NAME = os.path.join('google', 'gm_review.html')

  ITEM_RESTAURANT = "FoodEstablishment"
  ITEM_MOVIE = "Movie"
  ITEM_PRODUCT = "Product"

  HTTP_GET = "get"
  HTTP_POST = "post"

  COMMENT_REQ = "comment_req"
  COMMENT_OPT = "comment_opt"

  RATING_REQ = "rating_req"
  RATING_OPT = "rating_opt"
  
  def __init__(self):
    super(GmReview, self).__init__()
    self._description = ""

    self._item = GmReview.ITEM_RESTAURANT
    self._item_name = ""

    self._method = ""
    self._url = ""

    self._rating_asked = False
    self._best = 0
    self._worst = 0
    self._rating_required = False
    self._rating_req = ""
    self._rating_opt = ""

    self._comment_asked = False
    self._comment_required = False

    self._help_params["oneclick_selected"] = ""
    self._help_params["rsvp_selected"] = ""
    self._help_params["review_selected"] = "selected"
    self._help_params["goto_selected"] = ""

    
  def handler(self, jinja_env, request):
    self._item = request.get("item", GmReview.ITEM_RESTAURANT)
    if self._item == GmReview.ITEM_RESTAURANT:
      self._help_params["rest_selected"] = "selected"
      self._help_params["mov_selected"] = ""
      self._help_params["pr_selected"] = ""
    elif self._item == GmReview.ITEM_MOVIE:
      self._help_params["rest_selected"] = ""
      self._help_params["mov_selected"] = "selected"
      self._help_params["pr_selected"] = ""
    elif self._item == GmReview.ITEM_PRODUCT:
      self._help_params["rest_selected"] = ""
      self._help_params["mov_selected"] = ""
      self._help_params["pr_selected"] = "selected"

    self._description = request.get("description", "").strip()
    self._item_name = request.get("item_name", "").strip()  

    self._method = request.get("method", GmReview.HTTP_GET)
    if self._method == GmReview.HTTP_GET:
      self._help_params["get_selected"] = "selected"
      self._help_params["post_selected"] = ""
    else: #http post
      self._help_params["get_selected"] = ""
      self._help_params["post_selected"] = "selected"

    self._url = request.get("url", "").strip()
    
    self._rating_asked = bool(request.get("rating_asked", False))
    if self._rating_asked:
      self._help_params["rating_checked"] = "checked"
    else:
      self._help_params["rating_checked"] = ""

    self._worst = int(request.get("worst", 1))
    self._best  = int(request.get("best", 5))
    if self._best == 5:
        self._help_params["five_selected"] = "selected"
        self._help_params["four_selected"] = ""
        self._help_params["three_selected"] = ""
        self._help_params["two_selected"] = ""
        self._help_params["one_selected"] = ""

    elif self._best == 4:
        self._help_params["five_selected"] = ""
        self._help_params["four_selected"] = "selected"
        self._help_params["three_selected"] = ""
        self._help_params["two_selected"] = ""
        self._help_params["one_selected"] = ""

    elif self._best == 3:
        self._help_params["five_selected"] = ""
        self._help_params["four_selected"] = ""
        self._help_params["three_selected"] = "selected"
        self._help_params["two_selected"] = ""
        self._help_params["one_selected"] = ""

    elif self._best == 2: 
        self._help_params["five_selected"] = ""
        self._help_params["four_selected"] = ""
        self._help_params["three_selected"] = ""
        self._help_params["two_selected"] = "selected"
        self._help_params["one_selected"] = ""

    elif self._best == 1:
        self._help_params["five_selected"] = ""
        self._help_params["four_selected"] = ""
        self._help_params["three_selected"] = ""
        self._help_params["two_selected"] = ""
        self._help_params["one_selected"] = "selected"

    self._rating_required = (request.get("rating_required", GmReview.RATING_REQ) == GmReview.RATING_REQ)
    if self._rating_required :
      self._help_params["rating_req_selected"] = "selected"
      self._help_params["rating_opt_selected"] = ""
    else: #optional
      self._help_params["rating_req_selected"] = ""
      self._help_params["rating_opt_selected"] = "selected"

    self._comment_asked = bool(request.get("comment_asked", False))
    if self._comment_asked:
      self._help_params["comment_checked"] = "checked"
    else:
      self._help_params["comment_checked"] = ""

    self._comment_required = (request.get("comment_required", GmReview.COMMENT_REQ) == GmReview.COMMENT_REQ)
    if self._comment_required:
      self._help_params["comment_req_selected"] = "selected"
      self._help_params["comment_opt_selected"] = ""
    else: #optional
      self._help_params["comment_req_selected"] = ""
      self._help_params["comment_opt_selected"] = "selected"
      
    self._format = super(GmReview, self).handler(jinja_env, request)
    if self._format == GmAction.JSON_LD:
      self._gen_jsonld()
    else:
      self._gen_microdata()

    template = jinja_env.get_template(GmReview.TEMPLATE_NAME)
    return template.render(description = self._description, 
      item_name = self._item_name, url = self._url,
      response = self._response, 
      **self._help_params)

  def _gen_jsonld(self):
    def _add_property_json(name, req, indent):
      self._response   += ',\n'
      if req:
        self._response += indent + '"requiredProperty": {\n'
      else:
        self._response += indent + '"optionalProperty": {\n'  

      self._response   += indent + '  "@type": "Property",\n'
      self._response   += indent + '  "name": "{0}"\n'.format(name)
      self._response   += indent + '}'

    def _add_properties_2_array(req, prop1, prop2, indent):
      self._response   += ',\n'
      if req:
        self._response += indent + '"requiredProperty": [\n'
      else:
        self._response += indent + '"optionalProperty": [\n'  

      self._response   += indent + "  {\n"

      self._response   += indent + '    "@type": "Property",\n'
      self._response   += indent + '    "name": "{0}"\n'.format(prop1)
      self._response   += indent + '  },\n'

      self._response   += indent + '  {\n'

      self._response   += indent + '    "@type": "Property",\n'
      self._response   += indent + '    "name": "{0}"\n'.format(prop2)
      self._response   += indent + '  }\n'
      self._response   += indent + "]"


    if self._miss_req(): return

    self._response        = '<script type="application/ld+json">'
    self._response       += '\n{'
    self._response       += '\n  "@context": "http://schema.org"'
    self._response       += ',\n  "@type": "EmailMessage"'

    if self._description != "":
      self._response     += ',\n  "description": "{0}"'.format(self._description)

    self._response       += ',\n  "action": {'
    self._response       += '\n    "@type": "ReviewAction"'
    self._response       += ',\n    "review": {'
    self._response       += '\n      "@type": "Review"'
    self._response       += ',\n      "itemReviewed": {'
    self._response       += '\n        "@type": "{0}"'.format(self._item)
    self._response       += ',\n        "name": "{0}"'.format(self._item_name)
    self._response       += '\n      }'

    if self._rating_asked:
      self._response     += ',\n      "reviewRating": {'
      self._response     += '\n        "@type": "Rating"'
      self._response     += ',\n        "bestRating" : "{0}"'.format(self._best)
      self._response     += ',\n        "worstRating" : "{0}"'.format(self._worst)
      self._response     += '\n      }'
    
    self._response       += '\n    }'
    self._response       += ',\n    "handler": {'
    self._response       += '\n      "@type": "HttpActionHandler"'
    self._response       += ',\n      "url": "{0}"'.format(self._url)

    if self._rating_asked and self._comment_asked:
      if self._rating_required and self._comment_required:
        _add_properties_2_array(True, "review.reviewRating.ratingValue", "review.reviewBody", "      ")
      elif not self._rating_required and not self._comment_required:
        _add_properties_2_array(False, "review.reviewRating.ratingValue", "review.reviewBody", "      ")
      else:
        _add_property_json("review.reviewRating.ratingValue", self._rating_required, "      ")
        _add_property_json("review.reviewBody", self._comment_required, "      ")
    else:
      if self._rating_asked:
        _add_property_json("review.reviewRating.ratingValue", self._rating_required, "      ")

      if self._comment_asked:
        _add_property_json("review.reviewBody", self._comment_required, "      ")

    if self._method == GmReview.HTTP_GET:
      self._response     += ',\n      "method": "http://schema.org/HttpRequestMethod/GET"'
    else:#post
      self._response     += ',\n      "method": "http://schema.org/HttpRequestMethod/POST"'

    self._response     += '\n    }'
    self._response     += '\n  }'
    self._response     += '\n}'
    self._response     += '\n</script>'

  def _gen_microdata(self):
    def _add_property_microdata(name, req, indent):
      if req:   
        self._response += indent + '<div itemprop="requiredProperty" itemscope '
      else:
        self._response += indent + '<div itemprop="optionalProperty" itemscope '

      self._response   += 'itemtype="http://schema.org/Property">\n'
      self._response   += indent + '  <meta itemprop="name" content="{0}"/>\n'.format(name)
      self._response   += indent + '</div>\n'


    if self._miss_req(): return

    self._response        = '<div itemscope itemtype="http://schema.org/EmailMessage">\n'

    if self._description != "":
      self._response     += '  <meta itemprop="description" content="{0}"/>\n'.format(
      self._description)

    self._response       += '  <div itemprop="action" itemscope '
    self._response       += 'itemtype="http://schema.org/ReviewAction">\n'
    self._response       += '    <div itemprop="review" itemscope '
    self._response       += 'itemtype="http://schema.org/Review">\n'
    self._response       += '      <div itemprop="itemReviewed" itemscope '
    self._response       += 'itemtype="http://schema.org/{0}">\n'.format(self._item)
    self._response       += '        <meta itemprop="name" content="{0}"/>\n'.format(self._item_name)
    self._response       += '      </div>\n'

    if self._rating_asked:
      self._response     += '      <div itemprop="reviewRating" itemscope '
      self._response     += 'itemtype="http://schema.org/Rating">\n'
      self._response     += '        <meta itemprop="bestRating" content="{0}"/>\n'.format(self._best)
      self._response     += '        <meta itemprop="worstRating" content="{0}"/>\n'.format(self._worst)
      self._response     += '      </div>\n'

    self._response       += '    </div>\n'

    self._response       += '    <div itemprop="handler" itemscope '
    self._response       += 'itemtype="http://schema.org/HttpActionHandler">\n'
    self._response       += '      <link itemprop="url" href="{0}"/>\n'.format(
      self._url)

    if self._rating_asked:
      _add_property_microdata("review.reviewRating.ratingValue", 
        self._rating_required, "      ")

    if self._comment_asked:
      _add_property_microdata("review.reviewBody", 
        self._comment_required, "      ")

    self._response       += '      <link itemprop="method" '
    if self._method == GmReview.HTTP_GET:
      self._response     += 'href="http://schema.org/HttpRequestMethod/GET"\n'
    else:#post
      self._response     += 'href="http://schema.org/HttpRequestMethod/POST"\n'

    self._response += '    </div>\n'
    self._response += '  </div>\n'
    self._response += '</div>'

#according to spec, mandatory fields are (classes projected to properties) -
#item_reviewed.name, handler.url,   
  def _miss_req(self):
    self._response = "Required properties: "
    result = False

    if self._item_name == '':
      self._response += "name of the item, "
      result = True

    if self._url == '':
      self._response += "url for handler"
      result = True

    return result