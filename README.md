# TIC TAC TOE API

This API allows users to play a game of Tic-Tac-Toe against a bot, using RESTful API calls to various endpoints, which return JSON with hypermedia controls and the use of Hypermedia As The Engine Of Application State (HATEOAS). 

Important note: 
The form properties fields are entirely made up at the moment and need changing to something that fits an existing ontology (e.g. look to change this to be compatible with WOT descriptions)

## Game Play

The game play is as follows;

- The user registers at the endpoint /register, by POST request which includes the property "ttt:Agent" and the Agent URL
- This returns links and forms to play the game, with an assigned ID
- When the game is over, a link to the result, and form to register again are provided

For example:

#### Index page request:

GET http://localhost:8083/
Content-Type application/json

#### Index page response:

```
{
  "@id": "http://localhost:8083/",
  "@type": "ttt:Game",
  "@context": {
    "@vocab": "https://www.w3.org/2019/wot/hypermedia#",
    "ttt": "http://localhost:8083/tic-tac-toe#",
    "htv": "http://www.w3.org/2011/http#",
    "wot": "https://w3c.github.io/wot-thing-description/#",
    "sch": "https://schema.org/#",
    "links": {
      "@id": "Link"
    },
    "forms": {
      "@id": "Form"
    },
    "href": {
      "@id": "hasTarget"
    },
    "rel": {
      "@id": "hasRelationType",
      "@type": "@vocab"
    }
  },
  "ttt:Agent": "http://localhost:8083/apibot",
  "forms": [
    {
      "href": "http://localhost:8083/register",
      "contentType": "application/json",
      "htv:methodName": "POST",
      "wot:op": "readproperty",
      "properties": [
        {
          "name": "@id",
          "readOnly": false,
          "required": true
        }
      ]
    }
  ]
}
```

#### Register form request:

POST http://localhost:8083/register
Content-Type application/json

Body: 
```
{ 
 "@id": "http://agentURL.com",
  "@type":"ttt:Agent"
  "@context": {
    "ttt": "http://localhost:8083/tic-tac-toe#"
  }
}
```

#### Register form response::

```
{
  "@id": "http://localhost:8083/register",
  "@type": "",
  "@context": {
    "@vocab": "https://www.w3.org/2019/wot/hypermedia#",
    "ttt": "http://localhost:8083/tic-tac-toe#",
    "htv": "http://www.w3.org/2011/http#",
    "wot": "https://w3c.github.io/wot-thing-description/#",
    "sch": "https://schema.org/#",
    "links": {
      "@id": "Link"
    },
    "forms": {
      "@id": "Form"
    },
    "href": {
      "@id": "hasTarget"
    },
    "rel": {
      "@id": "hasRelationType",
      "@type": "@vocab"
    }
  },
  "links": [
    {
      "href": "http://localhost:8083/",
      "htv:methodName": "GET"
    },
    {
      "href": "http://localhost:8083/Board?id=1df666f8-6e74-4e51-8ad3-7f807bd380cc",
      "htv:methodName": "GET"
    }
  ],
  "forms": [
    {
      "href": "http://localhost:8083/Square11?id=1df666f8-6e74-4e51-8ad3-7f807bd380cc",
      "contentType": "application/json",
      "htv:methodName": "PUT",
      "wot:op": "readproperty"
    },
    {
      "href": "http://localhost:8083/Square12?id=1df666f8-6e74-4e51-8ad3-7f807bd380cc",
      "contentType": "application/json",
      "htv:methodName": "PUT",
      "wot:op": "readproperty"
    },
    {
      "href": "http://localhost:8083/Square13?id=1df666f8-6e74-4e51-8ad3-7f807bd380cc",
      "contentType": "application/json",
      "htv:methodName": "PUT",
      "wot:op": "readproperty"
    },
    {
      "href": "http://localhost:8083/Square21?id=1df666f8-6e74-4e51-8ad3-7f807bd380cc",
      "contentType": "application/json",
      "htv:methodName": "PUT",
      "wot:op": "readproperty"
    },
    {
      "href": "http://localhost:8083/Square22?id=1df666f8-6e74-4e51-8ad3-7f807bd380cc",
      "contentType": "application/json",
      "htv:methodName": "PUT",
      "wot:op": "readproperty"
    },
    {
      "href": "http://localhost:8083/Square23?id=1df666f8-6e74-4e51-8ad3-7f807bd380cc",
      "contentType": "application/json",
      "htv:methodName": "PUT",
      "wot:op": "readproperty"
    },
    {
      "href": "http://localhost:8083/Square31?id=1df666f8-6e74-4e51-8ad3-7f807bd380cc",
      "contentType": "application/json",
      "htv:methodName": "PUT",
      "wot:op": "readproperty"
    },
    {
      "href": "http://localhost:8083/Square32?id=1df666f8-6e74-4e51-8ad3-7f807bd380cc",
      "contentType": "application/json",
      "htv:methodName": "PUT",
      "wot:op": "readproperty"
    },
    {
      "href": "http://localhost:8083/Square33?id=1df666f8-6e74-4e51-8ad3-7f807bd380cc",
      "contentType": "application/json",
      "htv:methodName": "PUT",
      "wot:op": "readproperty"
    }
  ]
}
```

#### Square Form Request:

PUT http://localhost:8083/Square12?id=1df666f8-6e74-4e51-8ad3-7f807bd380cc
Content-Type application/json
(No body)

#### Square Form Response:

```
{
  "@id": "http://localhost:8083/Square12?id=1df666f8-6e74-4e51-8ad3-7f807bd380cc",
  "@type": "ttt:Square12",
  "@context": {
    "@vocab": "https://www.w3.org/2019/wot/hypermedia#",
    "ttt": "http://localhost:8083/tic-tac-toe#",
    "htv": "http://www.w3.org/2011/http#",
    "wot": "https://w3c.github.io/wot-thing-description/#",
    "sch": "https://schema.org/#",
    "links": {
      "@id": "Link"
    },
    "forms": {
      "@id": "Form"
    },
    "href": {
      "@id": "hasTarget"
    },
    "rel": {
      "@id": "hasRelationType",
      "@type": "@vocab"
    }
  },
  "ttt:moveTakenBy": "http://agentURL.com",
  "links": [
    {
      "href": "http://localhost:8083/",
      "htv:methodName": "GET"
    },
    {
      "href": "http://localhost:8083/Board?id=1df666f8-6e74-4e51-8ad3-7f807bd380cc",
      "htv:methodName": "GET"
    }
  ]
}
```

#### Board Request:

GET http://localhost:8083/Board?id=1df666f8-6e74-4e51-8ad3-7f807bd380cc
Content-Type application/json

#### Board Response:

```
{
  "@id": "http://localhost:8083/Board?id=1df666f8-6e74-4e51-8ad3-7f807bd380cc",
  "@type": "ttt:Board",
  "@context": {
    "@vocab": "https://www.w3.org/2019/wot/hypermedia#",
    "ttt": "http://localhost:8083/tic-tac-toe#",
    "htv": "http://www.w3.org/2011/http#",
    "wot": "https://w3c.github.io/wot-thing-description/#",
    "sch": "https://schema.org/#",
    "links": {
      "@id": "Link"
    },
    "forms": {
      "@id": "Form"
    },
    "href": {
      "@id": "hasTarget"
    },
    "rel": {
      "@id": "hasRelationType",
      "@type": "@vocab"
    }
  },
  "ttt:hasSquare": [
    {
      "http://localhost:8083/Square11?id=1df666f8-6e74-4e51-8ad3-7f807bd380cc": {
        "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": "http://localhost:8083/tic-tac-toe#Square11",
        "http://localhost:8083/tic-tac-toe#moveTakenBy": "http://localhost:8083/apibot"
      }
    },
    {
      "http://localhost:8083/Square12?id=1df666f8-6e74-4e51-8ad3-7f807bd380cc": {
        "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": "http://localhost:8083/tic-tac-toe#Square12",
        "http://localhost:8083/tic-tac-toe#moveTakenBy": "http://agentURL.com"
      }
    }
  ],
  "links": [
    {
      "href": "http://localhost:8083/",
      "htv:methodName": "GET"
    },
    {
      "href": "http://localhost:8083/Board?id=1df666f8-6e74-4e51-8ad3-7f807bd380cc",
      "htv:methodName": "GET"
    }
  ],
  "forms": [
    {
      "href": "http://localhost:8083/Square13?id=1df666f8-6e74-4e51-8ad3-7f807bd380cc",
      "contentType": "application/json",
      "htv:methodName": "PUT",
      "wot:op": "readproperty"
    },
    {
      "href": "http://localhost:8083/Square21?id=1df666f8-6e74-4e51-8ad3-7f807bd380cc",
      "contentType": "application/json",
      "htv:methodName": "PUT",
      "wot:op": "readproperty"
    },
    {
      "href": "http://localhost:8083/Square22?id=1df666f8-6e74-4e51-8ad3-7f807bd380cc",
      "contentType": "application/json",
      "htv:methodName": "PUT",
      "wot:op": "readproperty"
    },
    {
      "href": "http://localhost:8083/Square23?id=1df666f8-6e74-4e51-8ad3-7f807bd380cc",
      "contentType": "application/json",
      "htv:methodName": "PUT",
      "wot:op": "readproperty"
    },
    {
      "href": "http://localhost:8083/Square31?id=1df666f8-6e74-4e51-8ad3-7f807bd380cc",
      "contentType": "application/json",
      "htv:methodName": "PUT",
      "wot:op": "readproperty"
    },
    {
      "href": "http://localhost:8083/Square32?id=1df666f8-6e74-4e51-8ad3-7f807bd380cc",
      "contentType": "application/json",
      "htv:methodName": "PUT",
      "wot:op": "readproperty"
    },
    {
      "href": "http://localhost:8083/Square33?id=1df666f8-6e74-4e51-8ad3-7f807bd380cc",
      "contentType": "application/json",
      "htv:methodName": "PUT",
      "wot:op": "readproperty"
    }
  ]
}
```

### ...Winning Requests

PUT http://localhost:8083/Square22?id=1df666f8-6e74-4e51-8ad3-7f807bd380cc
PUT http://localhost:8083/Square32?id=1df666f8-6e74-4e51-8ad3-7f807bd380cc

### Response

```
{
  "@id": "http://localhost:8083/Square32?id=1df666f8-6e74-4e51-8ad3-7f807bd380cc",
  "@type": "ttt:Square32",
  "@context": {
    "@vocab": "https://www.w3.org/2019/wot/hypermedia#",
    "ttt": "http://localhost:8083/tic-tac-toe#",
    "htv": "http://www.w3.org/2011/http#",
    "wot": "https://w3c.github.io/wot-thing-description/#",
    "sch": "https://schema.org/#",
    "links": {
      "@id": "Link"
    },
    "forms": {
      "@id": "Form"
    },
    "href": {
      "@id": "hasTarget"
    },
    "rel": {
      "@id": "hasRelationType",
      "@type": "@vocab"
    }
  },
  "ttt:moveTakenBy": "http://agentURL.com",
  "links": [
    {
      "href": "http://localhost:8083/",
      "htv:methodName": "GET"
    },
    {
      "href": "http://localhost:8083/Board?id=1df666f8-6e74-4e51-8ad3-7f807bd380cc",
      "htv:methodName": "GET"
    },
    {
      "href": "http://localhost:8083/result?id=1df666f8-6e74-4e51-8ad3-7f807bd380cc",
      "htv:methodName": "GET"
    }
  ]
}
```

### Request

GET http://localhost:8083/result?id=1df666f8-6e74-4e51-8ad3-7f807bd380cc

### Response

```
{
  "@id": "http://localhost:8083/result?id=1df666f8-6e74-4e51-8ad3-7f807bd380cc",
  "@type": "ttt:TicTacToeResult",
  "@context": {
    "@vocab": "https://www.w3.org/2019/wot/hypermedia#",
    "ttt": "http://localhost:8083/tic-tac-toe#",
    "htv": "http://www.w3.org/2011/http#",
    "wot": "https://w3c.github.io/wot-thing-description/#",
    "sch": "https://schema.org/#",
    "links": {
      "@id": "Link"
    },
    "forms": {
      "@id": "Form"
    },
    "href": {
      "@id": "hasTarget"
    },
    "rel": {
      "@id": "hasRelationType",
      "@type": "@vocab"
    }
  },
  "ttt:TicTacToeResult": "http://agentURL.com",
  "links": [
    {
      "href": "http://localhost:8083/Board?id=1df666f8-6e74-4e51-8ad3-7f807bd380cc",
      "htv:methodName": "GET"
    },
    {
      "href": "http://localhost:8083/",
      "htv:methodName": "GET"
    }
  ]
```


#### Board Request:

GET http://localhost:8083/Board?id=1df666f8-6e74-4e51-8ad3-7f807bd380cc
Content-Type application/json

#### Board Response:

```
{
  "@id": "http://localhost:8083/Board?id=1df666f8-6e74-4e51-8ad3-7f807bd380cc",
  "@type": "ttt:Board",
  "@context": {
    "@vocab": "https://www.w3.org/2019/wot/hypermedia#",
    "ttt": "http://localhost:8083/tic-tac-toe#",
    "htv": "http://www.w3.org/2011/http#",
    "wot": "https://w3c.github.io/wot-thing-description/#",
    "sch": "https://schema.org/#",
    "links": {
      "@id": "Link"
    },
    "forms": {
      "@id": "Form"
    },
    "href": {
      "@id": "hasTarget"
    },
    "rel": {
      "@id": "hasRelationType",
      "@type": "@vocab"
    }
  },
  "ttt:hasSquare": [
    {
      "http://localhost:8083/Square11?id=1df666f8-6e74-4e51-8ad3-7f807bd380cc": {
        "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": "http://localhost:8083/tic-tac-toe#Square11",
        "http://localhost:8083/tic-tac-toe#moveTakenBy": "http://localhost:8083/apibot"
      }
    },
    {
      "http://localhost:8083/Square12?id=1df666f8-6e74-4e51-8ad3-7f807bd380cc": {
        "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": "http://localhost:8083/tic-tac-toe#Square12",
        "http://localhost:8083/tic-tac-toe#moveTakenBy": "http://agentURL.com"
      }
    },
    {
      "http://localhost:8083/Square13?id=1df666f8-6e74-4e51-8ad3-7f807bd380cc": {
        "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": "http://localhost:8083/tic-tac-toe#Square13",
        "http://localhost:8083/tic-tac-toe#moveTakenBy": "http://localhost:8083/apibot"
      }
    },
    {
      "http://localhost:8083/Square22?id=1df666f8-6e74-4e51-8ad3-7f807bd380cc": {
        "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": "http://localhost:8083/tic-tac-toe#Square22",
        "http://localhost:8083/tic-tac-toe#moveTakenBy": "http://agentURL.com"
      }
    },
    {
      "http://localhost:8083/Square32?id=1df666f8-6e74-4e51-8ad3-7f807bd380cc": {
        "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": "http://localhost:8083/tic-tac-toe#Square32",
        "http://localhost:8083/tic-tac-toe#moveTakenBy": "http://agentURL.com"
      }
    }
  ],
  "links": [
    {
      "href": "http://localhost:8083/",
      "htv:methodName": "GET"
    },
    {
      "href": "http://localhost:8083/result?id=1df666f8-6e74-4e51-8ad3-7f807bd380cc",
      "htv:methodName": "GET"
    }
  ],
  "forms": [
    {
      "href": "http://localhost:8083/register",
      "contentType": "application/json",
      "htv:methodName": "POST",
      "wot:op": "readproperty",
      "properties": [
        {
          "name": "ttt:Agent",
          "readOnly": false,
          "required": true
        }
      ]
    }
  ]
}
```


## Requirements


## Running the server


## Running testss