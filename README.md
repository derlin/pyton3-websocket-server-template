
pyton3-websocket-server-template
================================

A sample cherrypy server with ws4py websockets.

Purpose
-------
This project is just a skeleton to build a simple client-server application using websockets.

It is useful for very small projects which only requires a couple of pages and a fast deployement.


How to use
----------

### First run

1. Run `setup.py install`
2. Configure the server with your ip address and port (localhost:42000 by default)
3. Run `python3 server.py`
4. Open your webrowser (and its console <F12>) to check that everything works : `localhost:42000/index`

### Editing
Modify the server parameters at the end of `server.py`, as well as the @exposed methods to suit your needs.

Write (or modify) a wscontroller, which handles incoming messages from the client sockets. The names of the methods should match the "type" of the incoming messages.

Write (or modify) the javascript file, which handles the client socket.



How it works
------------

### Messages format
All the messages exchanged are json-encoded and have the following structure:

```python
{   
    type: "a_message_type",
    data: <whatever you want>
}
```

### Server-side
An instance of the `GenericWebSocket` class will be created for each new connection. In the ws method of the server, you need to call the `set_controller`method to define the object which will handle incoming messages:

```python
class SimpleServer( object ):
    controller = WsController()
    
    @cherrypy.expose
    def ws(self):
        """
        Client socket should connect to ws://<host>:<port>/ws.
        """
        # you can access the class instance through the following:
        handler = cherrypy.request.ws_handler
        handler.set_controller( self.controller )
        # register the socket to the controller (for broadcasts)
        self.controller.register_client_socket( self )
        log.info( self, 'client socket registered' )
        # don't forget to unregister the socket on close
        handler.set_close_callback( lambda: self.controller.unregister_client_socket( handler ) )
```

Upon reception of a message, the socket will extract the message type and call the corresponding method of the controller (the names should match exactly), passing it the data and a reference on the socket. 
If none is defined, the message will be ignored. A controller method has the following signature:

```python
def a_message_type(self, socket, data):
    # do something
    pass
```

### Client-side

In the javascript, you should first create a `SimpleSocketHandler`:
```javascript
/** the server address, in the form ws//<host>:<port>/<cherrypy exposed method> */
var SERVER_ADDR = 'ws://localhost:42000/ws';

// create the socket and connect to the server
socket = new SimpleSocketHandler(SERVER_ADDR);
```

You can then use its `bind(message_type, function)` method to associate a callback to an incoming message:

```javascript
// register an event on socket opened
socket.bind(MessageTypes.WS_OPEN, function () {
    console.log("opened");
    connected = true;
});
```

To send messages, call `socket.send(message_type, data)`.
