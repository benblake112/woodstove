#!/usr/bin/env python
import sys
from woodstove import app, server, log, arguments


class ExampleApp(object):
    wsapp = app.App('/hello')

    @wsapp.get('/')
    def hello(self):
        return "Hello world"

    @wsapp.get('/<name>')
    def hello_name(self, name):
        return "Hello %s!" % name

    @wsapp.args(query=arguments.ArgumentList(
        arguments.String('name', default="world"),
    ))
    @wsapp.get('/query')
    def hello_name_query(self):
        return "Hello %s!" % self.wsapp.request.query['name']

    @wsapp.args(body=arguments.ArgumentList(
        arguments.String('name', default="world"),
    ))
    @wsapp.post('/body')
    def hello_name_body(self):
        return "Hello %s!" % self.wsapp.request.body['name']

def main():
    if len(sys.argv) != 2:
        print >>sys.stderr, "Missing listen port"
        sys.exit(1)

    log.setup()
    log.to_console(log.logging.DEBUG)
    s = server.Server()
    s.mount(ExampleApp())
    s.run(host='0.0.0.0', port=int(sys.argv[1]))


if __name__ == '__main__':
    main()
