// Copyright (c) 2020, Hardik gadesha and contributors
// For license information, please see license.txt

frappe.ui.form.on('Overtime Application', {
	// refresh: function(frm) {

	// }
});

frappe.ui.form.on('Overtime Application', {
        employee(frm) {
                if(frm.doc.employee){
                    frappe.call({
                        method:"hr_policies.custom_validate.get_hourly_rate",
                        args:{"employee":frm.doc.employee},
                        callback:function(r){
                                frm.set_value("overtime_wages",r.message.per_day);
                        }
                    });
                }
        }
});


frappe.ui.form.on("Overtime Application", {
  employee: function(frm) {
    frappe.call({
    "method": "hr_policies.hr_policies.doctype.overtime_application.overtime_application.getOT",
args: {
employee: frm.doc.employee,
request_date: frm.doc.request_date,
},
callback:function(r){
        frm.set_value("overtime_based_on_bio_metric_punch",r.message[0][0]);
	}
    });
}
});

frappe.ui.form.on("Overtime Application", {
  request_date: function(frm) {
    frappe.call({
    "method": "hr_policies.hr_policies.doctype.overtime_application.overtime_application.getOT",
args: {
employee: frm.doc.employee,
request_date: frm.doc.request_date,
},
callback:function(r){
        frm.set_value("overtime_based_on_bio_metric_punch",r.message[0][0]);
	}
    });
}
});
