# MLOPS API Pipeline
This project is designed to make a series API endpoints that can be hit to document and manage every step of the mlops process

# Deployment of Demos to minikube
This version is to allow the demo applications to be deployed to Kubernetes without any dependencies on Red Hat OpenShift. This was tested with minikube, but should work on any Kubernetes distribution. 

# Prerequisites
Kubernetes - If installing locally you can use minikube (https://minikube.sigs.k8s.io/docs/start/?arch=%2Flinux%2Fx86-64%2Fstable%2Fbinary+download) 

This is the tested configuration that minikube was started with
```
minikube start --cpus 4 --memory 8192
minikube addons enable ingress
minikube addons enable dashboard
```

Tekton must be installed
```
kubectl apply -f https://storage.googleapis.com/tekton-releases/operator/latest/release.yaml
kubectl apply -f https://raw.githubusercontent.com/tektoncd/operator/main/config/crs/kubernetes/config/all/operator_v1alpha1_config_cr.yaml
```

We'll create the demo and minio namespaces
```
kubectl create namespace demo
kubectl create namespace minio
```

Run these commands to deploy the demo artifacts
```
kubectl apply -f minio/minio.yaml -n minio
kubectl apply -f python/flask-router/manifests/ -n demo
kubectl apply -f python/flask-router/manifests/routes/ -n demo
kubectl apply -f tekton/build_model/ -n demo
kubectl apply -f tekton/deploy_model/ -n demo
kubectl apply -f tekton/promote_data_card/ -n demo
kubectl apply -f tekton/request_model_card/ -n demo
kubectl apply -f tekton/update-model-pull-location/ -n demo
kubectl apply -f tekton/upload_data_card_s3/ -n demo
```

To access an endpoint run the below example for minio:
Copy the ADDRESS 
```
kubectl get ingress -o wide -n minio
```
Copy the PORT
```
kubectl get service minio -n minio
```

If you're accessing the minio UI URL it would look something like below. Note that we're not using the default 9090:
100.100.10.10:31762

# TODO - Demo instructions