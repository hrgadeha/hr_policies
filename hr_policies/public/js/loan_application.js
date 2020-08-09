frappe.ui.form.on('Loan Application', {
	applicant(frm,cdt,cdn) {
		// your code here
		//console.log(frm.doc.applicant)
		frappe.model.set_value(cdt,cdn,"eligible_amount","");
		frappe.model.set_value(cdt,cdn,"gross_salary","");
		if(frm.doc.applicant){
		    frappe.call({
		        method:"hr_policies.custom_validate.validate_eligibility",
		        args:{"employee":frm.doc.applicant},
		        callback:function(r){
		            if(!r.message){
		                var msg = "Employee "+ frm.doc.applicant + " Not Eligible For Loan.";
		                frappe.model.set_value(cdt,cdn,"applicant","");
		                frappe.throw(__(msg));
		            }
		            else{
		                frappe.model.set_value(cdt,cdn,"eligible_amount",r.message.eligible_amount);
		                frappe.model.set_value(cdt,cdn,"gross_salary",r.message.gross_pay);
		                frappe.model.set_value(cdt,cdn,"repayment_periods",r.message.month);
		            }
		        }
		    });
		}   
	}
});

frappe.ui.form.on('Loan Guarantor', {
	employee(frm,cdt,cdn) {
		// your code here
		var doc = locals[cdt][cdn];
	//console.log(cur_frm.doc.gross_salary)
		if(cur_frm.doc.gross_salary){
		    if(doc.employee){
		        if(doc.employee == cur_frm.doc.applicant){
		            frappe.model.set_value(cdt,cdn,"employee","");
		            frappe.throw(__("Applicant And Guarantor Must Be Different"));
		        }
		        frappe.call({
		            method:"hr_policies.custom_validate.get_guarantor_salary",
		            args:{"employee":doc.employee,"name":cur_frm.doc.name},
		            callback:function(r){
		             //   console.log(r.message)
		                if(r.message){
		                    if(parseFloat(cur_frm.doc.gross_salary)>parseFloat(r.message)){
		                        frappe.model.set_value(cdt,cdn,"employee","");
		                        frappe.model.set_value(cdt,cdn,"employee_name","");
		                        frappe.model.set_value(cdt,cdn,"status","");
		                        frappe.throw(__("Gross Salary of Guarantor Greater Than or Equal To Applicant Salary"));
		                    }
		                    
		                }
		                else{
		                     frappe.model.set_value(cdt,cdn,"employee","");
			                        frappe.model.set_value(cdt,cdn,"employee_name","");
		                        frappe.model.set_value(cdt,cdn,"status","");
		                }
		            }
		        });
		    }
		} 
		else{
		    frappe.throw(__("Loan Applicant Gross Salary Not Available. Select Applicant Again And Try Again"));
		}
	}
});

frappe.ui.form.on('Loan Application', {
	refresh: function(frm) {
	    frappe.call({
    "method": "hr_policies.custom_validate.getPLS",
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
							${__("You Are Eligible For Loan After You Complete "+r.message[0]+" Months In Company.")}
						</li>
						<li>
							${__("Standard Loan Repayment Period Is "+r.message[1]+" Months.")}
						</li>
						<li>
							${__("You Must Have "+r.message[2]+" Guarantor to Apply For Loan.")}
						</li>
						<li>
							${__("Eligible Loan Amount is Equal To Sum of Your Last "+r.message[3]+" Gross Salary.")}
						</li>
						<li>
							${__("You Can Be Guarantor For Maximum "+r.message[4]+" Loan Application")}
						</li>
					</ul>
				</td></tr>
			</table>`;

		set_field_options("policies", help_content);
	}
    });

	}
});
