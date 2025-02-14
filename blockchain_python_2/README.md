## This is block chain implementation with Fatsapi with graphQL
---
Take blocakchain reference from here.
[https://hackernoon.com/learn-blockchains-by-building-one-117428612f46](https://hackernoon.com/learn-blockchains-by-building-one-117428612f46)
#### Run Manually
1. Download this repo.
2. Run below commands to install dependencies.
```
pip install -r requirements.txt
```
3. Run below command to run this.
```
uvicorn main:app
```
4. You will see graphql swagger doce here.
[http://127.0.0.1:8000/graphql](http://127.0.0.1:8000/graphql)

---

#### Using Docker
1. Download this repo.
2. Run below commands to install dependencies to run it.
```
docker-compose up -d
```
4. You will see api swagger doce here.
[http://127.0.0.1:8000/graphql](http://127.0.0.1:8000/graphql)