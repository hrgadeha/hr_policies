// Copyright (c) 2020, Hardik gadesha and contributors
// For license information, please see license.txt

frappe.ui.form.on('Miss Punch Application', {
	// refresh: function(frm) {

	// }
});

frappe.ui.form.on("Miss Punch Application", {
  "miss_punch_date": function(frm) {
	if(frm.doc.miss_punch_date && frm.doc.employee && frm.doc.application_type == "Miss Punch"){
    frappe.call({
    "method": "hr_policies.hr_policies.doctype.miss_punch_application.miss_punch_application.getattendance",
args: {
employee: frm.doc.employee,
attendance_date: frm.doc.miss_punch_date
},
callback:function(r){
	var len=r.message.length;
	    if(!r.message){
	        frm.set_value("last_punch_time","");
	        frm.set_value("attendance","");
	        frappe.throw("No Miss Punch Found On Selected Date, Please Select Valid Date");
	    }
	    else{
	        frm.set_value("last_punch_time",r.message[0][1]);
	        frm.set_value("attendance",r.message[0][0]);
	    }
	}
    });

	}
	}
});


frappe.ui.form.on("Miss Punch Application", {
  "miss_punch_date": function(frm) {
	if(frm.doc.miss_punch_date && frm.doc.employee && frm.doc.application_type == "Miss Punch"){
    frappe.call({
    "method": "hr_policies.hr_policies.doctype.miss_punch_application.miss_punch_application.getlapp",
args: {
employee: frm.doc.employee,
attendance_date: frm.doc.miss_punch_date
},
callback:function(r){
	var len=r.message.length;
	    if(!r.message){
	        frm.set_value("leave_application","");
	        frappe.throw("No Miss Punch Found On Selected Date, Please Select Valid Date");
	    }
	    else{
	        frm.set_value("leave_application",r.message[0][0]);
	    }
	}
    });
}
}
});

frappe.ui.form.on("Miss Punch Application", {
  "employee": function(frm) {
	if(frm.doc.miss_punch_date && frm.doc.employee && frm.doc.application_type == "Miss Punch"){
    frappe.call({
    "method": "hr_policies.hr_policies.doctype.miss_punch_application.miss_punch_application.getattendance",
args: {
employee: frm.doc.employee,
attendance_date: frm.doc.miss_punch_date
},
callback:function(r){
	var len=r.message.length;
	    if(!r.message){
	        frm.set_value("last_punch_time","");
	        frm.set_value("attendance","");
	        frappe.throw("No Miss Punch Found On Selected Date, Please Select Valid Date");
	    }
	    else{
	        frm.set_value("last_punch_time",r.message[0][1]);
	        frm.set_value("attendance",r.message[0][0]);
	    }
	}
    });

	}
	}
});


frappe.ui.form.on("Miss Punch Application", {
  "employee": function(frm) {
	if(frm.doc.miss_punch_date && frm.doc.employee && frm.doc.application_type == "Miss Punch"){
    frappe.call({
    "method": "hr_policies.hr_policies.doctype.miss_punch_application.miss_punch_application.getlapp",
args: {
employee: frm.doc.employee,
attendance_date: frm.doc.miss_punch_date
},
callback:function(r){
	var len=r.message.length;
	    if(!r.message){
	        frm.set_value("leave_application","");
	        frappe.throw("No Miss Punch Found On Selected Date, Please Select Valid Date");
	    }
	    else{
	        frm.set_value("leave_application",r.message[0][0]);
	    }
	}
    });
}
}
});


frappe.ui.form.on('Miss Punch Application',  'validate',  function(frm) {
	if(frm.doc.application_type == "Miss Punch"){
		if (!frm.doc.attendance || !frm.doc.leave_application) {
		        frappe.throw("No Miss Punch Found On Selected Date, Please Select Valid Date");
		        validated = false;
    		}
	}
	if (frm.doc.exit_time < frm.doc.last_punch_time) {
                        frappe.throw("Check out time should be greater than check in time");
                        validated = false;
                }
});


frappe.ui.form.on('Miss Punch Application',  'exit_time',  function(frm) {
                if (frm.doc.exit_time < frm.doc.last_punch_time) {
                        frappe.throw("Check out time should be greater than check in time");
                }
});
