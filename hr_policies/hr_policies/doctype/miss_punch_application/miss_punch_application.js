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
	        frm.set_value("attendance","");
	        frappe.throw("No Miss Punch Found On Selected Date, Please Select Valid Date");
	    }
	    else{
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
	        frm.set_value("attendance","");
	        frappe.throw("No Miss Punch Found On Selected Date, Please Select Valid Date");
	    }
	    else{
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
		var in_time = frm.doc.last_punch_time;
		var out_time = frm.doc.exit_time;
		var hoursMinutes = in_time.toString().split(":");
                var hours = parseInt(hoursMinutes[0], 10);
                var minutes = hoursMinutes[1] ? parseInt(hoursMinutes[1], 10) : 0;
                var entry = hours + minutes / 60;

                var hoursMinutes1 = out_time.toString().split(":");
                var hours1 = parseInt(hoursMinutes1[0], 10);
                var minutes1 = hoursMinutes1[1] ? parseInt(hoursMinutes1[1], 10) : 0;
                var exit = hours1 + minutes1 / 60;
                if (exit < entry && frm.doc.shift_type == "Day Shift") {
                        frappe.throw("Check out time should be greater than check in time");
			validated = false;
                }
});


frappe.ui.form.on('Miss Punch Application',  'exit_time',  function(frm) {
	if(frm.doc.exit_time){
                frm.set_value("working_hours",0);
                frm.set_value("office_hours",0);
                var in_time = frm.doc.last_punch_time;
                var out_time = frm.doc.exit_time;
                var hoursMinutes = in_time.toString().split(":");
                var hours = parseInt(hoursMinutes[0], 10);
                var minutes = hoursMinutes[1] ? parseInt(hoursMinutes[1], 10) : 0;
                var entry = hours + minutes / 60;

                var hoursMinutes1 = out_time.toString().split(":");
                var hours1 = parseInt(hoursMinutes1[0], 10);
                var minutes1 = hoursMinutes1[1] ? parseInt(hoursMinutes1[1], 10) : 0;
                var exit = hours1 + minutes1 / 60;
                if (exit < entry && frm.doc.shift_type == "Day Shift") {
                        frappe.throw("Check out time should be greater than check in time");
                }
	}
});

frappe.ui.form.on('Miss Punch Application',  'last_punch_time',  function(frm) {
	if(frm.doc.last_punch_time){
                frm.set_value("working_hours",0);
                frm.set_value("office_hours",0);
                var in_time = frm.doc.last_punch_time;
                var out_time = frm.doc.exit_time;
                var hoursMinutes = in_time.toString().split(":");
                var hours = parseInt(hoursMinutes[0], 10);
                var minutes = hoursMinutes[1] ? parseInt(hoursMinutes[1], 10) : 0;
                var entry = hours + minutes / 60;

                var hoursMinutes1 = out_time.toString().split(":");
                var hours1 = parseInt(hoursMinutes1[0], 10);
                var minutes1 = hoursMinutes1[1] ? parseInt(hoursMinutes1[1], 10) : 0;
                var exit = hours1 + minutes1 / 60;
                if (exit < entry && frm.doc.shift_type == "Day Shift") {
                        frappe.throw("Check out time should be greater than check in time");
                }
	}
});

frappe.ui.form.on("Miss Punch Application", {
  "punch_type": function(frm) {
      if(frm.doc.shift_type == "Day Shift"){
        if(frm.doc.miss_punch_date && frm.doc.employee && frm.doc.application_type == "Miss Punch" && frm.doc.punch_type == "In"){
    frappe.call({
    "method": "hr_policies.hr_policies.doctype.miss_punch_application.miss_punch_application.getMaxpunch",
args: {
employee: frm.doc.employee,
attendance_date: frm.doc.miss_punch_date
},
callback:function(r){
            console.log(r.message);
            frm.set_value("exit_time",r.message[0][0]);
            frm.set_value("last_punch_time","00:00:00");
            frm.set_df_property('exit_time',  'read_only', 1);
            frm.set_df_property('last_punch_time',  'read_only', 0);
        }
    });
}
}
    if(frm.doc.shift_type == "Night Shift"){
        if(frm.doc.miss_punch_date && frm.doc.employee && frm.doc.application_type == "Miss Punch" && frm.doc.punch_type == "In"){
    frappe.call({
    "method": "hr_policies.hr_policies.doctype.miss_punch_application.miss_punch_application.getMaxpunch_Night",
args: {
employee: frm.doc.employee,
attendance_date: frm.doc.miss_punch_date
},
callback:function(r){
            console.log(r.message);
            frm.set_value("exit_time",r.message[0][0]);
            frm.set_value("last_punch_time","00:00:00");
            frm.set_df_property('exit_time',  'read_only', 1);
            frm.set_df_property('last_punch_time',  'read_only', 0);
        }
    });
}
}
}
});

frappe.ui.form.on("Miss Punch Application", {
  "punch_type": function(frm) {
        if(frm.doc.miss_punch_date && frm.doc.employee && frm.doc.application_type == "Miss Punch" && frm.doc.punch_type == "Out"){
    frappe.call({
    "method": "hr_policies.hr_policies.doctype.miss_punch_application.miss_punch_application.getMinpunch",
args: {
employee: frm.doc.employee,
attendance_date: frm.doc.miss_punch_date
},
callback:function(r){
            frm.set_value("last_punch_time",r.message[0][0]);
            frm.set_value("exit_time","00:00:00");
            frm.set_df_property('last_punch_time',  'read_only', 1);
            frm.set_df_property('exit_time',  'read_only', 0);
        }
    });
}
}
});


frappe.ui.form.on("Miss Punch Application", {
  "application_type": function(frm) {
        if(frm.doc.application_type == "Machine Off"){
            frm.set_df_property('last_punch_time',  'read_only', 0);
            frm.set_df_property('exit_time',  'read_only', 0);
            frm.set_df_property('punch_type',  'reqd', 0);
        }
        if(frm.doc.application_type == "Miss Punch"){
            frm.set_df_property('last_punch_time',  'read_only', 1);
            frm.set_df_property('exit_time',  'read_only', 1);
            frm.set_df_property('punch_type',  'reqd', 1);
        }
}
});

frappe.ui.form.on("Miss Punch Application", {
  "refresh": function(frm) {
        if(frm.doc.application_type == "Machine Off"){
            frm.set_df_property('last_punch_time',  'read_only', 0);
            frm.set_df_property('exit_time',  'read_only', 0);
            frm.set_df_property('punch_type',  'reqd', 0);
        }
        if(frm.doc.application_type == "Miss Punch"){
            frm.set_df_property('last_punch_time',  'read_only', 1);
            frm.set_df_property('exit_time',  'read_only', 1);
            frm.set_df_property('punch_type',  'reqd', 1);
        }
}
});


