#!/bin/bash

sudo docker login rg.fr-par.scw.cloud/djnd -u nologin -p $SCW_SECRET_TOKEN

# BUILD AND PUBLISH PRAVNA MREZA
sudo docker build -f glasljudstva/Dockerfile -t glas-ljudstva:latest ./glasljudstva
sudo docker tag glas-ljudstva:latest rg.fr-par.scw.cloud/djnd/glas-ljudstva:latest
sudo docker push rg.fr-par.scw.cloud/djnd/glas-ljudstva:latest
