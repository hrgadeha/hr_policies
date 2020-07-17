# -*- coding: utf-8 -*-
# Copyright (c) 2020, Hardik gadesha and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import datetime
from dateutil.relativedelta import relativedelta
from calendar import monthrange
from frappe.model.document import Document

class ReferralBonusApplication(Document):
	def validate(self):
		validity = frappe.db.get_single_value('Referral Bonus Policies', 'bonus_applicable_after_month')
		self.bonus_applicable_on = (datetime.datetime.today() + relativedelta(months=+validity)).date()
		date_value = self.bonus_applicable_on
		self.bonus_payment_date = date_value.replace(day = monthrange(date_value.year, date_value.month)[1])
		if self.is_labour:
			self.bonus_applicable = frappe.db.get_single_value('Referral Bonus Policies', 'labour_referral_bonus')

		if self.is_employee:
			self.bonus_applicable = frappe.db.get_single_value('Referral Bonus Policies', 'staff_referral_bonus')


	def on_submit(self):
		validity = frappe.db.get_single_value('Referral Bonus Policies', 'bonus_applicable_after_month')
		self.bonus_applicable_on = (datetime.datetime.today() + relativedelta(months=+validity)).date()
		date_value = self.bonus_applicable_on
		self.bonus_payment_date = date_value.replace(day = monthrange(date_value.year, date_value.month)[1])

		ads = frappe.get_doc({
		"doctype": "Additional Salary",
		"payroll_date": self.bonus_payment_date,
		"employee": self.employee,
		"bonus_for_employee": self.applicant_id,
		"employee_name": self.emp_name,
		"company": self.company,
		"salary_component": frappe.db.get_single_value('Referral Bonus Policies', 'referral_bonus_component'),
		"amount": self.bonus_applicable,
		"overwrite_salary_structure_amount": 1
		})
		ads.insert(ignore_permissions=True,ignore_mandatory = True)
		ads.save(ignore_permissions=True)
		ads.submit()

		emp = frappe.get_doc("Employee",self.applicant_id)
		emp.reference_of_employee_ = self.employee
		emp.save(ignore_permissions=True)

@frappe.whitelist()
def getPLS():
	return frappe.db.get_single_value('Referral Bonus Policies', 'bonus_applicable_after_month')


@frappe.whitelist()
def updateADS(self,method):
	if self.status == "Left":
		ads = frappe.db.get_list('Additional Salary', filters={'employee': self.reference_of_employee_,'bonus_for_employee':self.name}, fields=['name'])
		for i in ads:
			salary = frappe.get_doc("Additional Salary",i)
			salary.cancel()
