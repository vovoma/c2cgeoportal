# c2cgeoportal_admin

## Checkout

git clone git@github.com:camptocamp/c2cgeoportal.git
cd admin

## Create virtual environment

make install

## Set up the database

```
sudo -u postgres psql -c "CREATE USER \"www-data\" WITH PASSWORD 'www-data';"

DATABASE=c2cgeoportal
sudo -u postgres psql -c "CREATE DATABASE $DATABASE WITH OWNER \"www-data\";"
sudo -u postgres psql -d $DATABASE -c "CREATE EXTENSION postgis;"
```

Optionally update sqlachemy.url in development.ini

```
make init_db
```

## Run the tests

```
make test
```

## Run the application

```
make serve
```