from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
                        "label": _("Loan Management"),
                        "items": [
                                {
                                        "type": "doctype",
                                        "name": "Loan Application",
                                        "label": "Loan Application",
                                        "description": _("Loan Application"),
                                        "onboard": 1
                                },
                                {
                                        "type": "doctype",
                                        "name": "Loan",
                                        "label": "Loan",
                                        "description": _("Loan"),
                                        "onboard": 1
                                },
                                {
                                        "type": "doctype",
                                        "name": "Loan Type",
                                        "label": "Loan Type",
                                        "description": _("Loan Type"),
                                        "onboard": 1
                                }
                        ]
                },
		{
                        "label": _("Loan Setting"),
                        "items": [
                                {
                                        "type": "doctype",
                                        "name": "Change Loan Guarantor",
                                        "label": "Change Loan Guarantor",
                                        "description": _("Change Loan Guarantor"),
                                        "onboard": 1
                                },
                                {
                                        "type": "doctype",
                                        "name": "Loan Policies",
                                        "label": "Loan Policies",
                                        "description": _("Loan Policies"),
                                        "onboard": 1
                                }
                        ]
                },
		{
			"label": _("Policies"),
			"items": [
				{
                                        "type": "doctype",
                                        "name": "Attendance Policies",
                                        "label": "Attendance Policies",
                                        "description": _("Attendance Policies"),
                                        "onboard": 1
                                },
				{
                                        "type": "doctype",
                                        "name": "Attendance Machine Settings",
                                        "label": "Attendance Machine Settings",
                                        "description": _("Attendance Machine Settings"),
                                        "onboard": 1
                                },
				{
                                        "type": "doctype",
                                        "name": "Late Entry Policies",
                                        "label": "Late Entry Policies",
                                        "description": _("Late Entry Policies"),
                                        "onboard": 1
                                }
			]
		},
		{
                        "label": _("Approval"),
                        "items": [
                                {
                                        "type": "doctype",
                                        "name": "Gate Pass",
                                        "label": "Gate Pass",
                                        "description": _("Gate Pass"),
                                        "onboard": 1
                                },
				{
                                        "type": "doctype",
                                        "name": "Gate Pass Policies",
                                        "label": "Gate Pass Policies",
                                        "description": _("Gate Pass Policies"),
                                        "onboard": 1
                                }
                        ]
                },
		{
                        "label": _("Referral Bonus"),
                        "items": [
                                {
                                        "type": "doctype",
                                        "name": "Referral Bonus Application",
                                        "label": "Referral Bonus Application",
                                        "description": _("Referral Bonus Application"),
                                        "onboard": 1
                                },
                                {
                                        "type": "doctype",
                                        "name": "Referral Bonus Policies",
                                        "label": "Referral Bonus Policies",
                                        "description": _("Referral Bonus Policies"),
                                        "onboard": 1
                                }
                        ]
                },
		{
                        "label": _("Advance Salary"),
                        "items": [
                                {
                                        "type": "doctype",
                                        "name": "Employee Advance",
                                        "label": "Employee Advance",
                                        "description": _("Employee Advance"),
                                        "onboard": 1
                                },
                                {
                                        "type": "doctype",
                                        "name": "Advance Salary Policies",
                                        "label": "Advance Salary Policies",
                                        "description": _("Advance Salary Policies"),
                                        "onboard": 1
                                }
                        ]
                },
		{
                        "label": _("Overtime Tracking"),
                        "items": [
                                {
                                        "type": "doctype",
                                        "name": "Overtime Application",
                                        "label": "Overtime Application",
                                        "description": _("Overtime Application"),
                                        "onboard": 1
                                },
				{
                                        "type": "doctype",
                                        "name": "Overtime Policies",
                                        "label": "Overtime Policies",
                                        "description": _("Overtime Policies"),
                                        "onboard": 1
                                }
                        ]
                },
		{
                        "label": _("Miss Punch"),
                        "items": [
                                {
                                        "type": "doctype",
                                        "name": "Miss Punch Application",
                                        "label": "Miss Punch Application",
                                        "description": _("Miss Punch Application"),
                                        "onboard": 1
                                }
                        ]
                },
		{
                        "label": _("Shift Managemment"),
                        "items": [
                                {
                                        "type": "doctype",
                                        "name": "Shift Request",
                                        "label": "Shift Request",
                                        "description": _("Shift Request"),
                                        "onboard": 1
                                },
								{
                                        "type": "doctype",
                                        "name": "Update Shift Request",
                                        "label": "Update Shift Request",
                                        "description": _("Update Shift Request"),
                                        "onboard": 1
                                },
								{
                                        "type": "doctype",
                                        "name": "Shift Assignment",
                                        "label": "Shift Assignment",
                                        "description": _("Shift Assignment"),
                                        "onboard": 1
                                }
                        ]
                },
		{
                        "label": _("Report"),
                        "items": [
                                {
                                        "type": "report",
					"is_query_report": True,
                                        "name": "Attendance Log Report",
                                        "doctype": "Attendance Log"
                                }
                        ]
                }
]
