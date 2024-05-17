$name = "graggle-backend-service"
$version = "0.2.1"
$subscriptionIdProd = "364b7112-d791-4caa-99c9-9333f961b2a3"
$subscriptionIdDev = "205fa633-bf76-4fac-8cd1-3b60d08aa6df"


# copy pip.ini into the current directory
$source = "$HOME\pip\pip.ini"
$destination = ".\pip.ini"
Copy-Item -Path $source -Destination $destination

# remove proxy and cert from pip.ini
$content = Get-Content -Path $destination
$updatedContent = $content | Where-Object { $_ -notmatch 'proxy' }
$updatedContent = $updatedContent | Where-Object { $_ -notmatch 'cert' }
$updatedContent | Set-Content -Path $destination

#az account set --subscription $subscriptionIdProd
#docker build -t acrsaasaiprod.azurecr.io/ai/ord/dg/$name`:$version -f containerization/Dockerfile .
#az acr login -n acrsaasaiprod
#docker push acrsaasaiprod.azurecr.io/ai/ord/dg/$name`:$version

az account set --subscription $subscriptionIdDev
az acr login -n acrsaasaidev
docker build -t acrsaasaidev.azurecr.io/ai/ord/dg/$name`:$version -f containerization/Dockerfile .
# docker run -p 8102:8101 acrsaasaidev.azurecr.io/ai/ord/dg/$name`:$version
docker push acrsaasaidev.azurecr.io/ai/ord/dg/$name`:$version


# delete the pip.ini
Remove-Item -Path $destination