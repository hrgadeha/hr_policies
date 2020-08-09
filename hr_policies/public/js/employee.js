frappe.ui.form.on('Employee', {
        is_labour(frm) {
            if(frm.doc.is_labour){
                    frm.set_value("is_employee",0);
        }
        }
});

frappe.ui.form.on('Employee', {
        is_employee(frm) {
            if(frm.doc.is_employee){
                frm.set_value("is_labour",0);
        }
        }
});
