// Copyright (c) 2020, Hardik gadesha and contributors
// For license information, please see license.txt

frappe.ui.form.on('Change Loan Guarantor', {
	new_guarantor: function(frm,cdt,cdn) {
		if(!frm.doc.loan_application){
			frappe.model.set_value(cdt,cdn,"new_guarantor","")
			frappe.throw(__("Select Loan Application First"))
		}
		if(frm.doc.new_guarantor){
			frappe.call({
				method:"hr_policies.custom_validate.get_guarantor_salary",
				args:{"employee":frm.doc.new_guarantor,"name":frm.doc.loan_application},
				callback:function(r){
					console.log(r.message)
					if(r.message){
						if(parseFloat(frm.doc.gross_salary)>parseFloat(r.message)){
							frappe.model.set_value(cdt,cdn,"new_guarantor","");
							frappe.throw(__("Gross Salary of Guarantor Greater Than or Equal To Applicant Salary"))
						}
						
					}
					else{
						 frappe.model.set_value(cdt,cdn,"new_guarantor","");
					}
				}
			})
		}

	},
	old_guarantor: function(frm) {
		if(!frm.doc.loan_application){
			frappe.model.set_value(cdt,cdn,"old_guarantor","")
			frappe.throw(__("Select Loan Application First"))
		}
	},
});
