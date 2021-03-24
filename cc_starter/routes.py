def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('users', '/users')
    config.add_route('user', '/users/{id:\d+}')
