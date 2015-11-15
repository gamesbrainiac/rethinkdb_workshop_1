require 'sinatra'
require 'sinatra-websocket'
require 'rethinkdb'
include RethinkDB::Shortcuts

rdb_config ||= {
  :host => ENV['RDB_HOST'] || 'localhost',
  :port => ENV['RDB_PORT'] || 28015,
  :db   => ENV['RDB_DB']   || 'workshop_1'
}

connection = r.connect(:host => rdb_config[:host],
  :port => rdb_config[:port])

get '/' do
  File.read('./public/index.html')
end

get '/messages' do
  r.db("workshop_1").table("messages").coerce_to("array").run(connection).to_json
end
