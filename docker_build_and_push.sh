set -e

version=0.1
image_name=my-app-backend

echo "Pushing $image_name version $version"

docker login

docker build -t $image_name ./image