```
MATJOHN2-M-J0PL:1-Slide14 matjohn2$ cat myApp.py
#!/usr/bin/env python

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello Cisco LIVE! Cancun!"



if __name__ == "__main__":
    app.run(host='0.0.0.0')
```

```
MATJOHN2-M-J0PL:1-Slide14 matjohn2$ cat Dockerfile
FROM python
RUN mkdir /app
ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
ADD myApp.py /app/myApp.py
RUN chmod +x /app/myApp.py
CMD ["/app/myApp.py"]
```


```
MATJOHN2-M-J0PL:1-Slide14 matjohn2$ docker build .
Sending build context to Docker daemon  4.096kB
Step 1/7 : FROM python
 ---> a187104266fb
Step 2/7 : RUN mkdir /app
 ---> Using cache
 ---> e3f633276ec1
Step 3/7 : ADD requirements.txt /app/requirements.txt
 ---> Using cache
 ---> 1e804e53c100
Step 4/7 : RUN pip install -r /app/requirements.txt
 ---> Using cache
 ---> 0be9696652a0
Step 5/7 : ADD myApp.py /app/myApp.py
 ---> 207c55978425
Step 6/7 : RUN chmod +x /app/myApp.py
 ---> Running in f7831be45a69
Removing intermediate container f7831be45a69
 ---> 44074cbce379
Step 7/7 : CMD ["/app/myApp.py"]
 ---> Running in 70251b69e166
Removing intermediate container 70251b69e166
 ---> 11dc49a2816d
Successfully built 11dc49a2816d
```

```
MATJOHN2-M-J0PL:1-Slide14 matjohn2$ docker run -p5000:5000 11dc49a2816d
 * Serving Flask app "myApp" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

```
MATJOHN2-M-J0PL:~ matjohn2$ docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
4994ad4caf92        11dc49a2816d        "/app/myApp.py"     6 seconds ago       Up 4 seconds                            silly_aryabhata
```


