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
  data = frappe.db.sql("""SELECT * from `tabAssignment Detail` WHERE parent=%s and docstatus<2 and to_time=null""", employee, True)
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