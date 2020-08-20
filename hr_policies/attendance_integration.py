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
def run_attendance_manually():
	start_date = '2020-07-01'
	end_date = '2020-07-31'
	while getdate(start_date) <= getdate(end_date):
		print('Attendance Process Start For Date ' + str(start_date))
		process_attendance(start_date)
		start_date = add_days(start_date,1)

@frappe.whitelist()
def process_attendance(date=None):
	try:
		if date == None:
			date = add_days(today(),-1)
		shift_data = frappe.get_all("Shift Type",filters={},fields=["name","start_time","end_time"])
		for shift in shift_data:
			# filters = {
			# 	"shift":shift.name
			# }
			attendance_log = frappe.db.sql("""select * from `tabAttendance Log` where shift=%s and Date(attendance_time)=%s order by employee,attendance_time""",(shift.name,date),as_dict=1)
			# attendance_log = frappe.get_all("Attendance Log",fields="*",filters=filters, order_by="employee,attendance_time")
			for key, group in itertools.groupby(attendance_log, key=lambda x: (x['employee'], x['shift_start_time'])):
				print(key)
				# frappe.errprint(list(group))
				logs = list(group)
				if logs:
					try:
						in_time,out_time,total_hours,early_exit,late_entry,miss_punch = get_attendance_details(shift,logs)
						create_attendance(logs[0].employee,getdate(logs[0].attendance_time),in_time,out_time,total_hours,early_exit,late_entry,miss_punch,shift)
					except Exception as e:
						frappe.log_error(frappe.get_traceback())
	except Exception as e:
		frappe.log_error(frappe.get_traceback())

def get_attendance_details(shift_details,logs):
	print('in')
	last_logs = logs
	total_hours = 0
	in_time = out_time = None
	late_entry = early_exit = miss_punch = False
	in_time = get_time(logs[0].attendance_time)
	if len(logs) >= 2:
		out_time = get_time(logs[-1].attendance_time)
	else:
		out_time = get_time(logs[0].attendance_time)
	if not len(logs) % 2 == 0:
		miss_punch = True
		create_miss_punch_entry(logs[-1].employee,getdate(logs[0].attendance_time),logs[-1].attendance_type,get_time(logs[-1].attendance_time))
		print('Miss Punch')
	logs = logs[:]
	while len(logs) >= 2:
		total_hours += time_diff_in_hours(logs[0].attendance_time,logs[1].attendance_time)
		del logs[:2]
	if get_time(in_time) > get_time(shift_details.start_time):
		print('late_entry')
		if last_logs:
			gate_pass_details = get_gatepass_details(last_logs[0].employee,getdate(last_logs[0].attendance_time))
			print(gate_pass_details)
			if gate_pass_details:
				for gate_row in gate_pass_details:
					print('inside')
					print(get_time(gate_row.from_time))
					if get_time(gate_row.from_time) <= get_time(shift_details.start_time) and get_time(gate_row.to_time) >= get_time(shift_details.start_time):
						late_entry =False
					else:
						late_entry = True
			else:
				late_entry = True
		else:
			late_entry = True
	if get_time(out_time) < get_time(shift_details.end_time):
		print('early exit')
		early_exit = True
	return in_time,out_time,total_hours,early_exit,late_entry,miss_punch

def create_miss_punch_entry(employee,attendance_date,last_punch_type,last_punch_time):
	doc = frappe.get_doc(dict(
		doctype = "Miss Punch Entry",
		employee = employee,
		attendance_date = attendance_date,
		last_punch_time = last_punch_time,
		last_punch_type = last_punch_type
	)).insert(ignore_permissions = True)

def create_attendance(employee,attendance_date,in_time,out_time,total_hours,early_exit,late_entry,miss_punch,shift):
	print(shift)
	office_hours = flt(time_diff_in_hours(shift.start_time,shift.end_time)) / 60
	working_hours = flt(total_hours) / 60
	working_hours += get_pass_approved_hours(employee,attendance_date)
	print(office_hours)
	attendance_doc = frappe.get_doc(dict(
		doctype = "Attendance",
		attendance_date = attendance_date,
		in_time = in_time,
		out_time = out_time,
		late_entry = late_entry,
		early_exit = early_exit,
		employee = employee,
		shift = shift.name,
		working_hours = working_hours,
		office_hours = office_hours,
		miss_punch = miss_punch,
		overtime = flt(working_hours)-flt(office_hours) if flt(working_hours) > flt(office_hours) else 0
	)).insert(ignore_permissions = True)
	if not attendance_doc.miss_punch:
		attendance_doc.submit()

def get_gatepass_details(employee,date):
	get_pass_details = frappe.db.sql("""
SELECT from_time,to_time 
FROM `tabGate Pass`
WHERE employee=%s
  AND date=%s
  AND docstatus=1
  AND lop=0
	""",(employee,date),as_dict=1)
	return get_pass_details

def get_pass_approved_hours(employee,date):
	get_pass_details = frappe.db.sql("""
SELECT sum(apply_for) AS 'gate_pass_mins'
FROM `tabGate Pass`
WHERE employee=%s
  AND date=%s
  AND docstatus=1
  AND lop=0
	""",(employee,date),as_dict=1)
	print(get_pass_details)
	if len(get_pass_details) >= 1:
		if not get_pass_details[0].gate_pass_mins == None and get_pass_details[0].gate_pass_mins > 0:
			return flt(get_pass_details[0].gate_pass_mins) / 60
		else:
			return 0
	else:
		return 0

def time_diff_in_hours(start, end):
	print(start)
	print(end)
	print(time_diff(end, start).total_seconds() / 60)
	return round(time_diff(end, start).total_seconds() / 60,1)

@frappe.whitelist()
def add_late_entry(self,method):
	frappe.msgprint('call')
	import math
	att_settings = frappe.get_doc("Attendance Policies","Attendance Policies")
	if self.employee and self.late_entry == 1:
		is_labour = frappe.db.get_value("Employee",self.employee,"is_labour")
		if is_labour:
			if flt(self.office_hours) > flt(self.working_hours):
				late_hours = math.ceil(flt(self.office_hours) - flt(self.working_hours))
				if late_hours > 0:
					create_extra_entry(self.employee,self.attendance_date,1,0,late_hours,'Less Hours By Labour')
		else:
			is_employee = frappe.db.get_value("Employee",self.employee,"is_employee")
			if is_employee:
				late_mins = time_diff_in_hours(str(frappe.db.get_value("Shift Type",self.shift,"start_time")),str(self.in_time))
				if self.early_exit == 1:
					early_exit_min = time_diff_in_hours(str(self.out_time),str(frappe.db.get_value("Shift Type",self.shift,"end_time")))
					if early_exit_min > 0:
						create_extra_entry(self.employee,self.attendance_date,0,1,flt(early_exit_min)/60,'Early Exit')
				if flt(late_mins) >=  flt(att_settings.late_allowance_for) and flt(late_mins) <= flt(att_settings.max_late_allowance_for):
					# if self.early_exit == 1:
					# 	early_exit_min = time_diff_in_hours(str(frappe.db.get_value("Shift Type",self.shift,"end_time")),str(self.out_time))
					# late_mins += flt(early_exit_min)
					create_extra_entry(self.employee,self.attendance_date,0,1,flt(late_mins)/60,'Late Entry')
				else:
					if flt(late_mins) > flt(att_settings.max_late_allowance_for):
						create_leave(employee,date)
	else:
		is_employee = frappe.db.get_value("Employee",self.employee,"is_employee")
		if is_employee and self.early_exit == 1:
			early_exit_min = time_diff_in_hours(str(frappe.db.get_value("Shift Type",self.shift,"end_time")),str(self.out_time))
			if early_exit_min > 0:
				create_extra_entry(self.employee,self.attendance_date,0,1,flt(early_exit_min)/60,'Early Exit')		


def create_leave(employee,date):
	doc = frappe.get_doc(dict(
		doctype = "Leave Application",
		from_date = date,
		to_date = date,
		half_day = 1,
		leave_type = "Leave Without Pay",
		leave_approver = frappe.db.get_value("Employee",employee,"leave_approver")
	)).insert(ignore_permissions = True)
	doc.status = "Approved"
	doc.submit()

def create_extra_entry(employee,date,is_labour,is_employee,hours,entry_type=None):
	doc = frappe.get_doc(dict(
		doctype = "Attendance Extra Entry",
		employee = employee,
		is_labour = is_labour,
		is_employee= is_employee,
		hours =hours,
		date = date,
		type = entry_type
	)).insert(ignore_permissions = True)

@frappe.whitelist()
def add_late_entry_deduction():
	from hr_policies.custom_validate import preview_salary_slip_for_late_entry
	end_date = add_days(today(),-1)
	start_date = get_first_day(end_date)
	late_entry_doc = frappe.db.sql("""select employee,sum(hours) as 'hours' from `tabAttendance Extra Entry` where date between %s and %s group by employee""",(start_date,end_date),as_dict=1)
	for row in late_entry_doc:
		try:
			salary_slip = preview_salary_slip_for_late_entry(row.employee)
			day_rate = salary_slip.gross_pay / salary_slip.total_working_days
			shift_hours = get_shift_for_late_entry(row.employee,start_date,end_date)
			hourly_rate = 0
			if not shift_hours == False and shift_hours > 0:
				hourly_rate = flt(day_rate) / flt(shift_hours)
				amount = hourly_rate * row.hours
				add_deduction_for_late_entry(row.employee,end_date,amount)
			else:
				frappe.throw(_("Employee {0} Shift Not Define").format(row.employee))
		except Exception as e:
			frappe.log_error(frappe.get_traceback())

def get_shift_for_late_entry(employee,start_date,end_date):
	shift_data = frappe.db.sql("""select shift from `tabAttendance` where attendance_date between %s and %s limit 1""",(start_date,end_date),as_dict=1)
	if shift_data:
		if not shift_data[0].shift == None:
			shift = frappe.get_doc("Shift Type",shift_data[0].shift)
			return flt(time_diff_in_hours(shift.start_time,shift.end_time)) / 60
		else:
			default_shift = frappe.db.get_value("Employee",employee,"default_shift")
			if default_shift:
				shift = frappe.get_doc("Shift Type",default_shift)
				return flt(time_diff_in_hours(shift.start_time,shift.end_time)) / 60
			else:
				return False
	else:
		return False

def add_deduction_for_late_entry(employee,date,amount):
	doc = frappe.get_doc(dict(
		doctype = "Additional Salary",
		payroll_date = date,
		employee = employee,
		company = frappe.db.get_value("Global Defaults","Global Defaults","default_company"),
		salary_component = frappe.db.get_single_value('Late Entry Policies', 'late_entry_deduction_component'),
		amount = amount,
		overwrite_salary_structure_amount = 1
	)).insert(ignore_permissions = True)
	doc.submit()


@frappe.whitelist()
def get_last_id_attendance():
	return frappe.db.get_value("Attendance Machine Settings","Attendance Machine Settings","last_number")