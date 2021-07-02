var WebSocket = require("ws");
const Max = require('max-api');

// LOCAL
// wsServer = "ws://localhost:3000";
// HEROKU
wsServer = "wss://lithosys.herokuapp.com/wss";

var ws;
var username = "IAgotchi";
var usercolor = "#CC0000";
var usertype = "machine";

function connect() {
	Max.post("Connecting...");
	ws = new WebSocket(wsServer);
	ws.on('open', function open() {
		Max.post('WebSocket Opened ('+wsServer+')');
	});
	ws.on('error', function open() {
		Max.post('WebSocket Error ('+wsServer+')');
	});
	ws.on('close', function open() {
		Max.post('WebSocket Closed ('+wsServer+')');
		Max.outlet("closed");
	});
	ws.on('message', function received(message) {
		msg = JSON.parse(message);
		if(msg.command == "newmess")
		{
			if(msg.name != username)
			{
				Max.post('New Message received : '+msg.content);
				Max.outlet(msg);
			} else {
				Max.post('Message sent : '+msg.content);
			}
		} else {
			Max.post('Websocket received : '+msg.command);
		}
	});
}

Max.addHandler("setSocketAddress", (msg) => {
	wsServer = msg;
	Max.post('WebSocket to '+wsServer);
});

Max.addHandler("connect", () => {
	connect();
});

Max.addHandler("send", (message) => {
	ws.send(JSON.stringify(
		{
			charset : 'utf8mb4',
			command: "newmess",
			name: username,
			type: usertype,
			date: Date.now(),
			content: message,
			color: usercolor
		}));
});

Max.addHandler("keepAlive", (msg) => {
	//const ws = new WebSocket(wsServer);
	//ws.on('open', function open() {
	//if(ws)
	//	Max.post('WebSocket state : '+ws.readyState);
	if(ws.readyState == 1) {
			ws.send(JSON.stringify(
			{
				charset : 'utf8mb4',
				command: "keepAlive"
			}));
	} else {
		connect();
	}
	//	ws.close();
	//	});
});
