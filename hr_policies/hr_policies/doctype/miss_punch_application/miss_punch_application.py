# -*- coding: utf-8 -*-
# Copyright (c) 2020, Hardik gadesha and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class MissPunchApplication(Document):
	def on_submit(self):
		if self.action == "Present" and self.attendance:
			doc = frappe.get_doc("Attendance", self.attendance)
			doc.status = "Present"
			doc.save(ignore_permissions=True)
			doc.submit()

		if self.action == "Full Day Deduction" and self.leave_application:
			doc = frappe.get_doc("Attendance", self.attendance)
			doc.delete()

			doc = frappe.get_doc("Leave Application", self.leave_application)
			doc.status = "Approved"
			doc.save(ignore_permissions=True)
			doc.submit()

		if self.action == "Half Day Deduction" and self.leave_application:
			doc = frappe.get_doc("Attendance", self.attendance)
			doc.delete()

			doc = frappe.get_doc("Leave Application", self.leave_application)
			doc.half_day = 1
			doc.status = "Approved"
			doc.save(ignore_permissions=True)
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
