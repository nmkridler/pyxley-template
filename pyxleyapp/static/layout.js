
    var Component = require("custom").RunLayout;
    var filter_style = "'btn-group'";
var dynamic = true;
var charts = [{"type": "NewChart", "options": {"chartid": "new_chart", "url": "/new_chart/", "colors": ["#847c77", "#ff5c61"]}}];
var filters = [{"type": "SelectButton", "options": {"default": "Heart Rate", "items": ["Heart Rate", "Pace", "Distance"], "alias": "Data", "label": "Data"}}, {"type": "DownloadButton", "options": {"url": "/download/", "label": "Download"}}];
    React.render(
        React.createElement(Component, {
        filter_style: filter_style, 
dynamic: dynamic, 
charts: charts, 
filters: filters}),
        document.getElementById("component_id")
    );
    