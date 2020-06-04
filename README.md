# python-test-
running test case
docker-compose run app sh -c "python manage.py test"

making new core module
docker-compose run app sh -c "python manage.py startapp core"

updating migration file
docker-compose run app sh -c "python manage.py makemigrations core"