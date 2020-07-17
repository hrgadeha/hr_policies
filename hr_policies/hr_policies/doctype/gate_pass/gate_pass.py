# -*- coding: utf-8 -*-
# Copyright (c) 2020, Hardik gadesha and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _, throw, msgprint
from frappe.model.document import Document

class GatePass(Document):
	def validate(self):
		gp = frappe.db.sql("""select count(name) from `tabGate Pass` where MONTH(date_time) = MONTH(%s) AND YEAR(date_time) = YEAR(%s) and type = "Personal" 
			and docstatus = 1 and employee = %s;""",(self.date_time,self.date_time,self.employee),as_list = True)

		if self.type == "Personal" and self.apply_for > frappe.db.get_single_value("Gate Pass Policies", "personal_gate_pass_allowance_time"):
			frappe.throw(_("You are not allow for gate pass more then  {0} Minutes").format(frappe.db.get_single_value("Gate Pass Policies", "personal_gate_pass_allowance_time")))

		if self.type == "Personal" and int(gp[0][0]) >= int(frappe.db.get_single_value("Gate Pass Policies", "no_of_gate_pass_allowed_for_personal_work")):
			self.lop = 1
			frappe.msgprint("You crossed your gate pass allowance limit per month, this gate pass may result in deduction in salary")

		else:
			self.lop = 0


@frappe.whitelist()
def getPLS():
	pls = []
	no = frappe.db.get_single_value('Gate Pass Policies', 'no_of_gate_pass_allowed_for_personal_work')
	pls.append(no)
	time = frappe.db.get_single_value('Gate Pass Policies', 'personal_gate_pass_allowance_time')
	pls.append(time)
	return pls

