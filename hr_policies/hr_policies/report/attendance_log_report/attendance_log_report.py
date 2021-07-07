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
        invoice = frappe.db.sql("""
			select 
				al.employee as 'emp',
				emp.employee_name,
				al.card_no,
				date(al.attendance_time),
				al.shift_start_time,
				al.shift_end_time,
				al.attendance_type,
				time(al.attendance_time)
			from 
				`tabAttendance Log` as al, `tabEmployee` as emp
			where 
				al.employee = emp.name and
				al.docstatus = 0 
				%s 
			order by 
				date(al.attendance_time) desc;
		"""%conditions, filters, as_list=1)
        return invoice

def get_conditions(filters):
	conditions = ""
	if filters.get("employee"): conditions += "and al.employee = %(employee)s"
	if filters.get("from_date"): conditions += " and date(al.attendance_time) >= %(from_date)s"
	if filters.get("to_date"): conditions += " and date(al.attendance_time)  <= %(to_date)s"
	if filters.get("exclude_left"): conditions += " and emp.status  = 'Active' "

	return conditions, filters
