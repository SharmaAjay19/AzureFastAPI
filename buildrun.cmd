docker build -t azurefastapi:1.0.0 .
cd example
docker build -t azfastapisample .
docker rm -f azfastapisample
docker run -d --name azfastapisample -p 5001:80 azfastapisample
cd ..