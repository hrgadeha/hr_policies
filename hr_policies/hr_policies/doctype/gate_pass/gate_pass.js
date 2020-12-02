// Copyright (c) 2020, Hardik gadesha and contributors
// For license information, please see license.txt

frappe.ui.form.on('Gate Pass', {
	// refresh: function(frm) {

	// }
});

frappe.ui.form.on('Gate Pass', {
	refresh: function(frm) {
	    frappe.call({
    "method": "hr_policies.hr_policies.doctype.gate_pass.gate_pass.getPLS",
args: {
},
callback:function(r){
//        console.log(r.message);
		var help_content =
			`<br><br>
			<table class="table table-bordered" style="background-color: #f9f9f9;">
				<tr><td>
					<h4>
						<i class="fa fa-hand-right"></i> 
						${__("Notes")}:
					</h4>
					<ul>
						<li>
							${__("Personal Gate Pass Limit Per Month is "+r.message[0]+".")}
						</li>
						<li>
							${__(" Per Gate Pass Time Limit is "+r.message[1]+" Minutes.")}
						</li>
					</ul>
				</td></tr>
			</table>`;

		set_field_options("policies", help_content);
	}
    });

	}
});


frappe.ui.form.on('Gate Pass', {
	from_time(frm) {
		if(frm.doc.from_time > frm.doc.to_time){
		    frappe.throw("To Time Can Not Be Less Then From Time");
		    frm.set_value("apply_for",0);
		}

		else{
		    var startTime = moment(frm.doc.from_time, "HH:mm:ss a");
            var endTime = moment(frm.doc.to_time, "HH:mm:ss a");
		    var duration = moment.duration(endTime.diff(startTime));
		    var hours = (endTime.diff(startTime, 'hours')) * 60;
		    var mins = moment.utc(moment(endTime, "HH:mm:ss").diff(moment(startTime, "HH:mm:ss"))).format("mm");
		    var total_min = parseInt(hours) + parseInt(mins);
		    frm.set_value("apply_for",total_min);
		    frm.set_value("apply_for",0);
		}
	}
});

frappe.ui.form.on('Gate Pass', {
	to_time(frm) {
		if(frm.doc.from_time > frm.doc.to_time){
		    frappe.throw("To Time Can Not Be Less Then From Time");
		}

		else{
		    var startTime = moment(frm.doc.from_time, "HH:mm:ss a");
            var endTime = moment(frm.doc.to_time, "HH:mm:ss a");
		    var duration = moment.duration(endTime.diff(startTime));
		    var hours = (endTime.diff(startTime, 'hours')) * 60;
		    var mins = moment.utc(moment(endTime, "HH:mm:ss").diff(moment(startTime, "HH:mm:ss"))).format("mm");
		    var total_min = parseInt(hours) + parseInt(mins);
            frm.set_value("apply_for",total_min);
		}
	}
});

frappe.ui.form.on('Gate Pass', {
        validate(frm) {
                if(frm.doc.from_time > frm.doc.to_time){
                    frappe.throw("To Time Can Not Be Less Then From Time");
			validated = false;
                }

                else{
                    var startTime = moment(frm.doc.from_time, "HH:mm:ss a");
	            var endTime = moment(frm.doc.to_time, "HH:mm:ss a");
                    var duration = moment.duration(endTime.diff(startTime));
                    var hours = (endTime.diff(startTime, 'hours')) * 60;
                    var mins = moment.utc(moment(endTime, "HH:mm:ss").diff(moment(startTime, "HH:mm:ss"))).format("mm");
                    var total_min = parseInt(hours) + parseInt(mins);
        		frm.set_value("apply_for",total_min);
                }
        }
});

frappe.ui.form.on('Gate Pass', {
	validate(frm) {
		if(frm.doc.from_time > frm.doc.to_time){
		    frappe.throw("To Time Can Not Be Less Then From Time");
		    validated = false;
		}
	}
});

frappe.ui.form.on('Gate Pass', {
	type(frm) {
		if(frm.doc.type == "Official"){
		    frm.set_df_property('apply_for',  'reqd', 0);
		}
		if(frm.doc.type == "Official"){
		    frm.set_df_property('Personal',  'reqd', 1);
		}
	}
});


frappe.ui.form.on('Gate Pass', {
        employee(frm) {
                if(frm.doc.employee){
                    frappe.call({
                        method:"hr_policies.custom_validate.get_hourly_rate",
                        args:{"employee":frm.doc.employee},
                        callback:function(r){
                                frm.set_value("hourly_rate",r.message.per_day);
                        }
                    });
                }
        }
});
