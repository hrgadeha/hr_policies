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
					"name": "Referral Bonus Policies",
					"label": "Referral Bonus Policies",
					"description": _("Referral Bonus Policies"),
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
                        "label": _("Approval"),
                        "items": [
                                {
                                        "type": "doctype",
                                        "name": "Gate Pass",
                                        "label": "Gate Pass",
                                        "description": _("Gate Pass"),
                                        "onboard": 1
                                }
                        ]
                }

]
