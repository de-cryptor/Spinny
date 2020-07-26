## Basic API service for Box CRUD Operations

1. Get Authentication Token API - using username and password

curl --location --request POST 'http://127.0.0.1:8000/store/auth_login/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username":"store",
    "password":"admin@123"
}'

2. Box Creation API

curl --location --request POST 'http://127.0.0.1:8000/store/box_view/' \
--header 'authentication-token: 1nbnr7HAdNZDLq2zrdoapUj75peQm7UkxBfCqVB7w1faeRnHR9cMAqYeTi3KNtUh' \
--header 'Content-Type: application/json' \
--data-raw '{
    "length":4,
    "width":2,
    "height":5
}'

3. Box Listing API using Various filter

curl --location --request GET 'http://127.0.0.1:8000/store/box_view/?length__lt=1000&area__gt=10&volume__lt=100&created_by=store' \
--header 'authentication-token: 1nbnr7HAdNZDLq2zrdoapUj75peQm7UkxBfCqVB7w1faeRnHR9cMAqYeTi3KNtUh'

Filters 
a.length__lt
b.length__gt
c.width__lt
e.width__gt
f.height__lt
g.height__gt
h.created_by



4. Box Deletion API

curl --location --request DELETE 'http://127.0.0.1:8000/store/box_view/' \
--header 'authentication-token: 1nbnr7HAdNZDLq2zrdoapUj75peQm7UkxBfCqVB7w1faeRnHR9cMAqYeTi3KNtUh' \
--header 'Content-Type: application/json' \
--data-raw '{
    "id":4
}'

5. Box Updation API

curl --location --request PUT 'http://127.0.0.1:8000/store/box_view/' \
--header 'authentication-token: tLAfNXCdhJDaGuNgIzPdaZDRouLVHIt0iwFJ9jdlX2lCx1JbhKJU099iVhG0qTE2' \
--header 'Content-Type: application/json' \
--data-raw '{
    "id":5,
    "length":5,
    "width":2,
    "height":2,
    "username":"admin"
}'


