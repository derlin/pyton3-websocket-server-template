/**
 *
 * @author Lucy Linder
 * @date 10.07.2014
 */

/** the server address, in the form ws//<host>:<port>/<cherrypy exposed method> */
var SERVER_ADDR = 'ws://localhost:42000/ws'; // TODO change it
/**the connection status */
var connected = false;
/** the socket object */
var socket = null;


$(function () {
    // create the socket and connect to the server
    socket = new SimpleSocketHandler(SERVER_ADDR);

    // register an event on socket opened
    socket.bind(MessageTypes.WS_OPEN, function () {
        console.log("opened");
        connected = true;
    });

    // register an event on socket closed
    socket.bind(MessageTypes.WS_CLOSE, function () {
        connected = false;
        // show an alert message
        $('#connection_lost_alert').removeClass('hidden');
        // disable all the buttons which could trigger a "send"
        $('.link').off('click').removeClass('link');

    });

    // close the socket properly on unload
    $(window).unload(function () {
        socket.onclose = function () {  // disable onclose handler first
        };
        socket.close();
    });

    socket.bind(MessageTypes.IN_HELLO_WOLRD, function (data) {
        // here, we receive a simple string: just display it
        console.log("received hello");
        $('#hello_answer').text(data);
    });

    $('#hello_btn').click(function () {
        // send a hello message to the server, no data
        console.log("sending hello");
        socket.send(MessageTypes.OUT_HELLO_WOLRD, "");
    });

    //-------------------------------------------------------------

    socket.bind(MessageTypes.IN_GDC, function (data) {
        // here, we receive a simple array with one element
        console.log("received gdc");
        console.log(data);
        $('#gdc_answer').text(JSON.parse(data));
    });

    $('#gdc_button').click(function () {
        // send a hello message to the server, no data
        var nbrs = [
            parseInt($('*[name="nbr1_input"]').val()),
            parseInt($('*[name="nbr2_input"]').val())
        ];
        console.log("sending gdc");
        console.log(nbrs);
        socket.send(MessageTypes.OUT_GDC,
            JSON.stringify(nbrs)
        );
    });

});

