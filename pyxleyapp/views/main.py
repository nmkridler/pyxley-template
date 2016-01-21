from flask import render_template, make_response
from flask import request, jsonify
from flask import Blueprint
from . import config

from ..lib.factory import get_static_folder
from ..models.main import MainModel

from collections import OrderedDict
import pandas as pd
from pyxley.filters import SelectButton, DownloadButton
from pyxley import UILayout
from ..widgets.helper import NewChart

from datetime import date
import time
import json
import logging

class MainView(MainModel):
    _FILES = ["data"]
    def __init__(self, cache, save=False):
        super(MainView, self).__init__(cache)

        self.mod = Blueprint("main", __name__)
        self.mod.add_url_rule("/", view_func=self.index)

        self.ins_, self.static_ = get_static_folder()
        self.build_ui(save)

    def index(self):

        shims = {
            "custom": ["twoAxisLinePlot", "pyxley"],
            "main": ["custom"]
        }

        _module_list = [
            ["navbar", "main"]
        ]
        _modules = OrderedDict([(",".join(m), m) for m in _module_list])
        _baseUrl = "./static/js"
        _paths = {
            "pyxley": "../bower_components/pyxley/build/pyxley",
            "main": "../layout"
        }
        return render_template('index.html',
            title="Main",
            base_scripts=config.JS,
            css=config.CSS,
            baseUrl=_baseUrl,
            modules=_modules,
            paths=json.dumps(_paths),
            shims=json.dumps(shims))

    def build_ui(self, save):

        # Make a UI
        self.ui = UILayout(
            "RunLayout",
            "custom",
            "component_id")

        choices = ["Heart Rate", "Pace", "Distance"]
        btn = SelectButton("Data", choices, "Data", "Heart Rate")
        self.ui.add_filter(btn)

        """
            Add a download button,
            I typically use this to trigger a download, but
            it could be used to trigger another action
        """
        dlbtn = DownloadButton("Download", "/download/", self.download)
        self.ui.add_filter(dlbtn)

        self.add_chart()
        if save:
            self.ui.render_layout(self.mod, self.static_ + "/layout.js")
        else:
            self.ui.assign_routes(self.mod)

    def download(self):
        print "Change this to do something else"
        print "For now it will reload"
        self.cache.load()
        return jsonify({"data": "Success!"})

    def chart_data(self):
        args = {}
        for c in self.init_params:
            if request.args.get(c):
                args[c] = request.args[c]
            else:
                args[c] = self.init_params[c]
        return jsonify(NewChart.to_json(
                NewChart.apply_filters(self.data, args),
                "Seconds",
                "value",
                "Altitude"
            ))

    def add_chart(self):
        colors = ["#847c77", "#ff5c61"]
        self.init_params = {
            "Data": "Heart Rate"
        }
        nc = NewChart("Seconds", "value", "Altitude",
            self.data,
            init_params=self.init_params, colors=colors,
            route_func=self.chart_data)
        self.ui.add_chart(nc)
