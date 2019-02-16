# FriendPay API
Backend API for FriendPay Mobile App.



## Commands:
### Heroku:
To Upgrade Local:
   1) `python manage.py db migrate`
   2) `python manage.py db upgrade`
    


To Upgrade Staging:
    `heoku run python manage.py db upgrade --app --friendpay-stage`

To Upgrade Production:
    `heoku run python manage.py db upgrade --app --friendpay-pro`

