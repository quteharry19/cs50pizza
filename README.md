# CS50w Project 3 Pizza

Web Programming with Python and JavaScript

A web application for a pizza restaurant name Pinochio's Pizza.

web app hosted at https://cs50pizza.herokuapp.com

Completed all projects requirements as below:

- Registration, Login, Logout - completed using django's built in user authentication system.
- Additing Items - completed using django admin interface by using localhost:8000/admin route.
- Menu - updated all the menu items to the database as given under http://www.pinocchiospizza.net/menu.html
- Shopping Cart - goto menu from navbar or click view menu button to see the complete menu with appropriate topping select options and select subsextra for Subs in the menu. I had used browsers localstorage to store the cart Items selected by user.
- Placing Order - completed this using bootstarp modal and javascript alerts which also prevents form submission if the cart is empty
- Viewing Order - once logged in click on you name to see the dropdown option, click on your orders to see the order status
- Personal Touch -
1.  Email confirmation with order details and total will be mailed with the link to track the order status.
2.  if logged in as superuser, superuser can update the status of order from pending to Complete or delivered.
3.  user can reset the login password by clicking forgot password or clicking reset password after login

- Special pizza is pizza with any number of toppings which are available

Details of some files and tricks utilized.

- orders/templatetag/setvar.py - used to get the number of toppings to be allowed from the 1st charater of the product name, which will be any number of toppings available for special, 0 for cheese and 0 if first charater of product name is not numeric

- orders/sendEmail.py - contains a functions to generate mail from template name and send mail which returns the number of mail sent.

- Procfile - used to run gunicorrn web server on heroku

- run_waitress_server.py - used to run web server on azure

- signals.py - used to control the toppings allowed when order saved from Django admin interface
