# PalPay-API
Backend API for Pal-Pay Mobile App.



## Commands:
### Heroku:
To Upgrade Local:
   1) `python manage.py db migrate`
   2) `python manage.py db upgrade`
    


To Upgrade Staging:
    `heroku run python manage.py db upgrade --app friendpay-stage`

To Upgrade Production:
    `heroku run python manage.py db upgrade --app friendpay-pro`

