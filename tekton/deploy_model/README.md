In order to push to the git repo, we added a secret that does not appear in the repo for security reasons in this way:

```
oc create secret generic github-pat-demo --from-literal username=<your-git-username> --from-literal password=<your-git-access-token> --type kubernetes.io/basic-auth
oc annotate secret github-pat-demo "tekton.dev/git-0=https://github.com" ###Since our repo is on github, replace with your repo of choice
oc patch serviceaccount <pipelines-sa> -p '{"secrets": [{"name": "github-pat-demo"}]}'
```
