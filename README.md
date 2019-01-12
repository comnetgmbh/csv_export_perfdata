# csv_export_perfdata

Extension for Check_MK to output a single performance data variable per column in CSV export

This extension adds the new column "Service performance data (split into columns for CSV export)" that can be added to any existing service-related view. This column will be split into single columns for each performance data variable when using the CSV export function.

Put this into ~/local/share/check_mk/web/plugins/views

# License
csv_export_perfdata is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License version 2, as published by
the Free Software Foundation.

csv_export_perfdata is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with csv_export_perfdata.  If not, see <https://www.gnu.org/licenses/>.
