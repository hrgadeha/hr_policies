from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import formatdate, format_datetime, getdate, get_datetime,get_first_day,get_last_day, nowdate, flt, cint, cstr, add_days, today,month_diff,date_diff,add_months
from datetime import datetime,timedelta
from erpnext.hr.doctype.salary_structure.salary_structure import make_salary_slip
from frappe.model.mapper import get_mapped_doc
from erpnext.hr.doctype.employee.employee import get_holiday_list_for_employee
from frappe.utils import nowdate
from datetime import datetime, timedelta
import json
from ast import literal_eval

@frappe.whitelist()
def validate_eligibility(employee):
	joining_date = frappe.db.get_value("Employee",employee,"date_of_joining")
	#month_diff = month_diff(today(),joining_date)
	d1=getdate(today())
	d2=getdate(joining_date)
	month_diff = diff_month(datetime(d1.year,d1.month,d1.day), datetime(d2.year,d2.month,d2.day))
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
	no_of_guarantor_need = frappe.db.get_value("Loan Policies","Loan Policies","no_of_guarantor_need") or 2
	if len(self.loan_guarantor) < flt(no_of_guarantor_need):
		frappe.throw(_("2 Loan Guarantor Require For Loan Application"))

#check when employee left
@frappe.whitelist()
def check_guarantor_in_loan(self,method):
	# frappe.msgprint('call')
	if self.status == "Left":
		filters = [
			["Loan Guarantor","employee","=",self.name],
			["Loan Guarantor","status","=","Active"]
		]
		loan_applications = frappe.get_all("Loan Application",filters=filters,fields=["name"])
		if loan_applications:
			for loan_application in loan_applications:
				filters = [
					["loan_application","=",loan_application.name],
					["docstatus","=",1]
				]
				loan_doc = frappe.get_all("Loan",filters=filters,fields=["total_payment","total_amount_paid"])
				if len(loan_doc) >= 1:
					for loan in loan_doc:
						if flt(loan.total_payment) <= flt(loan.total_amount_paid):
							frappe.throw(_("Employee Available As A Guarantor For Loan Application {0}").format(loan_application.name))


@frappe.whitelist()
def getPLS():
	pls = []
	pls.append(frappe.db.get_single_value('Loan Policies', 'loan_eligibility_after'))
	pls.append(frappe.db.get_single_value('Loan Policies', 'loan_repayment_period'))
	pls.append(frappe.db.get_single_value('Loan Policies', 'no_of_guarantor_need'))
	pls.append(frappe.db.get_single_value('Loan Policies', 'no_of_salary_slip_for_eligible'))
	pls.append(frappe.db.get_single_value('Loan Policies', 'max_as_guarantor_in_loan'))
	return pls

#validate salary advance
@frappe.whitelist()
def validate_employee_advance(employee,date):
	policies = frappe.get_doc("Advance Salary Policies","Advance Salary Policies")
	employee_type = frappe.db.get_value("Employee",employee,"employment_type")
	if employee_type == "Probation":
		frappe.msgprint(_("Advance Salary Request Apply After Probation Period"))
		return False
	start_date = frappe.db.get_value("Employee",employee,"final_confirmation_date")
	if getdate(start_date) > getdate(date):
		frappe.msgprint(_("Advance Salary Request Apply After Probation Period"))
		return False
	if get_salary_advance_total(employee,date,policies) == True:
		frappe.msgprint(_("Already Applied Employee Advance In Last 6 Months"))
		return False
	sal_st = get_sal_structure(employee)
	salary_slip = make_salary_slip_custom(sal_st, employee=employee,start_date=get_first_day(date),end_date=add_days(get_first_day(date),19), ignore_permissions=True)
	if salary_slip.gross_pay > flt(policies.salary_should_be_below_or_equal_to):
		frappe.msgprint(_("Gross Pay Must Be Less Than or Equal {0}").format(policies.salary_should_be_below_or_equal_to))
		return False		
	holiday_list = get_holiday_list_for_employee(employee, False)
	attendance = get_filtered_date_list(employee, get_first_day(date), add_days(get_first_day(date),19),holiday_list)
	working_days = date_diff(get_last_day(date),get_first_day(date)) + 1
	gross_pay_day = salary_slip.gross_pay / working_days
	final_working_days = 20 - ((flt(salary_slip.total_working_days)-len(get_holidays_for_employee(employee,get_first_day(date), add_days(get_first_day(date),19)))) - flt(attendance))
	gross_pay_eligible_for_advance = (flt(gross_pay_day) * flt(final_working_days))
	loan = get_loan_amount(employee,get_first_day(date),get_last_day(date))
	return gross_pay_eligible_for_advance,loan

def get_salary_advance_total(employee,date,policies):
	if not policies.advance_salary_eligible_after_month:
		frappe.throw(_("Set Advance Salary Eligible After Month In Advance Salary Policies"))
	start_date = add_months(date,policies.advance_salary_eligible_after_month*-1)
	end_date = date
	advance_salary = frappe.db.sql("""select count(*) as 'count' from `tabEmployee Advance` where docstatus=1 and posting_date between %s and %s and employee=%s""",(start_date,end_date,employee),as_dict=1)
	frappe.errprint(advance_salary)
	if advance_salary and advance_salary[0].count > 0:
		return True
	else:
		return False


def get_filtered_date_list(employee,start_date,end_date,holiday_list):
	attendance = frappe.db.sql("""
SELECT count(name) as 'att_count'
FROM `tabAttendance`
WHERE attendance_date NOT IN
    (SELECT hd.holiday_date
     FROM `tabHoliday List` AS hl
     INNER JOIN `tabHoliday` AS hd ON hl.name=hd.parent
     WHERE hl.name=%s)
  AND employee=%s AND status='Present'  AND docstatus=1
  AND attendance_date BETWEEN %s AND %s
	""",(holiday_list,employee,start_date,end_date),as_dict=True)
	frappe.errprint(attendance)
	if attendance:
		return attendance[0].att_count
	else:
		return 0

def get_holidays_for_employee(employee, start_date, end_date):
	holiday_list = get_holiday_list_for_employee(employee)

	holidays = frappe.db.sql_list('''select holiday_date from `tabHoliday`
		where
			parent=%(holiday_list)s
			and holiday_date >= %(start_date)s
			and holiday_date <= %(end_date)s''', {
				"holiday_list": holiday_list,
				"start_date": start_date,
				"end_date": end_date
			})

	holidays = [cstr(i) for i in holidays]

	return holidays

def get_loan_amount(employee,start_date,end_date):
	loan = frappe.db.sql("""
SELECT rs.total_payment AS 'loan_amount'
FROM `tabLoan` AS loan
INNER JOIN `tabRepayment Schedule` AS rs ON loan.name=rs.parent
WHERE loan.applicant=%s
  AND rs.payment_date BETWEEN %s AND %s
  AND rs.paid=0	
	""",(employee,start_date,end_date),as_dict=1)
	if loan:
		return loan[0].loan_amount
	else:
		return 0

@frappe.whitelist()
def make_salary_slip_custom(source_name, target_doc = None, employee = None,start_date = None,end_date = None,as_print = False, print_format = None, for_preview=0, ignore_permissions=False):
	def postprocess(source, target):
		if employee:
			employee_details = frappe.db.get_value("Employee", employee,
				["employee_name", "branch", "designation", "department"], as_dict=1)
			target.employee = employee
			target.employee_name = employee_details.employee_name
			target.branch = employee_details.branch
			target.designation = employee_details.designation
			target.department = employee_details.department
			target.start_date = start_date
			target.end_date = end_date
		target.run_method('process_salary_structure', for_preview=for_preview)

	doc = get_mapped_doc("Salary Structure", source_name, {
		"Salary Structure": {
			"doctype": "Salary Slip",
			"field_map": {
				"total_earning": "gross_pay",
				"name": "salary_structure"
			}
		}
	}, target_doc, postprocess, ignore_child_tables=True, ignore_permissions=ignore_permissions)

	if cint(as_print):
		doc.name = 'Preview for {0}'.format(employee)
		return frappe.get_print(doc.doctype, doc.name, doc = doc, print_format = print_format)
	else:
		return doc

@frappe.whitelist()
def validate_loan_amount_for_advance(self,method):
	if flt(self.emi_amount) > flt(self.remain_amount_eligible):
		self.extra_approval_require = 1
	else:
		self.extra_approval_require = 0

	if flt(self.advance_amount) > flt(self.eligible_advance_amount_):
		frappe.throw(_("Advance Amount Must Be Less Than Your Eligible Advance Salary"))

@frappe.whitelist()
def preview_working_days(employee):
        sal_st = get_sal_structure(employee)
        salary_slip = make_salary_slip(sal_st, employee=employee,ignore_permissions=True)
        frappe.errprint(salary_slip)
        return salary_slip.total_working_days or 0

@frappe.whitelist()
def get_hourly_rate(employee):
	gross_pay = preview_salary_slip(employee)
	working_days = preview_working_days(employee)

	hours = frappe.db.sql("""select office_hours from `tabAttendance` where docstatus = 1 and employee = %s order by creation desc 
			limit 1;""",(employee))

	eligible_dict = dict(
		gross_pay = gross_pay,
		per_day = (gross_pay / working_days) / hours[0][0]
	)
	frappe.errprint(eligible_dict)
	return eligible_dict

@frappe.whitelist()
def add_additional_salary(self,method):
	doc = frappe.get_doc(dict(
		doctype = "Additional Salary",
		payroll_date = get_last_day(self.posting_date),
		employee = self.employee,
		company = self.company,
		salary_component = frappe.db.get_single_value('Advance Salary Policies', 'advance_salary_component'),
		amount = self.advance_amount,
		overwrite_salary_structure_amount = 1
	)).insert(ignore_permissions = True)
	doc.submit()
	frappe.db.set_value(self.doctype,self.name,"additional_salary_id",doc.name)

@frappe.whitelist()
def cancel_advance_salary(self,method):
	if self.additional_salary_id:
		add_sal = frappe.get_doc("Additional Salary",self.additional_salary_id)
		add_sal.cancel()
		frappe.delete_doc("Additional Salary",add_sal.name)

@frappe.whitelist()
def add_attendance_log():
	try:
		main_data = get_request_form_data()
		attendance_data = main_data.data
		last_row_machine_id = ''
		for row in eval(attendance_data):
			if not last_row_machine_id == '':
				if flt(last_row_machine_id) < flt(row[0]):
					last_row_machine_id = row[0]
			else:
				last_row_machine_id = row[0]
			if not frappe.db.exists("Attendance Log", {"machine_id": row[0]}):
				doc = frappe.get_doc(dict(
					doctype = "Attendance Log",
					card_no = row[1],
					attendance_type = 'IN',
					attendance_time = get_datetime(row[2]),
					machine_id = row[0]

				)).insert(ignore_permissions = True)
		frappe.db.set_value("Attendance Machine Settings","Attendance Machine Settings","last_number",last_row_machine_id)
		return last_row_machine_id
	except Exception as e:
		frappe.log_error(frappe.get_traceback())
		return False

def get_request_form_data():
	if frappe.local.form_dict.data is None:
		data = frappe.safe_decode(frappe.local.request.get_data())
	else:
		data = frappe.local.form_dict.data

	return frappe.parse_json(data)

@frappe.whitelist()
def preview_salary_slip_for_late_entry(employee):
	sal_st = get_sal_structure(employee)
	salary_slip = make_salary_slip(sal_st, employee=employee,ignore_permissions=True)
	return salary_slip


@frappe.whitelist()
def add_holiday_earning():
	data = frappe.db.sql("""select ha.employee,sum(ha.total_working_hours)
				from `tabHoliday Attendance` ha, `tabEmployee` emp where ha.total_working_hours != 0 and ha.added = 0 and
				YEAR(ha.date) = YEAR(CURRENT_DATE - INTERVAL 1 MONTH) AND 
				MONTH(ha.date) = MONTH(CURRENT_DATE - INTERVAL 1 MONTH) 
				and ha.employee = emp.name and emp.status = "Active"
				group by ha.employee;""",as_list=True)

	name = frappe.db.sql("""SELECT ha.name FROM `tabHoliday Attendance` ha, `tabEmployee` emp WHERE ha.total_working_hours != 0 and 
				YEAR(ha.date) = YEAR(CURRENT_DATE - INTERVAL 1 MONTH) AND 
				MONTH(ha.date) = MONTH(CURRENT_DATE - INTERVAL 1 MONTH) and ha.added = 0 and 
				ha.employee = emp.name and emp.status = "Active";""",as_list=True)


	if data:
		for d in data:
			salary_slip = preview_salary_slip_for_late_entry(d[0])
			day_rate = salary_slip.gross_pay / salary_slip.total_working_days

			hours = frappe.db.sql("""select office_hours from `tabAttendance` where status = "Present" and 
			docstatus = 1 and employee = %s and office_hours != 0 order by name desc limit 1;""",(d[0]))

			per_hr = day_rate / abs(hours[0][0])
#			print(d[0])
#			print(int(per_hr))

			ads = frappe.get_doc({
			"doctype": "Additional Salary",
			"employee": d[0],
			"payroll_date": datetime.today() - timedelta(days=1),
			"company": frappe.db.get_single_value('Global Defaults', 'default_company'),
			"salary_component": frappe.db.get_single_value('Attendance Policies', 'holiday_wages_component'),
			"amount": int(per_hr * d[1]),
			"overwrite_salary_structure_amount": 1
			})
			ads.insert(ignore_permissions=True,ignore_mandatory = True)
			ads.save(ignore_permissions=True)
			ads.submit()


	if name:
		for i in name:
			ot = frappe.get_doc("Holiday Attendance", i[0])
			ot.added = 1
			ot.save(ignore_permissions=True)

@frappe.whitelist()
def add_1_day_in_leave():
	for d in frappe.get_list("Leave Allocation", fields=("name"), filters={"docstatus": 1 }):
		if d:
			doc = frappe.get_doc("Leave Allocation", d)
			doc.new_leaves_allocated += 1
			doc.total_leaves_allocated += 1
			doc.save()




@frappe.whitelist()
def changeDayShift():
	data = frappe.db.sql("""select employee,shift_type
				from `tabShift Assignment` where docstatus = 1 and shift_time_type = "Day Shift"
				and date = DATE_ADD(CURDATE(),INTERVAL 1 DAY);""",as_list=True)

	if data:
		for d in data:
			doc = frappe.get_doc("Employee", d[0])
			doc.default_shift = d[1]
			doc.save(ignore_permissions=True)

@frappe.whitelist()
def changeNightShift():
	data = frappe.db.sql("""select employee,shift_type
                                from `tabShift Assignment` where docstatus = 1 and shift_time_type = "Night Shift"
                                and date = DATE_ADD(CURDATE(),INTERVAL 1 DAY);""",as_list=True)

	if data:
		for d in data:
			doc = frappe.get_doc("Employee", d[0])
			doc.default_shift = d[1]
			doc.save(ignore_permissions=True)
