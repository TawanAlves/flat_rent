# flat_rent

<p align="center">
  <a href="https://youtu.be/Jf5OK57SQWk" target="_blank">
    watch vídeo
  </a>
</p>

The project is a Django (CRUD) application that aims to record check-in and check-out dates related to a flat.
Basic constraints were added to date rules, such as preventing creation on past dates, check-out on a date before check-in, and overlapping bookings for the same flat on the same date. 
Additionally, an extra sorting feature was created to observe previous check-in and check-out dates. In a larger application, this sorting could be handled with a data structure like a linked list for performance. 
The project can be viewed at http://localhost:3000/flats. Moreover, for enhanced visual expansion, a simple and fake view was created at http://localhost:3000/ that does not pull information from the database. 
This route allows users to check available flats on selected check-in and check-out dates and sends a PDF with available flats to the email. 
The PDF creation and email sending are handled using Celery, allowing the task to run in the background. The PDF HTML only receives the flat IDs and, with basic logic, reflects the cards for each flat.

In future steps, I would add tests to the project, improve error and success message displays for users, refactor to reduce the number of repeated components and functions, address date and timezone issues on the frontend, and add email validation.

\_\_ To use Gmail for sending emails, it is necessary to have two-factor authentication and create an app password in Google App Passwords.

`pip freeze > requirements.txt` `pip install -r requirements.txt` `python3 manage.py runserver` at flat_rent

` npm i``npm run dev ` at frontend
