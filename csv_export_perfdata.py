#!/usr/bin/python
# Copyright (C) 2018, 2019 comNET GmbH
#
# This file is part of csv_export_perfdata.
#
# csv_export_perfdata is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2, as published by
# the Free Software Foundation.
#
# csv_export_perfdata is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with csv_export_perfdata.  If not, see <https://www.gnu.org/licenses/>.

# -*- encoding: utf-8; py-indent-offset: 4 -*-

# 2019-01-11, comNET GmbH, Fabian Binder
# Add new painter for performance data to be splitted into single columns for csv export
# 2019-01-21, comNET GmbH, Fabian Binder
# Added function to summarize fs checks' perfdata names

import metrics

def paint_perfdata_for_csv_export(row):
# ToDo: This works but you need to define fs_ checks manually...
    fs_checks = ["check_mk-netapp_api_aggr", "check_mk-df", "check_mk-netapp_api_qtree_quota", "check_mk-netapp_api_volumes"]
    perfdata_txt = row["service_perf_data"]
    perfdata_txt = perfdata_txt.replace(".", ",")
    if row["service_check_command"] in fs_checks:
        if len(perfdata_txt) > 0:
            perfdata_tmp = perfdata_txt.split("=")
            perfdata_tmp[0] = "fs_used"
            perfdata_txt = "=".join(perfdata_tmp)
            # replace normal perfdata names with human readable names
            for perfdata_split in perfdata_tmp:
                for perfdata_item in perfdata_split.split(" "):
                    perfdata_olditem = perfdata_item
                    perfdata_dict = metrics.check_metrics[row["service_check_command"]].get(perfdata_item, {})
                    perfdata_item = perfdata_dict.get("name", perfdata_item)
                    if perfdata_item in metrics.metric_info:
                        perfdata_txt = perfdata_txt.replace(perfdata_olditem, metrics.metric_info[perfdata_item]["title"].replace(" ", "_"))
    if html.is_api_call():
        return paint_stalified(row, perfdata_txt)
    return "", ""

multisite_painters["svc_perf_data_csv"] = {
    "title" : _("Service performance data (split into columns for CSV export)"),
    "short" : _(""),
    "columns" : ["service_perf_data"],
    "paint" : lambda row: paint_perfdata_for_csv_export(row)
}

def render_csv(rows, view, group_cells, cells, num_columns, show_checkboxes, export = False):
    if export:
        output_csv_headers(view)

    def format_for_csv(raw_data):
        # raw_data can also be int, float
        content = "%s" % raw_data
        stripped = html.strip_tags(content).replace('\n', '').replace('"', '""')
        return stripped.encode("utf-8")

    csv_separator = html.var("csv_separator", ";")
    first = True
    perfdata_cell_index = None
    for cell_count, cell in enumerate(group_cells + cells):
        if first:
            first = False
        else:
            html.write(csv_separator)
        content = cell.export_title()
        if format_for_csv(content) != "svc_perf_data_csv":
            html.write('"%s"' % format_for_csv(content))
        else:
            # We need to get all perfdata variable names from rows
            all_perfdata_names = set()
            perfdata_cell_index = cell_count
            for row in rows:
                for new_cell_count, cell in enumerate(group_cells + cells):
                    if new_cell_count == cell_count:
                        # We are now in a cell containing perfdata variables
                        joined_row = join_row(row, cell)
                        tdclass, content = cell.render_content(joined_row)
                        perfdata_names = [i.split("=")[0] for i in content.split()]
                        all_perfdata_names.update(perfdata_names)
            for perfdata_name in all_perfdata_names:
                html.write('"%s"' % format_for_csv(perfdata_name))
                html.write(csv_separator)

    for row in rows:
        html.write_text("\n")
        first = True
        for cell_count, cell in enumerate(group_cells + cells):
            if first:
                first = False
            else:
                html.write(csv_separator)
            joined_row = join_row(row, cell)
            tdclass, content = cell.render_content(joined_row)
            if perfdata_cell_index:
                if cell_count == perfdata_cell_index:
                    # Now write performance data based on column name
                    perfdata_names = [i.split("=")[0] for i in content.split()]
                    perfdata_values = [(i.split("=")[1]).split(";")[0] for i in content.split()]
                    perfdata_dict = dict(zip(perfdata_names, perfdata_values))
                    for this_perfdata_name in all_perfdata_names:
                        if this_perfdata_name in perfdata_dict:
                            html.write('"%s"' % format_for_csv(perfdata_dict[this_perfdata_name]))
                            html.write(csv_separator)
                        else:
                            html.write(csv_separator)
                else:
                    html.write('"%s"' % format_for_csv(content))
            else:
                html.write('"%s"' % format_for_csv(content))

multisite_layouts["csv_export"] = {
    "title"  : _("CSV data export"),
    "render" : lambda a,b,c,d,e,f: render_csv(a,b,c,d,e,f,True),
    "group"  : False,
    "hide"   : True,
}

multisite_layouts["csv"] = {
    "title"  : _("CSV data output"),
    "render" : lambda a,b,c,d,e,f: render_csv(a,b,c,d,e,f,False),
    "group"  : False,
    "hide"   : True,
}
