import rethinkdb as r
import tornado.ioloop
import tornado.web
import json

conn = r.connect("localhost", 28015).repl()
r.set_loop_type("tornado")

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("./public/index.html")

class MessagesHandler(tornado.web.RequestHandler):
    def get(self):
        cursor = r.db('workshop_1').table('messages')
        array = {}
        count = 0
        for row in cursor.run(conn):
            array[count] = {}
            array[count]['id'] = row['id']
            array[count]['message'] = row['message']
            count = count + 1

        self.write(json.dumps(array))

if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r'/messages', MessagesHandler),
        (r'/(.*)', tornado.web.StaticFileHandler, {'path': './public/'}),
    ])

print "Server running on Port 3002"
application.listen(3002)
tornado.ioloop.IOLoop.instance().start()
tornado.ioloop.IOLoop.current().add_callback(getMessages)
