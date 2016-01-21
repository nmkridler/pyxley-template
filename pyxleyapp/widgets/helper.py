
from pyxley.charts import Chart
from flask import jsonify, request

class NewChart(Chart):
    def __init__(self, x, y1, y2, data_source, init_params={},
        chart_id="new_chart", url="/new_chart/", colors=[],
        route_func=None):

        self.x = x
        self.y1 = y1
        self.y2 = y2
        self.options = {
            "chartid": chart_id,
            "url": url,
            "colors": colors
        }
        if not route_func:
            def get_data():
                args = {}
                for c in init_params:
                    if request.args.get(c):
                        args[c] = request.args[c]
                    else:
                        args[c] = init_params[c]
                return jsonify(self.to_json(
                        self.apply_filters(data_source, args)
                    ))
            route_func = get_data

        super(NewChart, self).__init__("NewChart", self.options, route_func)

    @staticmethod
    def to_json(df, x, y1, y2):
        if df.empty:
            return {
                "data": [],
                "yAxis1": {"mean": 0, "std": 1},
                "yAxis2": {"mean": 0, "std": 1}
            }

        mean_1, std_1 = df[y1].mean(), df[y1].std()
        mean_2, std_2 = df[y2].mean(), df[y2].std()

        records = [
            {"key": y1, "values": [], "yAxis": 1, "type": "line"},
            {"key": y2, "values": [], "yAxis": 2, "type": "line"}
        ]

        for n, r in df.iterrows():
            records[0]["values"].append({"x": r[x], "y": r[y1]})
            records[1]["values"].append({"x": r[x], "y": r[y2]})

        return {
            "data": records,
            "yAxis1": {"mean": mean_1, "std": std_1},
            "yAxis2": {"mean": mean_2, "std": std_2}
            }
