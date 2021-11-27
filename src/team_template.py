TEMPLATE="""
{
  "sprint_days": {{ sprint_days }},
  "scrum_factor": {{ scrum_factor }},
  "capacity": {{ capacity }},
  "member_list": [
    {% for i in range %}
      {
        "name": "Member {{ i }}",
        "days_off": 0,
        "training_days": 0,
        "activity": 0
      }{{ "," if not loop.last else "" }}
    {% endfor %}
  ]
}
"""
