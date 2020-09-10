# -*- coding: utf-8 -*-
# Copyright (c) 2020, Hardik gadesha and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class HolidayAttendance(Document):
	pass


def validateDate(date,employee):
	data = frappe.db.sql("""select name from `tabAttendance Log` where attendance_type = "IN" and date(attendance_time) = %s and 
			employee = %s;""",(date,employee),as_list=True)

	return data
