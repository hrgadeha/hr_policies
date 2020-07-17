// Copyright (c) 2020, Hardik gadesha and contributors
// For license information, please see license.txt

frappe.ui.form.on('Referral Bonus Application', {
	// refresh: function(frm) {

	// }
});

frappe.ui.form.on('Referral Bonus Application', {
	is_labour(frm) {
	    if(frm.doc.is_labour){
		    frm.set_value("is_employee",0);
	}
	}
});

frappe.ui.form.on('Referral Bonus Application', {
	is_employee(frm) {
	    if(frm.doc.is_employee){
	    	frm.set_value("is_labour",0);
	}
	}
});

frappe.ui.form.on('Referral Bonus Application', {
	refresh: function(frm) {
	    frappe.call({
    "method": "hr_policies.hr_policies.doctype.referral_bonus_application.referral_bonus_application.getPLS",
args: {
},
callback:function(r){
        console.log(r.message);
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
							${__("Referral Bouns Will Be Paid To You After "+r.message+" Months.")}
						</li>
						<li>
							${__("Referral Bouns Will Not Be Applicable if Employee Leave Company Before Bouns Hold Period.")}
						</li>
					</ul>
				</td></tr>
			</table>`;

		set_field_options("policies", help_content);
	}
    });

	}
});


