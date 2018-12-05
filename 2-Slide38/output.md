```
MATJOHN2-M-J0PL:2-Slide38 matjohn2$ cat myApp.py
#!/usr/bin/env python

from flask import Flask,request

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello Cisco LIVE! Cancun!"

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

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
MATJOHN2-M-J0PL:2-Slide38 matjohn2$ docker run -p 5000:5000 467c638084e4
 * Serving Flask app "myApp" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)


172.17.0.1 - - [05/Dec/2018 18:48:49] "GET / HTTP/1.1" 200 -
172.17.0.1 - - [05/Dec/2018 18:48:54] "GET /shutdown HTTP/1.1" 200 -
```

```
MATJOHN2-M-J0PL:~ matjohn2$ docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS                    NAMES
8d3692735f26        467c638084e4        "/app/myApp.py"     6 seconds ago       Up 5 seconds        0.0.0.0:5000->5000/tcp   hardcore_brown
MATJOHN2-M-J0PL:~ matjohn2$ docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
MATJOHN2-M-J0PL:~ matjohn2$ docker ps
CONTAINER ID        IMAGE
```

Kubernetes `kubectl`

```
MATJOHN2-M-J0PL:2-Slide38 matjohn2$ kubectl get ns
NAME          STATUS    AGE
default       Active    68d
docker        Active    68d
kube-public   Active    68d
kube-system   Active    68d
MATJOHN2-M-J0PL:2-Slide38 matjohn2$ kubectl get services
NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   68d
MATJOHN2-M-J0PL:2-Slide38 matjohn2$ kubectl get po
No resources found.
```




Kubernetes needs to pull docker images from somewhere, our app is just on our machine. `docker push` to a public repository.

```
MATJOHN2-M-J0PL:2-Slide38 matjohn2$ docker push trxuk/latam-live-18-simple-server1:latest
The push refers to repository [docker.io/trxuk/latam-live-18-simple-server1]
7f7967cd5ac7: Pushed
2a3d516cea5a: Pushed
46d8f7ab6327: Pushing [======================================>            ]   7.27MB/9.387MB
fa889aab8a2b: Pushed
616d02dd048b: Pushed

```


Now define our pod:

```
MATJOHN2-M-J0PL:2-Slide38 matjohn2$ cat pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp
  labels:
     app: myapp
spec:
  containers:
  - name: myapp
    image: trxuk/latam-live-18-simple-server1:latest
```

And tell kubernetes to run it:

```
MATJOHN2-M-J0PL:2-Slide38 matjohn2$ kubectl create -f pod.yaml
pod "myapp" created
```

Check status:

```
MATJOHN2-M-J0PL:2-Slide38 matjohn2$ kubectl get po
NAME      READY     STATUS    RESTARTS   AGE
myapp     1/1       Running   0          16s
```

Get logs:

```
MATJOHN2-M-J0PL:2-Slide38 matjohn2$ kubectl logs myapp
 * Serving Flask app "myApp" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

Get more info about our pod, including *internal* IP:

```

MATJOHN2-M-J0PL:2-Slide38 matjohn2$ kubectl describe po myapp
Name:         myapp
Namespace:    default
Node:         docker-for-desktop/192.168.65.3
Start Time:   Wed, 05 Dec 2018 14:00:09 -0500
Labels:       <none>
Annotations:  <none>
Status:       Running
IP:           10.1.0.25

```

We can't get to the internal IP often, expose resources using SERVICES.

```
MATJOHN2-M-J0PL:2-Slide38 matjohn2$ curl http://10.1.0.25:5000
curl: (7) Failed to connect to 10.1.0.25 port 5000: Connection refused
```

Create a kubernetes `Service` object:

```
MATJOHN2-M-J0PL:2-Slide38 matjohn2$ cat service.yaml
kind: Service
apiVersion: v1
metadata:
  name: myapp-service
spec:
  type: NodePort
  selector:
    app: myapp
  ports:
  - protocol: TCP
    port: 5000
```

Deploy and check it exists:

```
MATJOHN2-M-J0PL:2-Slide38 matjohn2$ kubectl create -f service.yaml
service "myapp-service" created


MATJOHN2-M-J0PL:2-Slide38 matjohn2$ kubectl get services
NAME            TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
kubernetes      ClusterIP   10.96.0.1       <none>        443/TCP          68d
myapp-service   NodePort    10.99.181.192   <none>        5000:30470/TCP   5s
```

Test

```
MATJOHN2-M-J0PL:2-Slide38 matjohn2$ curl http://localhost:30470/
Hello Cisco LIVE! Cancun!
```


Kubernetes will restart the pod if it dies. Upto a point!

```
MATJOHN2-M-J0PL:2-Slide38 matjohn2$ kubectl get po
NAME      READY     STATUS    RESTARTS   AGE
myapp     1/1       Running   0          17m

MATJOHN2-M-J0PL:2-Slide38 matjohn2$ curl http://localhost:30470/shutdown
Server shutting down...


MATJOHN2-M-J0PL:2-Slide38 matjohn2$ kubectl get po
NAME      READY     STATUS    RESTARTS   AGE
myapp     1/1       Running   1          17m

MATJOHN2-M-J0PL:2-Slide38 matjohn2$ curl http://localhost:30470/shutdown
Server shutting down...


MATJOHN2-M-J0PL:2-Slide38 matjohn2$ kubectl get po
NAME      READY     STATUS    RESTARTS   AGE
myapp     1/1       Running   2          18m
```


# Deployments

```
MATJOHN2-M-J0PL:3-Slide43 matjohn2$ cat deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-deployment
  labels:
    app: myapp2
spec:
  replicas: 4
  selector:
    matchLabels:
      app: myapp2
  template:
    metadata:
      labels:
        app: myapp2
    spec:
      containers:
      - name: myapp2
        image: trxuk/latam-live-18-simple-server2:latest
        ports:
        - containerPort: 5000
```
```
MATJOHN2-M-J0PL:3-Slide43 matjohn2$ kubectl create -f deployment.yaml
deployment "app-deployment" created

MATJOHN2-M-J0PL:3-Slide43 matjohn2$
MATJOHN2-M-J0PL:3-Slide43 matjohn2$ kubectl get deployment
NAME             DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
app-deployment   4         4         4            1           4s


MATJOHN2-M-J0PL:3-Slide43 matjohn2$ kubectl get po
NAME                              READY     STATUS    RESTARTS   AGE
app-deployment-645c69fdb4-2pfg4   1/1       Running   0          8s
app-deployment-645c69fdb4-kvxtf   1/1       Running   0          8s
app-deployment-645c69fdb4-m2l2h   1/1       Running   0          8s
app-deployment-645c69fdb4-tzkv2   1/1       Running   0          8s
myapp                             1/1       Running   2          51m
```

```
MATJOHN2-M-J0PL:3-Slide43 matjohn2$ kubectl edit service myapp-service
service "myapp-service" edited
```
