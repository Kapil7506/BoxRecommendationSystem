Collecting django                                        
  Using cached django-6.1.3-py3-none-any.whl.metadata (3.9 kB)
Collecting djangorestframework
  Using cached djangorestframework-3.18.3-py3-none-any.whl.metadata (7.8 kB)
Collecting asgiref>=3.9.1 (from django)
  Using cached asgiref-3.13.0-py3-none-any.whl.metadata (12 kB)
Collecting sqlparse>=0.5.0 (from django)
  Using cached sqlparse-0.6.1-py3-none-any.whl.metadata (6.9 kB)
Collecting tzdata (from django)
  Using cached tzdata-2026.6-py2.py3-none-any.whl.metadata (1.4 kB)
Using cached django-6.1.3-py3-none-any.whl (8.4 MB)
Using cached djangorestframework-3.18.3-py3-none-any.whl (903 kB)
Using cached asgiref-3.13.0-py3-none-any.whl (27 kB)
Using cached sqlparse-0.6.1-py3-none-any.whl (51 kB)
Using cached tzdata-2026.6-py2.py3-none-any.whl (348 kB)
Installing collected packages: tzdata, sqlparse, asgiref, django, djangorestframework
Successfully installed asgiref-3.13.0 django-6.1.3 djangorestframework-3.18.3 sqlparse-0.6.1 tzdata-2026.6
(boxvenv) PS D:\BoxRecommendationService\warehouse_project> python manage.py createsuperuser           
Username: kapil
Error: That username is already taken.
Username: kapil12
Email address:                        
Password: 
Password (again): 
The password is too similar to the username.
This password is too short. It must contain at least 8 characters.
Bypass password validation and create user anyway? [y/N]: y
Superuser created successfully.

----All modules test I have done its running----

----Github repo creation-----
(boxvenv) PS D:\BoxRecommendationService> git init                         
Initialized empty Git repository in D:/BoxRecommendationService/.git/
(boxvenv) PS D:\BoxRecommendationService>  git add .
(boxvenv) PS D:\BoxRecommendationSystem> git commit -m "Initial commit: Django shipping  box recommendation system"
[main (root-commit) d0e98fd] Initial commit: Django shipping  box recommendation system
 22 files changed, 893 insertions(+)
 create mode 100644 AI_USAGE.md
 create mode 100644 Boxrecommendationcheck.md
 create mode 100644 Test_output.md
 create mode 100644 requirement.txt
 create mode 100644 warehouse_project/.gitignore
 create mode 100644 warehouse_project/manage.py
 create mode 100644 warehouse_project/packing/__init__.py
 create mode 100644 warehouse_project/packing/admin.py
 create mode 100644 warehouse_project/packing/apps.py
 create mode 100644 warehouse_project/packing/migrations/0001_initial.py
 create mode 100644 warehouse_project/packing/migrations/__init__.py
 create mode 100644 warehouse_project/packing/models.py
 create mode 100644 warehouse_project/packing/serializers.py
 create mode 100644 warehouse_project/packing/services.py
 create mode 100644 warehouse_project/packing/tests.py
 create mode 100644 warehouse_project/packing/views.py
 create mode 100644 warehouse_project/warehouse_project/README.md
 create mode 100644 warehouse_project/warehouse_project/__init__.py
 create mode 100644 warehouse_project/warehouse_project/asgi.py
 create mode 100644 warehouse_project/warehouse_project/settings.py
 create mode 100644 warehouse_project/warehouse_project/urls.py
 create mode 100644 warehouse_project/warehouse_project/wsgi.py
(boxvenv) PS D:\BoxRecommendationSystem> git push -u origin main
fatal: 'origin' does not appear to be a git repository
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.
(boxvenv) PS D:\BoxRecommendationSystem> git branch -M main                                                      
(boxvenv) PS D:\BoxRecommendationSystem> git remote add origin https://github.com/Kapil7506/BoxRecommendationSystem.git
(boxvenv) PS D:\BoxRecommendationSystem> git push -u origin main                                                 
Enumerating objects: 26, done.
Counting objects: 100% (26/26), done.
Delta compression using up to 16 threads
Compressing objects: 100% (24/24), done.
Writing objects: 100% (26/26), 12.13 KiB | 1.52 MiB/s, done.
Total 26 (delta 1), reused 0 (delta 0), pack-reused 0 (from 0)
To https://github.com/Kapil7506/BoxRecommendationSystem.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
 
-------CRUD OPERATIONS---------
[16/Nov/2026 23:55:41] "GET /products/ HTTP/1.1" 200 10562
[16/Nov/2026 23:56:43] "POST /products/ HTTP/1.1" 201 10295
Not Found: /box/
[16/Nov/2026 23:56:57] "GET /box/ HTTP/1.1" 404 3208
[16/Nov/2026 23:57:05] "GET /boxes/ HTTP/1.1" 200 11158
Not Found: /
[16/Nov/2026 23:57:21] "GET / HTTP/1.1" 404 3178
[16/Nov/2026 23:57:55] "GET /orders/ HTTP/1.1" 200 11061
[16/Nov/2026 23:59:21] "GET /boxes/ HTTP/1.1" 200 11158
Not Found: /orders/1/recommend-box/
[17/Nov/2026 00:02:03] "GET /orders/1/recommend-box/ HTTP/1.1" 404 3265
[17/Nov/2026 00:02:14] "GET /orders/1 HTTP/1.1" 301 0
[17/Nov/2026 00:02:14] "GET /orders/1/ HTTP/1.1" 200 12107
[17/Nov/2026 00:02:51] "GET /orders/1/ HTTP/1.1" 200 12107
[17/Nov/2026 00:02:55] "GET /orders/1/ HTTP/1.1" 200 12107
Bad Request: /orders/1/
[17/Nov/2026 00:03:00] "PUT /orders/1/ HTTP/1.1" 400 11294
[17/Nov/2026 00:03:40] "GET /products/1/ HTTP/1.1" 200 11554
[17/Nov/2026 00:03:52] "PUT /products/1/ HTTP/1.1" 200 11554
[17/Nov/2026 00:04:03] "PUT /products/1/ HTTP/1.1" 200 11554
[17/Nov/2026 00:07:57] "OPTIONS /products/1/ HTTP/1.1" 200 13744
[17/Nov/2026 00:11:40] "DELETE /products/1/ HTTP/1.1" 200 11260
