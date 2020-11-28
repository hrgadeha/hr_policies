# -*- coding: utf-8 -*-
# Copyright (c) 2020, Hardik gadesha and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import formatdate, get_time, time_diff,getdate, get_datetime,get_first_day,get_last_day, nowdate, flt, cint, cstr, add_days, today,month_diff,date_diff,add_months
from datetime import datetime
from frappe.model.document import Document

class MissPunchApplication(Document):
	def validate(self):
		if self.working_hours == 0 and self.office_hours == 0:
			FMT = '%H:%M:%S'
			dateTimeDifference = datetime.strptime(self.exit_time, FMT) - datetime.strptime(self.last_punch_time, FMT)
			self.working_hours =  dateTimeDifference.total_seconds() / 3600
			dateTimeDifference_shift = self.end_time - self.start_time
			self.office_hours =  dateTimeDifference_shift.total_seconds() / 3600

	def on_submit(self):
		if self.leave_application:
			doc = frappe.get_doc("Leave Application", self.leave_application)
			doc.delete()

		if self.attendance:
			doc = frappe.get_doc("Attendance", self.attendance)
			doc.delete()

		doc = frappe.get_doc(dict(
			doctype = "Attendance",
			attendance_date = self.miss_punch_date,
			status = "Present",
			in_time = self.last_punch_time,
			out_time = self.exit_time,
			employee = self.employee,
			shift = self.default_shift,
			working_hours = self.working_hours,
			office_hours = self.office_hours,
			overtime = flt(self.working_hours)-flt(self.office_hours) if flt(self.working_hours) > flt(self.office_hours) else 0,
		)).insert(ignore_permissions = True)
		doc.submit()

@frappe.whitelist(allow_guest=True)
def getattendance(employee,attendance_date):
	attendance = frappe.db.sql("""select name,in_time from `tabAttendance`
		where employee = %s and attendance_date = %s and miss_punch = 1 and docstatus = 0
		""",(employee,attendance_date))

	if attendance:
		return attendance
	else:
		return False


@frappe.whitelist(allow_guest=True)
def getlapp(employee,attendance_date):
	attendance = frappe.db.sql("""select name from `tabLeave Application`
                where employee = %s and from_date = %s and docstatus = 0
                """,(employee,attendance_date))

	if attendance:
		return attendance
	else:
		return False


@frappe.whitelist(allow_guest=True)
def getMinpunch(employee,attendance_date):
	attendance = frappe.db.sql("""SELECT min(time(attendance_time)) from `tabAttendance Log` where employee = %s
                        and date(attendance_time) = %s;""",(employee,attendance_date))

	if attendance:
		return attendance
	else:
		return False


@frappe.whitelist(allow_guest=True)
def getMaxpunch(employee,attendance_date):
	attendance = frappe.db.sql("""SELECT max(time(attendance_time)) from `tabAttendance Log` where employee = %s
                        and date(attendance_time) = %s;""",(employee,attendance_date))

	if attendance:
		return attendance
	else:
		return False
