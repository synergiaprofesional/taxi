var express = require('express');
var cors = require('cors');

var app = express();
var server = require('http').Server(app);

var io = require('socket.io')(server);

io.on('connection', function (socket) {
    socket.on('client_connected', (data) => {
        console.log(data);
    });
});

app.use(cors());
app.use(express.json());

function response(path, res, req) {
    io.emit(path, req.body);
    return res.send(true);
}

app.post('/session', (req, res) => {
    return response('session', res, req);
});

app.post('/turn', (req, res) => {
    return response('turn', res, req);
});

app.post('/dispatch', (req, res) => {
    return response('dispatch', res, req);
});

app.post('/payment', (req, res) => {
    return response('payment', res, req);
});

server.listen(3000, function () {
    console.log('App running in port 3000');
});