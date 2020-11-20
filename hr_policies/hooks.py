# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "hr_policies"
app_title = "Hr Policies"
app_publisher = "Hardik gadesha"
app_description = "App for custom HR"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "hardikgadesha@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/hr_policies/css/hr_policies.css"
# app_include_js = "/assets/hr_policies/js/hr_policies.js"

# include js, css files in header of web template
# web_include_css = "/assets/hr_policies/css/hr_policies.css"
# web_include_js = "/assets/hr_policies/js/hr_policies.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views

doctype_js = {
	"Employee Advance" : "public/js/employee_advance.js",
	"Employee" : "public/js/employee.js",
	"Loan Application" : "public/js/loan_application.js"
}


# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "hr_policies.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "hr_policies.install.before_install"
# after_install = "hr_policies.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "hr_policies.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Loan Application": {
		"validate": "hr_policies.custom_validate.validate_guarantor"
	},
	"Employee": {
		"on_change": "hr_policies.hr_policies.doctype.referral_bonus_application.referral_bonus_application.updateADS",
		"validate":"hr_policies.custom_validate.check_guarantor_in_loan"
	},
	"Employee Advance": {
		"validate": "hr_policies.custom_validate.validate_loan_amount_for_advance",
		"on_submit":"hr_policies.custom_validate.add_additional_salary",
		"on_cancel":"hr_policies.custom_validate.cancel_advance_salary"
	},
	"Attendance Log":{
		"before_insert":"hr_policies.attendance_integration.update_attendance_log"
	},
	"Attendance":{
		"on_submit":"hr_policies.attendance_integration.add_late_entry",
		"before_submit":"hr_policies.process_attendance.process_sandwich_leave"
	}
}

fixtures = [
	{
	"doctype": "Role",
	"filters": [
            [
		"name",
		"in",
		[
			 "HR Master Manager"
	    ]
	]
	]
	},
	{
        "doctype": "Custom Field",
        "filters": [
            [
                "name",
                "in",
                [
			"Gate Pass-workflow_state",
			"Loan Application-workflow_state",
			"Loan Application-gross_salary",
			"Loan Application-loan_guarantor",
			"Loan Application-guarantor_details",
			"Loan Application-eligible_amount",
			"Loan Application-section_break_1",
			"Loan Application-policies",
			"Employee-reference_of_employee_",
			"Additional Salary-bonus_for_employee",
			"Employee Advance-eligible_advance_amount_",
			"Employee Advance-additional_salary_id",
			"Employee Advance-extra_approval_require",
			"Employee Advance-emi_amount",
			"Employee Advance-remain_amount_eligible",
			"Employee-is_labour",
			"Employee-is_employee",
			"Employee-card_no",
			"Employee-has_rm",
			"Gate Pass-has_rm",
			"Employee Advance-has_rm",
			"Overtime Application-has_rm",
			"Miss Punch Application-has_rm",
			"Loan-has_rm",
			"Employee-has_rm",
			"Loan-department",
			"Loan-employee_name",
			"Loan-employee",
			"Loan Application-department",
			"Loan Application-employee_name",
			"Loan Application-employee",
			"Miss Punch Application-department",
			"Attendance-in_time",
			"Attendance-out_time",
			"Attendance-miss_punch",
			"Attendance-overtime",
			"Attendance-office_hours",
			"Attendance Extra Entry-calculated",
			"Shift Type-shift_type",
			"Shift Type-section_break_1",
			"Shift Assignment-shift_time_type"
		]
	   ]
	]
    }
]


# Scheduled Tasks
# ---------------

scheduler_events = {
	"cron": {
		"30 23 1 * *": [
			"hr_policies.hr_policies.doctype.gate_pass.gate_pass.insertGP",
			"hr_policies.hr_policies.doctype.gate_pass.gate_pass.insertOT",
			"hr_policies.attendance_integration.add_late_entry_deduction",
			"hr_policies.custom_validate.add_holiday_earning",
		],
		"0 9 * * *":[
			"hr_policies.attendance_integration.process_attendance"
		],
		"0 18 * * *":[
                        "hr_policies.attendance_integration.process_attendance_night_shift"
                ],
		"30 23 * * Sun":[
			"hr_policies.process_attendance.process_sandwich_leave_weekly"
		],
		"0 22 * * *":[
                        "hr_policies.custom_validate.changeDayShift"
                ],
		"0 13 * * *":[
                        "hr_policies.custom_validate.changeNightShift"
                ]
	}

}

# Testing
# -------

# before_tests = "hr_policies.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "hr_policies.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "hr_policies.task.get_dashboard_data"
# }

