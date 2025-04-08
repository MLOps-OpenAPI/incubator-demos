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

## Deploying to a fresh Openshift cluster

1. Create a new branch in the repo.
2. Run a global find and replace for apps.cluster-4ghn9.4ghn9.sandbox2431.opentlc.com for whatever the equivalent in your cluster.  Do this for the entire repo in your branch.
3. Install openshift gitops on the cluster
4. Add the three apps in the `argo` subdirectory manually.  Replace the `HEAD` revision with whatever you branch is called.
5. Add the following minio buckets manually:
    1. data-bucket
    2. data-cards
    3. model-bucket
    4. model-cards
    5. request-models
6. You can import the [collection](postman/army-incubator.postman_collection.json) file in the `postman` directory.  The find and replace should hit those, endpoints as well, so it Should work as is.