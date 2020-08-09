frappe.ui.form.on('Employee Advance', {
	employee(frm,cdt,cdn) {
		// your code here
		if(frm.doc.employee){
		    	frappe.call({
		            method:"hr_policies.custom_validate.validate_employee_advance",
		            args:{"employee":frm.doc.employee,"date":frm.doc.posting_date},
		            callback:function(r){
		                console.log(r.message)
		                if(r.message){
		                    let percentage = 0
		                    let remain_percentage = 0
                			frappe.db.get_value("Advance Salary Policies", {"name":"Advance Salary Policies"}, "advance_applicable_percentage", (res) => {
                            console.log(res);
                            percentage = parseFloat(res.advance_applicable_percentage)/100
                            remain_percentage = (100 - parseFloat(res.advance_applicable_percentage))/100
		                    frappe.model.set_value(cdt,cdn,"eligible_advance_amount_",parseFloat(r.message[0])*percentage);
		                    frappe.model.set_value(cdt,cdn,"remain_amount_eligible",parseFloat(r.message[0])*remain_percentage);
		                    frappe.model.set_value(cdt,cdn,"emi_amount",r.message[1]);
                			});

		            }
		            else{
		                frappe.model.set_value(cdt,cdn,"employee","");
		                frappe.model.set_value(cdt,cdn,"employee_name","");
		                frappe.model.set_value(cdt,cdn,"eligible_advance_amount_","");
		                frappe.model.set_value(cdt,cdn,"remain_amount_eligible","");
		                frappe.model.set_value(cdt,cdn,"emi_amount","");
		            }
		            }

		        });
		}
	}
});
