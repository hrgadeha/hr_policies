// Copyright (c) 2020, Hardik gadesha and contributors
// For license information, please see license.txt

frappe.ui.form.on('Attendance Machine Settings', {
	// refresh: function(frm) {

	// }
});


frappe.ui.form.on('Attendance Machine Settings', {
	process_attendance_manually(frm) {
    frappe.call({
        "method": "hr_policies.attendance_integration.run_attendance_manually",
        args: {
            from_date: frm.doc.from_date,
            to_date: frm.doc.to_date
        },
        callback:function(r){
            msgprint("Attendance Generated For Date : "+frm.doc.from_date+" To " + frm.doc.to_date);
    }
});
}
});


