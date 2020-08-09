# -*- coding: utf-8 -*-
# Copyright (c) 2020, Hardik gadesha and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class OvertimeApplication(Document):
	pass

@frappe.whitelist(allow_guest=True)
def getOT(employee,request_date):
	ot = frappe.db.sql("""select overtime from `tabAttendance` where employee = %s and attendance_date = %s and
				docstatus = 1;""",(employee,request_date),as_list = True)
	return ot
