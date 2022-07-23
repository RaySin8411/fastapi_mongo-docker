# FastAPI + MongoDB

A simple starter for building RESTful APIs with FastAPI and MongoDB. 

## Dockerising

To build a docker image for this boilerplate, create a duplicate `.env` file but with name `env`. Next, build an image:

```console
docker build -t fastapi-mongo .
```

The command above builds an image that can be deployed. To run the image in a container:

```console
docker run --env-file env -d --name fastapi-mongo -p 80:80 fastapi-mongo:latest
```

## 參考網址
* [台北市建築管理工程處-雙語詞彙](https://dba.gov.taipei/cp.aspx?n=E8A756CFF2A5C236)