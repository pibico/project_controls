# -*- coding: utf-8 -*-
# Copyright (c) 2020, PibiCo and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

@frappe.whitelist()
def get_commit(project):
  """ Get from database all committments amounts from not cancelled Purchase Orders
  on specific Project
  """
  data = frappe.db.sql("""
		SELECT item_code, item_name, parent, parenttype, docstatus, sum(qty) as Qty, sum(net_amount) as Amount FROM `tabPurchase Order Item` WHERE  project=%s and docstatus<2 GROUP by item_code""", project, True)
  return data

@frappe.whitelist()
def get_time(project):
  """ Get from database all hours from not cancelled Timesheets on specific Project """
  data = frappe.db.sql("""
     SELECT name, docstatus, parent, parenttype, sum(hours) as Hours, project, task, activity_type, item_code, sum(costing_amount) as Costs from `tabTimesheet Detail` WHERE project=%s and docstatus<2 GROUP by item_code""", project, True)
  return data

@frappe.whitelist()
def get_assignment(employee):
  """ Get from database all non closed assignments to an employee """
  data = frappe.db.sql("""SELECT * from `tabAssignment Detail` WHERE parent=%s and docstatus<2 and to_time is NULL""", employee, True)
  return data
  
@frappe.whitelist()
def get_timelogs(timesheet):
  """ Get from database all time logs from draft Timesheet """
  data = frappe.db.sql("""SELECT * from `tabTimesheet Detail` WHERE parent=%s and docstatus<2""", timesheet, True)
  return data

@frappe.whitelist()
def get_emplid(user):
  """ Get from database employee id from user logged in """
  data = frappe.db.sql("""SELECT * from `tabEmployee` WHERE user_id=%s""", user, True)
  return data

from six import BytesIO
from docxtpl import DocxTemplate

def _fill_template(template, data):
    """
    Fill a word template with data.

    Makes use of BytesIO to write the resulting file to memory instead of disk.

    :param template:    path to docx file or file-like object
    :param data:    dict with keys and values
    """
    doc = DocxTemplate(template)
    doc.render(data)
    _file = BytesIO()
    doc.docx.save(_file)
    return _file

@frappe.whitelist()
def fill_and_attach_template(doctype, name, template):
    """
    Use a documents data to fill a docx template and attach the result.

    Reads a document and a template file, fills the template with data from the
    document and attaches the resulting file to the document.

    :param doctype"     data doctype
    :param name"        data name
    :param template"    name of the template file
    """
    data = frappe.get_doc(doctype, name)
    data_dict = data.as_dict()

    template_doc = frappe.get_doc("File", template)
    #frappe.msgprint(template_doc.get_full_path())
    
    template_path = template_doc.get_full_path()

    output_file = _fill_template(template_path, data_dict)
    output_doc = frappe.get_doc({
        "doctype": "File",
        "file_name": "-".join([name, template_doc.file_name]),
        "attached_to_doctype": doctype,
        "attached_to_name": name,
        "content": output_file.getvalue(),
    })
    output_doc.save()