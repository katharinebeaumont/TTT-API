# TIC TAC TOE API

## Game play

The index page. This returns the context, and links including the form to register.

#### Request:

GET http://localhost:8083/

#### Response:

```
{
  "@context": {
    "@vocab": "https://www.w3.org/2019/wot/hypermedia#",
    "forms": {
      "@id": "Form"
    },
    "href": {
      "@id": "hasTarget"
    },
    "htv": "http://www.w3.org/2011/http#",
    "links": {
      "@id": "Link"
    },
    "rel": {
      "@id": "hasRelationType",
      "@type": "@vocab"
    },
    "sch": "https://schema.org/#",
    "ttt": "http://localhost:8083/tic-tac-toe#",
    "wot": "https://w3c.github.io/wot-thing-description/#"
  },
  "@id": "tic-tac-toe",
  "@type": "http://localhost:8083",
  "forms": [
    {
      "contentType": "application/json",
      "href": "http://localhost:8083/register",
      "htv:methodName": "POST",
      "properties": [
        {
          "name": "ttt:Agent",
          "readOnly": false,
          "required": true
        }
      ],
      "wot:op": "readproperty"
    }
  ],
  "links": [
    {
      "href": "http://localhost:8083/tic-tac-toe",
      "htv:methodName": "GET"
    },
    {
      "href": "http://localhost:8083/apibot",
      "htv:methodName": "GET"
    }
  ]
}
```

Next, registering. An agent POSTS to the /register endpoint, with the parameter in the body which is the agent's URI.
The response includes the possible moves on the tic tac toe board (presented as POST links) and a link to the board, along with links back to
the index.

#### Request:

POST http://localhost:8083/register
```
Body: agent=http://agentURL.com
```

#### Response:

```
{
  "@context": {
    "@vocab": "https://www.w3.org/2019/wot/hypermedia#",
    "forms": {
      "@id": "Form"
    },
    "href": {
      "@id": "hasTarget"
    },
    "htv": "http://www.w3.org/2011/http#",
    "links": {
      "@id": "Link"
    },
    "rel": {
      "@id": "hasRelationType",
      "@type": "@vocab"
    },
    "sch": "https://schema.org/#",
    "ttt": "http://localhost:8083/tic-tac-toe#",
    "wot": "https://w3c.github.io/wot-thing-description/#"
  },
  "@id": "http://localhost:8083/register",
  "@type": "",
  "links": [
    {
      "href": "http://localhost:8083/",
      "htv:methodName": "GET"
    },
    {
      "href": "http://localhost:8083/board?id=1c1b1628-d9d1-42c9-889d-265f528c738e",
      "htv:methodName": "GET"
    },
    {
      "href": "http://localhost:8083/Square11?id=1c1b1628-d9d1-42c9-889d-265f528c738e",
      "htv:methodName": "POST"
    },
    {
      "href": "http://localhost:8083/Square12?id=1c1b1628-d9d1-42c9-889d-265f528c738e",
      "htv:methodName": "POST"
    },
    {
      "href": "http://localhost:8083/Square13?id=1c1b1628-d9d1-42c9-889d-265f528c738e",
      "htv:methodName": "POST"
    },
    {
      "href": "http://localhost:8083/Square21?id=1c1b1628-d9d1-42c9-889d-265f528c738e",
      "htv:methodName": "POST"
    },
    {
      "href": "http://localhost:8083/Square22?id=1c1b1628-d9d1-42c9-889d-265f528c738e",
      "htv:methodName": "POST"
    },
    {
      "href": "http://localhost:8083/Square23?id=1c1b1628-d9d1-42c9-889d-265f528c738e",
      "htv:methodName": "POST"
    },
    {
      "href": "http://localhost:8083/Square31?id=1c1b1628-d9d1-42c9-889d-265f528c738e",
      "htv:methodName": "POST"
    },
    {
      "href": "http://localhost:8083/Square32?id=1c1b1628-d9d1-42c9-889d-265f528c738e",
      "htv:methodName": "POST"
    },
    {
      "href": "http://localhost:8083/Square33?id=1c1b1628-d9d1-42c9-889d-265f528c738e",
      "htv:methodName": "POST"
    }
  ]
}
```

Posting to a square: this gives the options to navigate back to the index, or to the board.

#### Request:

POST http://localhost:8083/Square31?id=e686d513-e2ce-409a-802a-d854b8204581

#### Response:

```
{
  "@context": {
    "@vocab": "https://www.w3.org/2019/wot/hypermedia#",
    "forms": {
      "@id": "Form"
    },
    "href": {
      "@id": "hasTarget"
    },
    "htv": "http://www.w3.org/2011/http#",
    "links": {
      "@id": "Link"
    },
    "rel": {
      "@id": "hasRelationType",
      "@type": "@vocab"
    },
    "sch": "https://schema.org/#",
    "ttt": "http://localhost:8083/tic-tac-toe#",
    "wot": "https://w3c.github.io/wot-thing-description/#"
  },
  "@id": "http://localhost:8083/Square31",
  "@type": "ttt:Square31",
  "links": [
    {
      "href": "http://localhost:8083/",
      "htv:methodName": "GET"
    },
    {
      "href": "http://localhost:8083/board?id=1c1b1628-d9d1-42c9-889d-265f528c738e",
      "htv:methodName": "GET"
    }
  ]
}
```

Going back to the board: this reveals the possible moves left to make, and reveals any moves the APIBOT has taken.

#### Request:

GET http://localhost:8083/board?id=1c1b1628-d9d1-42c9-889d-265f528c738e

#### Response:

```
{
  "@context": {
    "@vocab": "https://www.w3.org/2019/wot/hypermedia#",
    "forms": {
      "@id": "Form"
    },
    "href": {
      "@id": "hasTarget"
    },
    "htv": "http://www.w3.org/2011/http#",
    "links": {
      "@id": "Link"
    },
    "rel": {
      "@id": "hasRelationType",
      "@type": "@vocab"
    },
    "sch": "https://schema.org/#",
    "ttt": "http://localhost:8083/tic-tac-toe#",
    "wot": "https://w3c.github.io/wot-thing-description/#"
  },
  "@id": "http://localhost:8083/board",
  "@type": "ttt:Board",
  ttt:hasSquare: {
    
  }
  "http://localhost:8083/tic-tac-toe#Square11": "http://localhost:8083/apibot",
  "http://localhost:8083/tic-tac-toe#Square12": "",
  "http://localhost:8083/tic-tac-toe#Square13": "",
  "http://localhost:8083/tic-tac-toe#Square21": "",
  "http://localhost:8083/tic-tac-toe#Square22": "",
  "http://localhost:8083/tic-tac-toe#Square23": "",
  "http://localhost:8083/tic-tac-toe#Square31": "http://agentURL.com",
  "http://localhost:8083/tic-tac-toe#Square32": "",
  "http://localhost:8083/tic-tac-toe#Square33": "",
  "links": [
    {
      "href": "http://localhost:8083/",
      "htv:methodName": "GET"
    },
    {
      "href": "http://localhost:8083/board?id=1c1b1628-d9d1-42c9-889d-265f528c738e",
      "htv:methodName": "GET"
    },
    {
      "href": "http://localhost:8083/Square12?id=1c1b1628-d9d1-42c9-889d-265f528c738e",
      "htv:methodName": "POST"
    },
    {
      "href": "http://localhost:8083/Square13?id=1c1b1628-d9d1-42c9-889d-265f528c738e",
      "htv:methodName": "POST"
    },
    {
      "href": "http://localhost:8083/Square21?id=1c1b1628-d9d1-42c9-889d-265f528c738e",
      "htv:methodName": "POST"
    },
    {
      "href": "http://localhost:8083/Square22?id=1c1b1628-d9d1-42c9-889d-265f528c738e",
      "htv:methodName": "POST"
    },
    {
      "href": "http://localhost:8083/Square23?id=1c1b1628-d9d1-42c9-889d-265f528c738e",
      "htv:methodName": "POST"
    },
    {
      "href": "http://localhost:8083/Square32?id=1c1b1628-d9d1-42c9-889d-265f528c738e",
      "htv:methodName": "POST"
    },
    {
      "href": "http://localhost:8083/Square33?id=1c1b1628-d9d1-42c9-889d-265f528c738e",
      "htv:methodName": "POST"
    }
  ]
}
```

On the game finishing, the agent can see links to the board, the index, and now to the result page.

### ...Winning Requests

POST http://localhost:8083/Square32?id=1c1b1628-d9d1-42c9-889d-265f528c738e
POST http://localhost:8083/Square33?id=1c1b1628-d9d1-42c9-889d-265f528c738e

### Response

```
{
  "@context": {
    "@vocab": "https://www.w3.org/2019/wot/hypermedia#",
    "forms": {
      "@id": "Form"
    },
    "href": {
      "@id": "hasTarget"
    },
    "htv": "http://www.w3.org/2011/http#",
    "links": {
      "@id": "Link"
    },
    "rel": {
      "@id": "hasRelationType",
      "@type": "@vocab"
    },
    "sch": "https://schema.org/#",
    "ttt": "http://localhost:8083/tic-tac-toe#",
    "wot": "https://w3c.github.io/wot-thing-description/#"
  },
  "@id": "http://localhost:8083/Square33",
  "@type": "ttt:Square33",
  "links": [
    {
      "href": "http://localhost:8083/",
      "htv:methodName": "GET"
    },
    {
      "href": "http://localhost:8083/board?id=1c1b1628-d9d1-42c9-889d-265f528c738e",
      "htv:methodName": "GET"
    },
    {
      "href": "http://localhost:8083/result?id=1c1b1628-d9d1-42c9-889d-265f528c738e",
      "htv:methodName": "GET"
    }
  ]
}
```

### Request

GET http://localhost:8083/result?id=1c1b1628-d9d1-42c9-889d-265f528c738e

### Response

```
{
  "@context": {
    "@vocab": "https://www.w3.org/2019/wot/hypermedia#",
    "forms": {
      "@id": "Form"
    },
    "href": {
      "@id": "hasTarget"
    },
    "htv": "http://www.w3.org/2011/http#",
    "links": {
      "@id": "Link"
    },
    "rel": {
      "@id": "hasRelationType",
      "@type": "@vocab"
    },
    "sch": "https://schema.org/#",
    "ttt": "http://localhost:8083/tic-tac-toe#",
    "wot": "https://w3c.github.io/wot-thing-description/#"
  },
  "@id": "http://localhost:8083/result",
  "@type": "ttt:TicTacToeResult",
  "links": [
    {
      "href": "http://localhost:8083/board?id=1c1b1628-d9d1-42c9-889d-265f528c738e",
      "htv:methodName": "GET"
    },
    {
      "href": "http://localhost:8083/",
      "htv:methodName": "GET"
    }
  ],
  "ttt:TicTacToeResult": "http://agentURL.com"
}
```
