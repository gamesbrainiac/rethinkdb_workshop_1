import rethinkdb as r
import tornado.ioloop
import tornado.web

r.set_loop_type("tornado")
conn = yield r.connect(host="localhost", port=28015)
sub = set()


class WSocketHandler(tornado.websocket.WebSocketHandler): #Tornado Websocket Handler
    def check_origin(self, origin):
        return True

    def open(self):
        print "Client connected"
        self.stream.set_nodelay(True)
        sub.add(self)

    def on_close(self):
        print "Client disconnected"

@tornado.gen.coroutine
def getMessages()
    feed = yield r.db('workshop_1').table('messages').changes().run(conn)
    while (yield feed.fetch_next())
        change = yield feed.next()
        sub.write_message(change)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("./public/index.html")

if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r'/ws', WSocketHandler),
        (r'/(.*)', tornado.web.StaticFileHandler, {'path': './public/'}),
    ])

print "Server running on Port 3002"
application.listen(3002)
tornado.ioloop.IOLoop.instance().start()
tornado.ioloop.IOLoop.current().add_callback(getMessages)
