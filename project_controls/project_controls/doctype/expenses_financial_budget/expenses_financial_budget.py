# -*- coding: utf-8 -*-
# Copyright (c) 2020, PibiCo and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class ExpensesFinancialBudget(Document):
  def autoname(self):
    """Set name `date` plus `financial_budget_code`"""
    ## self.name = get_datetime(self.posting_date).strftime("%y%m%d") + "_" + str(self.financial_budget_code)
    self.name = str(self.financial_budget_code) + "_" + str(self.financial_budget_name)

@frappe.whitelist()
def get_last_budget():
  """Returns last recorded budget to generate code.
  """
  ppto = '0000'
  budget = frappe.get_last_doc('Expenses Financial Budget')
  if budget:
    ppto = budget.financial_budget_code
    sqe = '%004d' % (int(ppto[-4:]) + 1)
  return sqe