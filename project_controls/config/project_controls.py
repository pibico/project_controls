from __future__ import unicode_literals
from frappe import _

def get_data():
  return [
    {
      "label": _("Project Controls"),
      "icon": "fa fa-star",
      "items": [
        {
          "type": "doctype",
          "name": "Expenses Financial Budget",
          "description": _("Financial Budget"),
          "onboard": 1,
        },
        {
          "type": "doctype",
          "name": "Activity Entry",
          "description": _("Activity Entry"),
          "onboard": 1,
        }        
      ]
    },
    {
      "label": _("Project Controls Settings"),
      "icon": "fa fa-star",
      "items": [
        {
          "type": "doctype",
          "name": "Financial Task",
          "description": _("Cost Breakdown Structure"),
          "onboard": 1,
        }        
      ]
    }
  ]