## Basic API service for Box CRUD Operations

1. Get Authentication Token API - using username and password

<pre><code>
curl --location --request POST 'http://127.0.0.1:8000/store/auth_token/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username":"store",
    "password":"admin@123"
}'
</code></pre>

2. Box Creation API

<pre><code>
curl --location --request POST 'http://127.0.0.1:8000/store/box/create/' \
--header 'Authorization: Token 97b722f9af48b16f47e563bb69bd615e60fbeca8' \
--header 'Content-Type: application/json' \
--data-raw '{
    "length":4,
    "width":2,
    "height":5
}'
</code></pre>

3. Box Listing API using Various filter

<pre><code>
curl --location --request GET 'http://127.0.0.1:8000/store/box/list/?length__lt=1000&area__gt=10&volume__lt=100&created_by=store' \
--header 'Authorization: Token 97b722f9af48b16f47e563bb69bd615e60fbeca8'
</code></pre>

Filters 
1.length__lt
2.length__gt
3.width__lt
4.width__gt
5.height__lt
6.height__gt
7.created_by

4. Box Listing for specific user.
<pre><code>
curl --location --request GET 'http://127.0.0.1:8000/store/box/my_list/?length__lt=1000&area__gt=10&volume__lt=100&created_by=store' \
--header 'Authorization: Token 97b722f9af48b16f47e563bb69bd615e60fbeca8'
</code></pre>

Filters 
1.length__lt
2.length__gt
3.width__lt
4.width__gt
5.height__lt
6.height__gt

4. Box Deletion API

<pre><code>
curl --location --request GET 'http://127.0.0.1:8000/store/box/my_list/?length__lt=1000&area__gt=10&volume__lt=100&created_by=store' \
--header 'Authorization: Token 97b722f9af48b16f47e563bb69bd615e60fbeca8'
</code></pre>


5. Box Updation API

<pre><code>
curl --location --request DELETE 'http://127.0.0.1:8000/store/box/delete/5' \
--header 'Authorization: Token 97b722f9af48b16f47e563bb69bd615e60fbeca8'
</code></pre>


