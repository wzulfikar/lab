import postgresql

def open(conf: dict = None):
    if conf is None:
        print('- using default postgres connection')
        return postgresql.open('pq://user:pass@localhost:5434/db')

    db_path = '{}:{}/{}'.format(conf['host'], conf['port'], conf['db'])
    print('- using postgres connection from config:', db_path)
    return postgresql.open('pq://{}:{}@{}'.format(conf['user'],
                                                  conf['pass'],
                                                  db_path))
