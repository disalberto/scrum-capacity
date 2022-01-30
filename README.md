[![Pylint](https://github.com/disalberto/scrum-capacity/actions/workflows/pylint.yml/badge.svg)](https://github.com/disalberto/scrum-capacity/actions/workflows/pylint.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![Stars of my repo](https://img.shields.io/github/stars/disalberto/scrum-capacity?style=social)
![Followers of my repos](https://img.shields.io/github/followers/disalberto?style=social)

# oRatio - The Capacity Calculator
***
## The need
This small software has been designed and developed to ease the activity of a ***Scrum Master***,
or anyone who has to deal with a team and its capacity.

<img src="images/Estimation.png" alt="Estimation" width="1000">

## Start Estimation
- For the first execution, it's mandatory to start a new estimation, that can be then reused as a base
for future iterations.

- The user is asked to specify **how many people are there in the team**.
Once confirmed, a table is shown with default pre-filled values.

- In the top left corner, the user has to select the base country of the team.
This will be used to retrieve the good bank-holidays.
  - *Current limitation*: if someone in the team is working in another country, a different bank-holiday
  must be treated as a day off.
- The user has to specify the start and end dates of the iteration for which the estimation is needed.
Sprint/Iteration days are automatically calculated, taking into account weekends and bank holidays.
  - The result can be manually forced to another value,
  in order to handle corner cases (i.e. company-specific day off or regional vacations).
- The **Scrum Factor in %** is the impact of SCRUM in your team: how much time in % is reserved
to Agile meetings (Daily Stand-up, Planning, Sprint Review,...).
  - It's by default set to 20%.
- For each team member, the user can specify:
  - A name
  - The number of days off
  - The number of days the member will be involved in trainings
  - The number of days the member will be involved in support/maintenance activity
  - The % of activity in the team:
    - For example a user could be DEV at 50% and Scrum Master for the remaining 50%.
    In this case his/her (dev) Activity would be 50%.
  - Notes/Comments, if needed.
- The capacity is automatically filled for each team member and the sum for all members is then reported in
the **Total Capacity** text area (top-right corner).
  - Its color can vary from red to green, depending on the underlying value:
    - Red: < 20 Story Points
    - Yellow: 20 SP < Capacity < 40 SP
    - Green: > 40 Story Points
- Once satisfied with the current estimation, the user can save the filled content with the dedicated button
in the bottom-left part of the UI.
  - The current date and the extension will be automatically appended to the chosen filename.

## Load JSON File
- An old estimation can be loaded to make adjustments or to be used as a base for a new one, to save some time.

## Wishlist for future releases
* Capacity with velocity integration
