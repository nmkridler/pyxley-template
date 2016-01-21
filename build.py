from pyxleyapp.lib.factory import create_app, get_static_folder
from pyxleyapp.views import config
ins_, static_ = get_static_folder()
config.transform_react(static_dir=static_+"/")

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
MainView(cache, save=True)
