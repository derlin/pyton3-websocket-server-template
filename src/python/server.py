#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Lucy Linder'

import cherrypy
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from wsocket.sock import GenericWebSocket
from wsocket.wscontroller import WsController

WebSocketPlugin( cherrypy.engine ).subscribe( )
cherrypy.tools.websocket = WebSocketTool( )

import os.path

current_dir = os.path.abspath( os.path.join( os.path.dirname( __file__ ), ".." ) )
print(current_dir)


class SimpleServer( object ):
    controller = WsController()

    @cherrypy.expose
    def index(self):
        print(current_dir)
        output = open( os.path.join( current_dir, 'html/example.html' ) ).read( )
        return output


    @cherrypy.expose
    def ws(self):
        # you can access the class instance through the following:
        handler = cherrypy.request.ws_handler
        handler.set_controller( self.controller )
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