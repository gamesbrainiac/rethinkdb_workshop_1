var r = require('rethinkdbdash')();
var express = require('express');
var cron = require('cron');
var app = express();
var db = r.db('workshop_1');

function makeId() {
  var text = "";
  var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

  for( var i=0; i < 5; i++ )
      text += possible.charAt(Math.floor(Math.random() * possible.length));

  return text;
}

function generateMessage() {
  var message = makeId();
  db.table('messages').insert({
    message: message,
    date: new Date()
  })
    .run()
    .then(function(result) {
      console.log('Message created - ' + message);
    })
    .error(function(err) {
      console.log(err);
    })
}

var cronJob = cron.job('*/5 * * * * *', function() {
  generateMessage();
})

cronJob.start();

app.get('*', function(req,res,next) {
  res.send('This server generates ids');
})

app.listen(3000);
