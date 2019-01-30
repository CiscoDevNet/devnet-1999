FROM python
RUN mkdir /app
ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
ADD myApp.py /app/myApp.py
RUN chmod +x /app/myApp.py
EXPOSE 5000
CMD ["/app/myApp.py"]

