# -*- coding: utf-8 -*-
# Copyright (c) 2020, Hardik gadesha and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class ChangeLoanGuarantor(Document):
	def validate(self):
		self.validate_old_guarantor()

	def validate_old_guarantor(self):
		if self.old_guarantor:
			loan_guarantors = frappe.db.sql("""select name from `tabLoan Guarantor` where parent=%s and employee=%s and status='Active'""",(self.loan_application,self.old_guarantor),as_dict=1)
			if not loan_guarantors:
				frappe.throw(_("Old Guarantor Must Be Available In Loan Application With Active State"))

	def on_submit(self):
		frappe.msgprint("Call")
		update_old_guarantor_status(self.old_guarantor,self.loan_application,'Deactive')
		res = update_new_guarantor_in_loan_application(self.new_guarantor,self.loan_application)
		self.new_guarantor_id = res

	def on_cancel(self):
		frappe.msgprint("Call")
		update_old_guarantor_status(self.old_guarantor,self.loan_application,'Active')
		delete_new_guarantor_in_loan_application(self.new_guarantor_id)

@frappe.whitelist()
def update_old_guarantor_status(employee,loan_application,status):
	frappe.db.sql("""Update `tabLoan Guarantor` set status=%s where parent=%s and employee=%s""",(status,loan_application,employee))

@frappe.whitelist()
def update_new_guarantor_in_loan_application(employee,loan_application):
	loan_doc = frappe.get_doc("Loan Application",loan_application)
	doc = frappe.get_doc(dict(
		doctype = "Loan Guarantor",
		parentfield = "loan_guarantor",
		parenttype = "Loan Application",
		idx = len(loan_doc.loan_guarantor) + 1,
		employee = employee,
		parent = loan_application,
		status = 'Active'
	)).insert(ignore_permissions = True)
	return doc.name

@frappe.whitelist()
def delete_new_guarantor_in_loan_application(new_guarantor_id):
	frappe.delete_doc("Loan Guarantor",new_guarantor_id)
	# frappe.db.sql("""delete from `tabLoan Guarantor` where name=%s""",new_guarantor_id)
