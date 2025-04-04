# MLOPS API Pipeline
This project is designed to make a series API endpoints that can be hit to document and manage every step of the mlops process

# Prerequisits
Deploy OpenShift Pipelines or Tekton

# Deploy
This can be deployed with ArgoCD using the applications in the argo folder

```
oc apply -n openshift-gitops -f argo/*.yaml
```

If not using argocd simply run these commands

```
oc apply -n demo -f python/flask-router/manifests/*.yaml
oc apply -n demo -f python/flask-router/manifests/routes/*.yaml
oc apply -n demo -f tekton/*/*.yaml
```

