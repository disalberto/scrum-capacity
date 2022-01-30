"""Base template to load and save the estimations"""

TEMPLATE: str = """
{
  "date_from": "{{ date_from }}",
  "date_to": "{{ date_to }}",
  "sprint_days": {{ sprint_days }},
  "scrum_factor": {{ scrum_factor }},
  "capacity": {{ capacity }},
  "member_list": [
    {% for i in range %}
      {
        "name": "Member {{ i }}",
        "days_off": 0,
        "training_days": 0,
        "support_days": 0,
        "activity": 0,
        "capacity": 0,
        "notes": ""
      }{{ "," if not loop.last else "" }}
    {% endfor %}
  ]
}
"""
