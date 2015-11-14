var r = require('rethinkdbdash')();
var db = r.db('workshop_1');
var express = require('express');
var app = express();
var server = require('http').createServer(app);
var io = require('socket.io')(server);

io.on('connection', function(){
  console.log('client connected');
});

db.table('messages')
  .changes()
  .run()
  .then(function(cursor) {
    cursor.each(function(err, result) {
      if (err) console.log(err)
      io.emit('new_message', result);
    });
  });

app.get('/messages', function(req,res,next) {
  db.table('messages')
    .orderBy({index: r.desc('date')})
    .run()
    .then(function(result) {
      res.send(result);
    })
    .error(function(err) {
      res.status(400).send(err);
    })
})

app.use(express.static('./public/'));

console.log('Running on Port 3001')

server.listen(3001);
