$name = "graggle-backend-service"
$version = "0.1.25"
$subscriptionIdProd = "364b7112-d791-4caa-99c9-9333f961b2a3"
$subscriptionIdDev = "205fa633-bf76-4fac-8cd1-3b60d08aa6df"

az account set --subscription $subscriptionIdProd
docker build -t acrsaasaiprod.azurecr.io/ai/ord/dg/$name`:$version .
az acr login -n acrsaasaiprod
docker push acrsaasaiprod.azurecr.io/ai/ord/dg/$name`:$version

#az account set --subscription $subscriptionIdDev
#az acr login -n acrsaasaidev
#docker build -t acrsaasaidev.azurecr.io/ai/ord/dg/$name`:$version .
# docker run -p 8102:8101 acrsaasaidev.azurecr.io/ai/ord/dg/$name`:$version
