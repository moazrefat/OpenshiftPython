## General Idea
A python/flask api application accepts requests on certain port number which is given as environment variable.

#### Building docker image
```bash
docker build -t hf . #hf refers to HelloFresh 
docker tag hf moazrefat/hello:hf 
docker push moazrefat/hello:hf
```

#### This project provides the following files:

|File	| Description| 
|--------------------------- | -----------------------------|
|deployment.yaml |	The definition file for your application| 
|Dockerfile |	Docker file denfination|
|requirements.txt |	The required modules for this api app|
|files |	Images for the app after the implemetation |
|.dockerignore |	Files not to be considered by docker |

## Implemetation 
#### Curl-ing api /config/burger-nutrition 
![api-configs.png](files/api-configs.png)
#### Results with postman 
![api-configs.png](files/api-configs-postman.png)
#### Curl-ing api /config/burger-nutrition 
![api-burger-nutrition.png](files/api-burger-nutrition.png)
#### Results with postman 
![api-burger-nutrition.png](files/api-burger-nutrition-postman.png)


#### Implement the app on kubernetes cluster
```bash
kubectl apply -f deployment.yaml
# or from any path 
find . -iname deployment.yaml | xargs kubectl apply -f
```

#### Generate traffic on different endpoints
```bash
# /configs
siege -c 10 -t 10m http://$(kubectl get svc hello -o jsonpath='{.status.loadBalancer.ingress[0].ip}'):8080/configs
while true; do curl -s http://$(kubectl get svc hello -o jsonpath='{.status.loadBalancer.ingress[0].ip}'):8080/configs && sleep 1 ; done
# /configs/burger-nutrition
siege -c 10 -t 10m http://$(kubectl get svc hello -o jsonpath='{.status.loadBalancer.ingress[0].ip}'):8080/configs/burger-nutrition
while true; do curl -s http://$(kubectl get svc hello -o jsonpath='{.status.loadBalancer.ingress[0].ip}'):8080/configs/burger-nutrition && sleep 1 ; done
```
#### Prometheus metrics API /metrics
```bash
curl -s http://$(kubectl get svc hello -o jsonpath='{.status.loadBalancer.ingress[0].ip}'):8080/metrics
```
#### Prometheus Metrics
![prometheus-metrics-sample.png](files/prometheus-metrics-sample.png)

#### Sample post request
```bash
export IP=$(kubectl get svc hello -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
curl -X POST -H "Content-Type: application/json" -d '{
    "name": "datacenter-3",
    "metadata": {
      "monitoring": {
        "enabled": "true"
      },
      "limits": {
        "cpu": {
          "enabled": "false",
          "value": "300m"
        }
      }
    }
  }' http://$IP:8080/configs
```
#### Sample delete request
```bash
curl -X DELETE http://localhost:8080/configs/datacenter-2
```
#### Output 
```text
Here datacenter-2 was deleted as shown in below output
[{"name":"datacenter-1","metadata":{"monitoring":{"enabled":"true"},"limits":{"cpu":{"enabled":"false","value":"300m"}}}}]
```
Delete request removed `datacenter-2` 
![api-delete-method.png](files/api-delete-method.png)


# Bonus
Below is my [Github repo](https://github.com/moazrefat/K8S-Bonus) where i did a practical hands-on step-by-step howto where i explained different deployments strategies 
#### Deployment Strategies:
1. Blue/Green deployments [here](https://github.com/moazrefat/K8S-Bonus/tree/master/istio)
2. Automated canary deployment using flagger [here](https://github.com/moazrefat/K8S-Bonus/tree/master/flagger)
3. Gitops approach [here](https://github.com/moazrefat/K8S-Bonus/tree/master/argocd)
4. Monitor k8s cluster and apps with prometheus + grafana [here](https://github.com/moazrefat/K8S-Bonus/tree/master/k8s-prometheus-grafana)
5. Use Terraform to build multi-regsion cluster on AWS cloud [here](https://github.com/moazrefat/K8S-Bonus/tree/master/aws-terraform-k8s)