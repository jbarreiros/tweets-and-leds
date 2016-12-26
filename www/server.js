const compression = require('compression');
const express = require('express');
const path = require('path');
const app = express();

app.use(compression());
app.use(express.static('./build'));

app.get('/', (req, res) => res.sendFile(path.join(__dirname, './build', 'index.html')));

app.listen(9000, () => console.log('App started!'));

// nodejs websocket
/*const WebsocketServer = require('ws').Server;
const wss = new WebsocketServer({port:9001, path: '/skynet'});
wss.on('connection', (ws) => {
    ws.on('message', (msg) => {
        console.log('received: %s', msg);
    });

    let c = 0;
    setInterval(() => {
        console.log('ping');
        c++;
        ws.send(c.toString());
    }, 10000);
});*/

