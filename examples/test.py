# Copyright (C) 2016 IAC Publishing Labs. All rights reserved.
#
# License: Apache (see LICENSE for details)
import peewee
from playhouse import shortcuts
from woodstove import log, server, plugin, db, app, arguments

def crud_factory(model, path, namespace=None):
    class CRUD(object):
        wsapp = app.App(path, namespace)
        _model = model

        @wsapp.auth(Group('foo'))
        @wsapp.args(query_args=arguments.ArgumentList(
            arguments.String('sort', optional=True),
            arguments.Integer('limit', cast=int, default=25),
            arguments.Integer('offset', cast=int, default=0),
        ))
        @wsapp.get('/')
        def find(self):
            return [shortcuts.model_to_dict(d) for d in self._model.select()]

        @wsapp.get('/<key>')
        def read(self, key):
            return db.get_obj(self._model, key)

        @wsapp.args(body_args=arguments.ArgumentList(
            arguments.peewee_to_spec(model)
        ))
        @wsapp.post('/')
        def create(self):
            ''' '''

    return CRUD()


class TestModel(db.BaseModel):
    name = peewee.CharField(unique=True)

class Foo(db.BaseModel):
    bar = peewee.CharField()

def test():
    database = db.get_db()
    database.create_tables([TestModel, Foo])

    print [f.get_column_type() for f in Foo._meta.sorted_fields]

    TestModel(name='foo').save()
    TestModel(name='bar').save()
    Foo(bar='foo').save()
    Foo(bar='bar').save()
    print shortcuts.model_to_dict(TestModel())
    import sys
    log.setup()
    log.to_console(log.logging.DEBUG)
    plugin.load_plugin('woodstove.plugins.cors')
    plugin.load_plugin('woodstove.plugins.trace')
    plugin.load_plugin('woodstove.plugins.duration')
    plugin.load_plugin('woodstove.plugins.db')
    s = server.Server()
    s.mount(crud_factory(TestModel, '/test'))
    s.mount(crud_factory(Foo, '/foo'))
    s.import_apps()
    s.run(host='0.0.0.0', port=int(sys.argv[1]))


if __name__ == '__main__':
    test()
