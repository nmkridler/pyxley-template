from pyxleyapp.lib.factory import create_app
from pyxleyapp.lib.scheduler import Scheduler


from flask import jsonify

import argparse
parser = argparse.ArgumentParser(description="Flask Template")
parser.add_argument("--env", help="production or local", default="local")
args = parser.parse_args()

app = create_app()

from pyxleyapp.lib.cache import CacheData
from pyxleyapp.models.config import FILES
cache = CacheData(FILES[args.env], env=args.env)
cache.load()

from pyxleyapp.views.main import MainView
_views = {}
_views["main"] = MainView(cache)

for v in _views.values():
    app.register_blueprint(v.mod)

@app.route('/health_check', methods=["GET"])
def health_check():
    return jsonify({"result": "wubbalubbadubdub"})

import time
def check_status():
    cache.status()
    for v in _views:
        if v == "feedback":
            continue
        _views[v].status()

if __name__ == "__main__":
    if args.env == "prod":
        scheduler = Scheduler(1800, check_status)
        scheduler.start()
        app.run(host='0.0.0.0')
        scheduler.stop()
    else:
        app.run(debug=True, port=5555)
