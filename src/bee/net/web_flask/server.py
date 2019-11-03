from bee import config
from bee.data.map import Map
from bee.bee import banner

class ServerOptions(Map):

    def __init__(self, port: int=8080, context_path: str="bee", banner: bool=True, debug: bool=True):
        self.port = port
        self.path = context_path
        self.banner = banner
        self.debug = debug




def start_up(app):

    port = config.get("port")
    path = config.get("context-path")
    opts = ServerOptions(port=port, context_path=path)
    if opts.debug:
        print(banner)
    app.run(debug=opts.debug, use_reloader=False, host='0.0.0.0', port=port)

