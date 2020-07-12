from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import formatdate, format_datetime, getdate, get_datetime, nowdate, flt, cstr, add_days, today,month_diff
from datetime import datetime
from erpnext.hr.doctype.salary_structure.salary_structure import make_salary_slip

@frappe.whitelist()
def validate_eligibility(employee):
	joining_date = frappe.db.get_value("Employee",employee,"date_of_joining")
	#month_diff = month_diff(today(),joining_date)
	d1=getdate(today())
	d2=getdate(joining_date)
	month_diff = diff_month(datetime(d1.year,d1.month,d1.day), datetime(d2.year,d2.month,d2.day))
	frappe.errprint(month_diff)
	if int(month_diff) < int(frappe.db.get_value("Loan Policies","Loan Policies","loan_eligibility_after")):
		return False
	else:
		amount = get_eligible_amount(employee)
		return amount

def diff_month(d1, d2):
	if d1.day>=d2.day-1:
		return (d1.year - d2.year) * 12 + d1.month - d2.month
	else:
		return (d1.year - d2.year) * 12 + d1.month - d2.month - 1


@frappe.whitelist()
def get_eligible_amount(employee):
	gross_pay = preview_salary_slip(employee)
	loan_policy = frappe.get_doc("Loan Policies","Loan Policies")
	if not loan_policy.no_of_salary_slip_for_eligible:
		frappe.throw(_("Set No of Salary Slip For Eligible Amount In Loan Policy"))
	eligible_dict = dict(
		gross_pay = gross_pay,
		eligible_amount = gross_pay * int(loan_policy.no_of_salary_slip_for_eligible),
		month = loan_policy.loan_repayment_period or 1
	)
	frappe.errprint(eligible_dict)
	return eligible_dict
	# salary_slips = frappe.get_all("Salary Slip",filters={"employee":employee,"docstatus":1},fields=["gross_pay"],order_by='modified desc',limit=3)
	# amount = 0
	# for slip in salary_slips:
	# 	amount += slip.gross_pay
	# return amount

@frappe.whitelist()
def preview_salary_slip(employee):
	sal_st = get_sal_structure(employee)
	salary_slip = make_salary_slip(sal_st, employee=employee,ignore_permissions=True)
	frappe.errprint(salary_slip)
	return salary_slip.gross_pay or 0

@frappe.whitelist()
def get_sal_structure(employee):
	cond = """and sa.employee=%(employee)s and sa.from_date <= %(date)s"""
	st_name = frappe.db.sql("""
		select sa.salary_structure
		from `tabSalary Structure Assignment` sa join `tabSalary Structure` ss
		where sa.salary_structure=ss.name
			and sa.docstatus = 1 and ss.docstatus = 1 and ss.is_active ='Yes' %s
		order by sa.from_date desc
		limit 1
	""" %cond, {'employee': employee, 'date':today()})

	if st_name:
		return st_name[0][0]
	else:
		frappe.msgprint(_("No active or default Salary Structure found for employee {0} for the given dates")
			.format(employee), title=_('Salary Structure Missing'))

@frappe.whitelist()
def get_guarantor_salary(employee,name=None):
	guarantors = frappe.db.sql("""SELECT lp.name
FROM `tabLoan Application` AS lp
INNER JOIN `tabLoan Guarantor` AS lg ON lp.name=lg.parent
WHERE lp.docstatus<>2 AND lg.status='Active' 
  AND lg.employee=%s And lp.name<>%s	
	""",(employee,name),as_dict=1)
	max_as_guarantor_in_loan = frappe.db.get_value("Loan Policies","Loan Policies","max_as_guarantor_in_loan") or 2
	if len(guarantors) >= int(max_as_guarantor_in_loan):
		frappe.msgprint(_("Employee {0} Already Available In {1} Loan Application").format(employee,len(guarantors)))
		return False
	return preview_salary_slip(employee)

@frappe.whitelist()
def validate_guarantor(self,method):
	if len(self.loan_guarantor) < 2:
		frappe.throw(_("2 Loan Guarantor Require For Loan Application"))