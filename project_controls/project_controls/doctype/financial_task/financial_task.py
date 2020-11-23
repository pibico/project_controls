# -*- coding: utf-8 -*-
# Copyright (c) 2020, PibiCo and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe.utils.nestedset import NestedSet

class FinancialTask(NestedSet):
  def autoname(self):
    """Set name as `financial_task_number` plus `financial_task_name`"""
    self.name = str(self.financial_task_number) + " " + str(self.financial_task_name)