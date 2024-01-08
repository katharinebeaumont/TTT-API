# TIC TAC TOE API

This API allows users to play a game of Tic-Tac-Toe against a bot, using RESTful API calls to various endpoints, which return JSON with hypermedia controls and the use of Hypermedia As The Engine Of Application State (HATEOAS). 

Important note: 
The form properties fields are entirely made up at the moment and need changing to something that fits an existing ontology (e.g. look to change this to be compatible with WOT descriptions)

## Requirements

This has been developed using the [anaconda3](https://anaconda.org/) environment / suite of libraries and dependencies and [pip](https://pypi.org/project/pip/) for dependencies.

[RDFLib](https://rdflib.readthedocs.io/en/stable/index.html) is used for the ontology and graph. [Flask](https://flask.palletsprojects.com/en/3.0.x/) is used for the server. [pyLODE](https://github.com/RDFLib/pyLODE) is used to load in the Tic-Tac-Toe ontology and host it as HTML.

Requirements are in requirements.txt
Run ```pip install -r requirements.txt```

## Test and run

The script `testAndRun.sh` runs unit and server tests, then runs the application at http://localhost:8083/
To execute, run:

```flask run```

## Running the server

The by default the server runs at http://127.0.0.1:5000/

```flask run```

To specify host and port, e.g.:

```flask run --host=localhost --port=8083```

## Running unit tests

```python -m unittest tests/*.py```

or for more specific tests

```python -m unittest tests/responsewritertests.py```

## Running server tests

```python -m pytest tests/*.py```

## Game Play

The game play is as follows;

- The user registers at the endpoint /register, by POST request which includes the property "ttt:Agent" and the Agent URL
- This returns links and forms to play the game, with an assigned ID
- The server creates an RDF graph in memory using the assigned ID, and intantiates classes of ttt:Board and ttt:SquareXX (XX being the square location from the set {11,12,13,21,22,23,31,32,33}. Diagonals are {11,22,33} and {13,22,31}). The graph is stored against the ID in a dictionary data structure. Moves are added to this graph.
- When the game is over, a link to the result, and form to register again are provided. The graph of the game is stored in the /results folder, with the game ID as the file title and in ttl format.

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
    "sch":"https://schema.org/",
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
  "@type":"ttt:Agent",
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
    "sch":"https://schema.org/",
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
    "sch":"https://schema.org/",
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
    "sch":"https://schema.org/",
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
    "sch":"https://schema.org/",
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
    "sch":"https://schema.org/",
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
    "sch":"https://schema.org/",
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
