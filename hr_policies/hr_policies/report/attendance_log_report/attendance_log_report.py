# Copyright (c) 2013, Hardik Gadesha and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import msgprint, _

def execute(filters=None):
        conditions, filters = get_conditions(filters)
        columns = get_column()
        data = get_data(conditions,filters)
        return columns,data

def get_column():
        return [_("Employee") + ":Link/Employee:150",
		_("Employee Name") + ":Data:150",
                _("Card No") + ":Data:100",
		_("Date") + ":Date:100",
		_("Shift Start Time") + ":Time:150",
		_("Shift End Time") + ":Time:150",
                _("Punch") + ":Data:100",
		_("Punch Time") + ":Time:100"]

def get_data(conditions,filters):
        invoice = frappe.db.sql("""select employee as 'emp',(select employee_name from `tabEmployee` where name = emp),card_no,
				date(attendance_time),shift_start_time,shift_end_time,attendance_type,time(attendance_time)
				from `tabAttendance Log` where docstatus = 0 %s order by date(attendance_time) desc;"""%conditions, filters, as_list=1)
        return invoice

def get_conditions(filters):
	conditions = ""
	if filters.get("employee"): conditions += "and employee = %(employee)s"
	if filters.get("from_date"): conditions += " and date(attendance_time) >= %(from_date)s"
	if filters.get("to_date"): conditions += " and date(attendance_time)  <= %(to_date)s"

	return conditions, filters
