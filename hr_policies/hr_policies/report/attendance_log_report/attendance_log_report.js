// Copyright (c) 2016, Hardik gadesha and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Attendance Log Report"] = {
	"filters": [
		{
			"fieldname": "employee",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options": "Employee"
		},
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"options": frappe.datetime.month_start()
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"options": frappe.datetime.month_end()
		},
		{
			"fieldname": "exclude_left",
			"label": __("Exclude Left"),
			"fieldtype": "Check",
			"default": 1
		}
	]
};
