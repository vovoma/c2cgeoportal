#!/bin/bash -ex

mkdir -p /tmp/travis/testgeomapfish

export SRID=21781 EXTENT=489246.36,78873.44,837119.76,296543.14
./docker-run --share /tmp/travis pcreate --scaffold=c2cgeoportal_create /tmp/travis/testgeomapfish \
    --ignore-conflicting-name --package-name testgeomapfish > /dev/null
./docker-run --share /tmp/travis pcreate --scaffold=c2cgeoportal_update /tmp/travis/testgeomapfish \
    --ignore-conflicting-name --package-name testgeomapfish > /dev/null # on create
./docker-run --share /tmp/travis pcreate --scaffold=tilecloud_chain /tmp/travis/testgeomapfish

# Copy files for travis build and tests
cp travis/build.mk /tmp/travis/testgeomapfish/travis.mk
cp travis/empty-vars.mk /tmp/travis/testgeomapfish/empty-vars.mk
cp travis/vars.yaml /tmp/travis/testgeomapfish/vars_travis.yaml
cp travis/docker-compose.yaml /tmp/travis/testgeomapfish/docker-compose.yaml.mako
cp --recursive travis /tmp/travis/testgeomapfish/travis
cd /tmp/travis/testgeomapfish

# Init Git repository
git config --global user.name "Travis"
git config --global user.email "travis@example.com"
git init
git add --all
git commit --quiet --message="Initial commit"
git remote add origin . # add a fake remote

# Minimal build
./docker-run make -f travis.mk \
    docker-compose-build.yaml \
    geoportal-docker mapserver-docker print-docker testdb-docker
# Wait DB
./docker-compose-run sleep 15
# Create default theme
./docker-compose-run create-demo-theme
