
from react import jsx
import glob

def transform_react(static_dir="static/"):
    transformer = jsx.JSXTransformer()
    for f in glob.glob(static_dir+"jsx/*.js"):
        transformer.transform(f,
            js_path=static_dir+"js/"+f.split('/')[-1])

JS = [
    "./bower_components/jquery/dist/jquery.min.js",
    "./bower_components/d3/d3.min.js",
    "./bower_components/nvd3/build/nv.d3.js",
    "./bower_components/react/react.js",
    "./bower_components/react-bootstrap/react-bootstrap.min.js",
    "./bower_components/pyxley/build/pyxley.js",
    "./chartfunc.js"
]

CSS = [
    "./bower_components/bootstrap/dist/css/bootstrap.min.css",
    "./bower_components/nvd3/build/nv.d3.min.css",
    "./css/main.css"
]
