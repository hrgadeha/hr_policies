# -*- coding: utf-8 -*-
# Copyright (c) 2020, Hardik gadesha and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _, throw, msgprint
from frappe.model.document import Document
from frappe.utils import nowdate
from datetime import datetime, timedelta

class GatePass(Document):
	def validate(self):
		gp = frappe.db.sql("""select count(name) from `tabGate Pass` where MONTH(date) = MONTH(%s) AND YEAR(date) = YEAR(%s) and type = "Personal" 
			and docstatus = 1 and employee = %s;""",(self.date,self.date,self.employee),as_list = True)
		self.lop = 0
		#	lop only true if one of below condition true
		#	in both case we allow to create gate pass but in case of not follow any of following condition we will deduct salary
		#	Discusd with taiyab khan 
		# 	change by Jigar Tarpara
		if self.type == "Personal" and self.apply_for > frappe.db.get_single_value("Gate Pass Policies", "personal_gate_pass_allowance_time"):
			self.lop = 1
			frappe.msgprint(_("You crossed your gate pass allowance limit more then {0} Minutes").format(frappe.db.get_single_value("Gate Pass Policies", "personal_gate_pass_allowance_time")))

		if self.type == "Personal" and int(gp[0][0]) >= int(frappe.db.get_single_value("Gate Pass Policies", "no_of_gate_pass_allowed_for_personal_work")):
			self.lop = 1
			frappe.msgprint("You crossed your gate pass allowance limit per month, this gate pass may result in deduction in salary")			
		# In Case of Employee is "Is Labour" True Then LOP must 1 as labour will charge for any exit in shift
		is_labour = frappe.db.get_value("Employee", self.employee,"is_labour")
		if is_labour:
			self.lop = 1

@frappe.whitelist()
def getPLS():
	pls = []
	no = frappe.db.get_single_value('Gate Pass Policies', 'no_of_gate_pass_allowed_for_personal_work')
	pls.append(no)
	time = frappe.db.get_single_value('Gate Pass Policies', 'personal_gate_pass_allowance_time')
	pls.append(time)
	return pls


def insertGP():
	data = frappe.db.sql("""select employee,((sum(apply_for)/60)*hourly_rate),company
				from `tabGate Pass` where docstatus = 1 and lop = 1 and deducted = 0 and
				YEAR(date) = YEAR(CURRENT_DATE - INTERVAL 1 MONTH) AND MONTH(date) = MONTH(CURRENT_DATE - INTERVAL 1 MONTH)
				group by employee;""",as_list=True)

	name = frappe.db.sql("""SELECT name FROM `tabGate Pass` WHERE YEAR(date) = YEAR(CURRENT_DATE - INTERVAL 1 MONTH)
			AND MONTH(date) = MONTH(CURRENT_DATE - INTERVAL 1 MONTH) and deducted = 0 
			and lop = 1 and docstatus = 1;""",as_list=True)

	if data:
		for d in data:
			ads = frappe.get_doc({
			"doctype": "Additional Salary",
			"employee": d[0],
			"payroll_date": datetime.today() - timedelta(days=1),
			"company": d[2],
			"salary_component": frappe.db.get_single_value('Gate Pass Policies', 'gate_pass_component'),
			"amount": d[1],
			"overwrite_salary_structure_amount": 1
			})
			ads.insert(ignore_permissions=True,ignore_mandatory = True)
			ads.save(ignore_permissions=True)
			ads.submit()


	if name:
		for i in name:
			gp = frappe.get_doc("Gate Pass", i[0])
			gp.deducted = 1
			gp.save(ignore_permissions=True)


def insertOT():
	data = frappe.db.sql("""select employee,(sum(overtime_worked) * overtime_wages),company
				from `tabOvertime Application` where docstatus = 1 and paid = 0 and
				YEAR(request_date) = YEAR(CURRENT_DATE - INTERVAL 1 MONTH) AND MONTH(request_date) = MONTH(CURRENT_DATE - INTERVAL 1 MONTH)
				group by employee;""",as_list=True)

	name = frappe.db.sql("""SELECT name FROM `tabOvertime Application` WHERE YEAR(request_date) = YEAR(CURRENT_DATE - INTERVAL 1 MONTH)
			AND MONTH(request_date) = MONTH(CURRENT_DATE - INTERVAL 1 MONTH) and paid = 0 
			and docstatus = 1;""",as_list=True)

	if data:
		for d in data:
			ads = frappe.get_doc({
			"doctype": "Additional Salary",
			"employee": d[0],
			"payroll_date": datetime.today() - timedelta(days=1),
			"company": d[2],
			"salary_component": frappe.db.get_single_value('Overtime Policies', 'overtime_component'),
			"amount": d[1],
			"overwrite_salary_structure_amount": 1
			})
			ads.insert(ignore_permissions=True,ignore_mandatory = True)
			ads.save(ignore_permissions=True)
			ads.submit()


	if name:
		for i in name:
			ot = frappe.get_doc("Overtime Application", i[0])
			ot.paid = 1
			ot.save(ignore_permissions=True)
