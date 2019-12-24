FROM python:3-alpine

COPY . /app

WORKDIR /app

#RUN pip install flask
RUN pip install -r requirements.txt

EXPOSE 5000

#1. set env 
ENV FLASK_APP index
ENV FLASK_ENV development
ENV FLASK_RUN_PORT 5000
ENV FLASK_DEBUG True

#2. run 
CMD python -m flask run --host=0.0.0.0

# docker build -t python/phutest1.
# docker run -d --rm --name my-py-test1 -p 5001:5000 -v $(pwd):/app python/test/flask
# docker logs -f my-py-test1

