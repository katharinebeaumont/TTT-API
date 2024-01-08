from constants import GAME_ONTOLOGY_PREFIX, BASE_URL, GAME_ONTOLOGY_TAG

class ResponseWriter():

    def __init__(self, id, type_dsc):
        self.type_dsc = type_dsc
        self.id = id
            
        self.additional_fields = {}
        self.links = []
        self.forms = []

        self.context = {
            "@vocab": "https://www.w3.org/2019/wot/hypermedia#",
            GAME_ONTOLOGY_PREFIX: BASE_URL + GAME_ONTOLOGY_TAG + "#",
            "htv":"http://www.w3.org/2011/http#",
            "wot":"https://w3c.github.io/wot-thing-description/#",
            "sch":"https://schema.org/",
            "links":{ "@id": "Link" },
            "forms":{ "@id": "Form" },
            "href":{ "@id": "hasTarget" },
            "rel": { "@id": "hasRelationType", "@type": "@vocab" },
        }


    def add_link(self, link, rel=None, method_name=None):
        new_link = {
            "href":link
        }
        if rel:
            new_link["rel"]=rel

        if method_name:
            new_link["htv:methodName"]=method_name

        self.links = self.links + [new_link]


    def add_form(self, link, contentType, method_name, op=None):
        new_form = {
            "href":link,
            "contentType":contentType,
            "htv:methodName":method_name
        }

        if op:
            new_form["wot:op"]=op

        
        self.forms = self.forms + [new_form]


    def add_form_property(self, form_link, name, readOnly, reqiured):
        #1. Get form
        form = None
        for f in self.forms:
            if f["href"] == form_link:
                form = f
            
        #2. get properties
        # see https://stackoverflow.com/questions/65236613/restful-api-hateoas
        #See https://github.com/hateoas-forms/spring-hateoas-example
        #FIND ONTOLOGIES FOR THESE FIELDS
        # see this? https://json-schema.org/draft/2019-09/json-schema-hypermedia
        #NB don't think you can mix and match with JSON schema.
        if form:
            properties = []
            for key in form:
                if (key == "properties"):
                    properties = form["properties"]
            
            property = {
                        "name": name,
                        "readOnly": readOnly,
                        "required": reqiured
            }
            properties = properties + [property]
            form["properties"] = properties

        
    def add_field(self, label, value):
        self.additional_fields[label] = value

    
    def add_nested_field(self, label, key, value):
         #1. Get field if it exists already
        new_field =  {
            key: value
        }

        field = None
        for key in self.additional_fields:
            if key == label:
                field = self.additional_fields[label]

        
        if (field):
            field = field + [new_field]
            self.additional_fields[label] = field
        else:            
            self.additional_fields[label] = [ new_field ]


    def add_error(self, error_text):
        self.add_field("sch:error", error_text)

        
    # Return constructed response as json string
    def build(self):
        retval = {
            "@id": self.id,
            "@type": self.type_dsc,
            "@context": self.context,
        }

        if (len(self.additional_fields)>0):
            retval.update(self.additional_fields)

        if (len(self.links)>0):
            retval["links"]=self.links

        if (len(self.forms)>0):
            retval["forms"]=self.forms
        
        return retval

