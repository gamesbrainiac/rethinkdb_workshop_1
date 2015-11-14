import rethinkdb as r
import tornado.ioloop
import tornado.web

r.set_loop_type("tornado")

@gen.coroutine
def messages
    conn = yield r.connect(host="localhost", port=28015)
    feed = yield r.db('workshop_1').table('messages').changes().run(conn)
    while (yield feed.fetch_next())
        change = yield feed.next()
        print (change)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("./public/index.html")

if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/)
        (r'/(.*)', tornado.web.StaticFileHandler, {'path': './public/'}),
    ])

print "Server running on Port 3002"
application.listen(3002)
tornado.ioloop.IOLoop.instance().start()
