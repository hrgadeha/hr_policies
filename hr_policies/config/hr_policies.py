from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Policies"),
			"items": [
				{
                                        "type": "doctype",
                                        "name": "Loan Policies",
                                        "label": "Loan Policies",
                                        "description": _("Loan Policies"),
                                        "onboard": 1
                                },
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
