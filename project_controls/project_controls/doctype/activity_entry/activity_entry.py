# -*- coding: utf-8 -*-
# Copyright (c) 2020, pibico and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import json
import datetime

class ActivityEntry(Document):
  def on_update(self):
    ## If time_log is empty create new timesheet
    if not self.time_log:
      create_timesheet(self)
    else:
      timesheet = frappe.get_doc("Timesheet", self.time_log)
      if not self.index:
        ## Create new child
        time_logs = {
          "activity_type": self.activity_type,
          "project": self.project,
          "task": self.task,
          "from_time": self.from_time,
          "item_code": self.item_code
        }
        timesheet.append("time_logs", time_logs)
        if self.notes:
          timesheet.note = timesheet.note + " | " + datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S") + " " + self.notes
        timesheet.save()
        frappe.db.commit()
      else:
        tarea = '' 
        ## Update existing child row
        for row in timesheet.get('time_logs'):
          if not row.to_time:
            row.to_time =  datetime.datetime.strptime(self.to_time, "%Y-%m-%d %H:%M:%S")
            row.save()
            tarea = row.task
        if tarea not in [self.task, '']:
          ## Create new child
          time_logs = {
            "activity_type": self.activity_type,
            "project": self.project,
            "task": self.task,
            "from_time": self.from_time,
            "item_code": self.item_code
          }
          timesheet.append("time_logs", time_logs)
          timesheet.save()
          frappe.db.commit()
        if self.notes:
          timesheet.note = timesheet.note + " | " + datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S") + " " + self.notes
          timesheet.save()
          frappe.db.commit()

def create_timesheet(doc):
  ## Create new timesheet
  time_logs = [{
    "activity_type": doc.activity_type,
    "project": doc.project,
    "task": doc.task,
    "from_time": doc.from_time,
    "item_code": doc.item_code
  }]
  note = ''
  if doc.notes:
    note = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S") + " " + doc.notes
    
  timesheet = frappe.get_doc({
    "doctype": "Timesheet",
    "company": doc.company,
    "employee": doc.employee,
    "time_logs": time_logs,
    "note": note
	})
  timesheet.insert()
