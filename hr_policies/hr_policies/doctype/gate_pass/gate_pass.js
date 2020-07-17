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
