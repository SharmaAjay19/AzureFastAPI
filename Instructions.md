## How to build the azurefastapi locally

In the top level parent directory, run the below command to build the base azurefastapi image:
```
docker build -t azurefastapi:1.0.0 .
```

## How to run an app with azurefastapi

Navigate to the example directory and run the docker build commands as below:
```
cd example
docker build -t azfastapisample .
docker rm -f azfastapisample
docker run -d --name azfastapisample -p 5001:80 azfastapisample
```

**Alternatively, you can run the buildrun.cmd script to build and run locally.**

## How to deploy the app to Azure Container Apps

### Step 1: Build and publish your docker image to Azure container registry

```
docker build -t azfastapiapps.azurecr.io/azfastapisample .
docker push azfastapiapps.azurecr.io/azfastapisample
```

### Step 2: 

Create a container app in Azure. Select the container image to the one published above.