import os

base_dir = os.path.dirname(__file__)

setting = {
            'template_path': os.path.join(base_dir, "template"),
            'static_path': os.path.join(base_dir, "static"),
            'debug':True,
            "xsrf_cookies": False,
}

username = 'neo4j'
password = '123456'
host = 'localhost:7474'
host_link = 'http://localhost:7474/db/data/'