// Copyright (c) 2020, Hardik gadesha and contributors
// For license information, please see license.txt

frappe.ui.form.on('Overtime Application', {
	// refresh: function(frm) {

	// }
});

frappe.ui.form.on('Overtime Application', {
	employee(frm,cdt,cdn) {
		// your code here
		//console.log(frm.doc.applicant)
		frappe.model.set_value(cdt,cdn,"gross_salary","");
		if(frm.doc.employee){
		    frappe.call({
		        method:"hr_policies.custom_validate.get_hourly_rate",
		        args:{"employee":frm.doc.employee,"labour":frm.doc.is_labour,"staff":frm.doc.is_employee},
		        callback:function(r){
		            console.log(r.message);
		                frappe.model.set_value(cdt,cdn,"overtime_wages",r.message.per_day);
		        }
		    });
		}
	}
});
