import frappe
from datetime import datetime, timedelta
from frappe.utils import add_days,today
from erpnext.hr.doctype.employee.employee import get_holiday_list_for_employee
from erpnext.hr.doctype.holiday_list.holiday_list import is_holiday
from erpnext.hr.doctype.employee.employee import get_holiday_list_for_employee

@frappe.whitelist()
def process_sandwich_leave(self,method):
	# try:
	process_sandwich_leave_daily(self)
	# process_sandwich_leave_weekly(self)
	# except Exception as e:
	# 	frappe.log_error(frappe.get_traceback())

def process_sandwich_leave_daily(self):
	holiday_date = []
	last_date = add_days(self.attendance_date,-1)
	on_leave = leave_check = False
	while leave_check == False:
		if check_leave(self,last_date):
			last_date = add_days(last_date,-1)
			on_leave = True
		else:
			leave_check = True
	holiday = get_holiday_list_for_employee(self.employee)
	frappe.errprint(holiday)
	if on_leave == True:
		while check_holiday(last_date,holiday):
			frappe.errprint('holiday')
			holiday_date.append(last_date)
			last_date = add_days(last_date,-1)
		if len(holiday_date) >= 1:
			if check_leave(self,last_date):
				for hd in holiday_date:
					create_leave(self.employee,hd,0)

@frappe.whitelist()
def process_sandwich_leave_weekly():
	sunday = today()
	first_day_of_week = add_days(sunday,-6)
	employees = get_employess(first_day_of_week,sunday)
	for employee in employees:
		if check_weekly_leave(employee.employee,first_day_of_week,sunday):
			create_leave(employee.employee,sunday,0)

def check_weekly_leave(employee,from_date,to_date):
	filters = [
		['employee', '=', employee],
		['from_date', '>=', from_date],
		['to_date', '<=',to_date],
		['docstatus','=',1],
		['leave_type', 'in',["Leave Without Pay","Miss Punch"]]
	]
	leave_application = frappe.get_all("Leave Application",filters=filters,fields=["name"])
	if len(leave_application) > 1:
		return True
	else:
		return False


def check_holiday(date,holiday):
	holiday = frappe.db.sql("""select holiday_date from `tabHoliday` where holiday_date=%s and parent=%s""",(date,holiday),as_dict=1)
	if len(holiday) >= 1:
		return True
	else:
		return False

def check_leave(self,date):
	filters = [
		['employee', '=', self.employee],
		['docstatus','=',1],
		['from_date', '<=', date],
		['to_date', '>=',date],
		['half_day', '=',0],
		['leave_type', 'in',["Leave Without Pay","Miss Punch"]]
	]
	leave_application = frappe.get_all("Leave Application",filters=filters,fields=["name"])
	frappe.errprint(leave_application)
	if len(leave_application) >= 1:
		return True
	else:
		return False

def create_leave(employee,date,half_day):
	if half_day == 1:
		doc = frappe.get_doc(dict(
			doctype = "Leave Application",
			employee = employee,
			from_date = date,
			to_date = date,
			half_day = half_day,
			leave_type = "Half Day",
			follow_via_email = 0,
			leave_approver = frappe.db.get_value("Employee",employee,"leave_approver")
		)).insert(ignore_permissions = True)
		doc.status = "Approved"
		doc.submit()

	if half_day == 0:
		doc = frappe.get_doc(dict(
			doctype = "Leave Application",
			employee = employee,
			from_date = date,
			to_date = date,
			half_day = half_day,
			leave_type = "Leave Without Pay",
			follow_via_email = 0,
			leave_approver = frappe.db.get_value("Employee",employee,"leave_approver")
		)).insert(ignore_permissions = True)
		doc.status = "Approved"
		doc.submit()


def get_employess(from_date,to_date):
	employee_list = frappe.db.sql("""select distinct employee from `tabLeave Application` where from_date>=%s and to_date<=%s""",(from_date,add_days(to_date,-1)),as_dict=1)
	print(employee_list)
	return employee_list or []
