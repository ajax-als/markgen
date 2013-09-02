Markgen
=======
##Summary
Markgen is a simple [web app](http://markupgen.appspot.com) that (at the moment) generates "actions" markup for [GMail Actions](https://developers.google.com/gmail/schemas/overview) (schema.org in microdata and JSON-LD syntax) and  for [Yandex Islands](http://beta.yandex.com) (OGP, schema.org in JSON-LD syntax). Produced markup can be easily embedded to web page, email, etc. without any additional processing.

##Markup details
While it is always an issue to use third-party generated code in own visible part of html, one can easily integrate any markup in invisible parts (e.g., in 'head' area). The tool aims for such kind of data - just copy-paste result to the place you need. This is achieved by using 'script' tag (for JSON-LD syntax) and 'meta' tag (for OGP and microdata syntax). 

At the moment following types of markup are supported:
	- [Google GMail Actions](https://developers.google.com/gmail/schemas/overview) - schema.org in JSON-LD and microdata syntax
		- [One Click Action](https://developers.google.com/gmail/schemas/reference/one-click-action)
		Ex: confirm expense report ([JSON-LD](http://markupgen.appspot.com/gm_actions?gm_action_type=one_click&action=confirm&method=get&name=Approve+Expense&url=https%3A%2F%2Fmyexpenses.com%2Fapprove%3FexpenseId%3Dabc123&description=Approval+request+for+John%27s+%2410.13+expense+for+office+supplies&format=jsonld#response), [Microdata](http://markupgen.appspot.com/gm_actions?gm_action_type=one_click&action=confirm&method=get&name=Approve+Expense&url=https%3A%2F%2Fmyexpenses.com%2Fapprove%3FexpenseId%3Dabc123&description=Approval+request+for+John%27s+%2410.13+expense+for+office+supplies&format=microdata#response))
		- [RSVP Action](https://developers.google.com/gmail/schemas/reference/rsvp-action)
		Ex: Taco Night at Google ([JSON-LD](http://markupgen.appspot.com/gm_actions?gm_action_type=rsvp&start_date=2015-04-18T15%3A30%3A00Z&end_date=2015-04-18T16%3A30%3A00Z&event_name=Taco+Night&location_name=Google&street_address=24+Willie+Mays+Plaza&address_locality=San+Francisco&address_region=CA&postal_code=94107&address_country=USA&yes_url=http%3A%2F%2Fmysite.com%2Frsvp%3FeventId%3D123%26value%3Dyes&no_url=http%3A%2F%2Fmysite.com%2Frsvp%3FeventId%3D123%26value%3Dno&maybe_url=http%3A%2F%2Fmysite.com%2Frsvp%3FeventId%3D123%26value%3Dmaybe&format=jsonld#response), [Microdata](http://markupgen.appspot.com/gm_actions?gm_action_type=rsvp&start_date=2015-04-18T15%3A30%3A00Z&end_date=2015-04-18T16%3A30%3A00Z&event_name=Taco+Night&location_name=Google&street_address=24+Willie+Mays+Plaza&address_locality=San+Francisco&address_region=CA&postal_code=94107&address_country=USA&yes_url=http%3A%2F%2Fmysite.com%2Frsvp%3FeventId%3D123%26value%3Dyes&no_url=http%3A%2F%2Fmysite.com%2Frsvp%3FeventId%3D123%26value%3Dno&maybe_url=http%3A%2F%2Fmysite.com%2Frsvp%3FeventId%3D123%26value%3Dmaybe&format=microdata#response))
		- [Review Action](https://developers.google.com/gmail/schemas/reference/review-action)
		Ex: review restaurant with rating and review text ([JSON-LD](http://markupgen.appspot.com/gm_actions?gm_action_type=review&description=We+hope+you+enjoyed+your+meal+at+Joe%27s+Diner.+Please+tell+us+about+it.&item=FoodEstablishment&item_name=Joe%27s+Diner&method=post&url=http%3A%2F%2Freviews.com%2Freview%3Fid%3D123&rating_asked=True&rating_required=rating_req&worst=1&best=5&comment_asked=True&comment_required=comment_opt&format=jsonld#response), [Microdata](http://markupgen.appspot.com/gm_actions?gm_action_type=review&description=We+hope+you+enjoyed+your+meal+at+Joe%27s+Diner.+Please+tell+us+about+it.&item=FoodEstablishment&item_name=Joe%27s+Diner&method=post&url=http%3A%2F%2Freviews.com%2Freview%3Fid%3D123&rating_asked=True&rating_required=rating_req&worst=1&best=5&comment_asked=True&comment_required=comment_opt&format=microdata#response))
		- [Go-To Action](https://developers.google.com/gmail/schemas/reference/go-to-action)
		Ex: watch movie online ([JSON-LD](http://markupgen.appspot.com/gm_actions?gm_action_type=go_to&description=Watch+the+%27Avengers%27+movie+online.&url=https%3A%2F%2Fwatch-movies.com%2Fwatch%3FmovieId%3Dabc123&name=&format=jsonld#response), [Microdata](http://markupgen.appspot.com/gm_actions?gm_action_type=go_to&description=Watch+the+%27Avengers%27+movie+online.&url=https%3A%2F%2Fwatch-movies.com%2Fwatch%3FmovieId%3Dabc123&name=&format=microdata#response))

	- [Yandex Islands Actions at SERP](http://beta.yandex.com) - extension for Open Graph Protocol by Yandex, schema.org in JSON-LD syntax
		- [Form defined in separate XML file](http://help.yandex.com/webmaster/?id=1127882)
		Ex: XML form with two default params ([OGP](http://markupgen.appspot.com/ya_actions?ya_action_type=xml_form&url=http%3A%2F%2Fexample.com%2Fmy_xml_url.xml&def0_name=property_name&def0_value=property_default_value&def1_name=property_2_name&def1_value=property_2_default_value&def2_name=&def2_value=&def3_name=&def3_value=&def4_name=&def4_value=&format=ogp#response),  [Schema.org](http://markupgen.appspot.com/ya_actions?ya_action_type=xml_form&url=http%3A%2F%2Fexample.com%2Fmy_xml_url_1.xml&def0_name=property_name&def0_value=property_def_value&def1_name=property_2_name&def1_value=property_2_def_value&def2_name=&def2_value=&def3_name=&def3_value=&def4_name=&def4_value=&format=schema#response)) 
		- [Action Button](http://help.yandex.com/webmaster/?id=1127989)
		Ex: check in for a flight ([OGP](http://markupgen.appspot.com/ya_actions?ya_action_type=button&button_type=CheckInAction&url=http%3A%2F%2Fwww.example.com%2Fcheck_in&format=ogp#response), [Schema.org](http://markupgen.appspot.com/ya_actions?ya_action_type=button&button_type=CheckInAction&url=http%3A%2F%2Fwww.example.com%2Fcheck_in&format=schema.org#response))

All examples are taken from the product docs.

##Plans
While the first version is done there is room for improvements. This is a list of the next steps as I see it. I prefer to follow it but appreciate any feedback and suggestions.

	- Tests
	Flying in manual testing mode so far. It's a shame, should be corrected. 

	- Validation for different types of data (url, datetime, etc)
	HTML5 input types are poorly supported by browsers for now, so self-written type validation would be nice to have. 

	- GMail RSVP Action has two datetime properties (one of which required). Datetime input type killed my phone browser so now they're text fields. This is extremely confusing since one must provide dates in ISO 8601. Should be done with JS calendar or smth like that.

	- It would be convenient to have cute "Copy to clipboard" button for response area. As I've figured out so far there is no universal way of doing so. Should investigate. 

	- Actually XML form (Yandex Islands) may have infinite number of properties with default values. Now up to five can be provided cause it was a bit easier to code. Should be corrected.

	- The next step from the latter - more real-time, less peculiar "Confirm" buttons. That is response should be generated right in the same moment with filling the form.

	- Integration with product instruments: check using appropriate validators, send email with markup (for GMail actions), etc. 

	- More types for "invisible" embedding: [Gmail Reservations](https://developers.google.com/gmail/schemas/reference/event-reservation), [GMail Orders](https://developers.google.com/gmail/schemas/reference/order), [Yandex Target Audience](http://help.yandex.ru/webmaster/?id=1127899)

	- Find or write lib for constructing JSON-LD and microdata. For now it is made "by hand" for every specific action type which is ugly. 

	- Evolving the latter: the best solution is to construct automate which has markup spec as input and html form plus class-processor as output. 

	- Web app is useful. But maybe CMS plugins or libs would be even more useful. 