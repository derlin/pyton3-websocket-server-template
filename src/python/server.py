#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Lucy Linder'

import cherrypy
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from wsocket.sock import GenericWebSocket
from wsocket.wscontroller import WsController
from utils import log

WebSocketPlugin( cherrypy.engine ).subscribe( )
cherrypy.tools.websocket = WebSocketTool( )

import os.path

current_dir = os.path.abspath( os.path.join( os.path.dirname( __file__ ), ".." ) )
print( current_dir )


class SimpleServer( object ):
    controller = WsController( )

    @cherrypy.expose
    def default(self, *args, **kwargs):
        """
        Make index the default page
        """
        self.index( )

    @cherrypy.expose
    def index(self):
        """
        Simply return the html/example.html page
        """
        output = open( os.path.join( current_dir, 'html/example.html' ) ).read( )
        return output


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


cherrypy.quickstart(
    SimpleServer( ),
    config = {
        'global': {
            'server.socket_host': "localhost",
            'server.socket_port': 42000,
            'tools.sessions.on': True,
            'tools.staticfile.root': current_dir,
            'tools.sessions.locking': 'explicit',
            'checker.on': False
        },

        ## websocket handling
        '/ws': {
            'tools.websocket.on': True,
            'tools.websocket.handler_cls': GenericWebSocket
        },

        ## js
        '/example.js': {
            'tools.staticfile.on': True,
            'tools.staticfile.filename': "js/example.js"
        },

        '/socket.js': {
            'tools.staticfile.on': True,
            'tools.staticfile.filename': "js/simplesocket.js"
        },

        '/message.js': {
            'tools.staticfile.on': True,
            'tools.staticfile.filename': "js/messages.js"
        },

        ## css
        '/example.css': {
            'tools.staticfile.on': True,
            'tools.staticfile.filename': "other/example.css"
        }
    } )