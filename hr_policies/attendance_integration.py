from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import formatdate, get_time, time_diff,getdate, get_datetime,get_first_day,get_last_day, nowdate, flt, cint, cstr, add_days, today,month_diff,date_diff,add_months
from datetime import datetime
from erpnext.hr.doctype.salary_structure.salary_structure import make_salary_slip
from frappe.model.mapper import get_mapped_doc
from erpnext.hr.doctype.employee.employee import get_holiday_list_for_employee
import json
from ast import literal_eval
import itertools

@frappe.whitelist()
def update_attendance_log(self,method):
	employee = get_employee_from_card(self.card_no)
	if employee:
		shift = frappe.db.get_value("Employee",employee,"default_shift")
		frappe.errprint(shift)
		if shift:
			self.shift = shift
			self.shift_start_time = frappe.db.get_value("Shift Type",shift,"start_time")
			self.shift_end_time = frappe.db.get_value("Shift Type",shift,"end_time")
		new_log_type = check_last_log(employee,self.attendance_time)
		self.employee = employee
		self.attendance_type = new_log_type

def check_last_log(employee,date):
	log_data = frappe.db.sql("""select attendance_type from `tabAttendance Log` where employee=%s and DATE(attendance_time)=%s order by creation desc""",(employee,getdate(date)),as_dict=1)
	if log_data:
		if log_data[0].attendance_type == "IN":
			return 'OUT'
		else:
			return 'IN'
	else:
		return 'IN'

def get_employee_from_card(card):
	employee = frappe.get_all("Employee",filters={"card_no":card},fields=["name"])
	if employee:
		return employee[0].name
	else:
		return False

@frappe.whitelist()
def process_attendance():
	shift_data = frappe.get_all("Shift Type",filters={},fields=["name","start_time","end_time"])
	for shift in shift_data:
		filters = {
			"shift":shift.name
		}
		attendance_log = frappe.get_all("Attendance Log",fields="*",filters=filters, order_by="employee,attendance_time")
		for key, group in itertools.groupby(attendance_log, key=lambda x: (x['employee'], x['shift_start_time'])):
			print(key)
			# frappe.errprint(list(group))
			logs = list(group)
			if logs:
				print('in')
				total_hours = 0
				in_time = out_time = None
				in_time = get_time(logs[0].attendance_time)
				if len(logs) >= 2:
					out_time = get_time(logs[-1].attendance_time)
				print(len(logs))
				if not len(logs) % 2 == 0:
					print('Miss Punch')
				logs = logs[:]
				while len(logs) >= 2:
					total_hours += time_diff_in_hours(logs[0].attendance_time,logs[1].attendance_time)
					del logs[:2]

				print('-----------------')
				print(in_time)
				print(out_time)
				print(total_hours)

def time_diff_in_hours(start, end):
	print(start)
	print(end)
	print(time_diff(end, start).total_seconds() / 60)
	return round(time_diff(end, start).total_seconds() / 60,1)