# Kubectl
Now that k3s is running on the cluster we want to be able to control the cluster. This is done using `kubectl`. First we need to copy the kube config file from the master node to our device:
```bash
scp hypriot@master.local:~/.kube/config ~/Documents/Cluster/.kube/blade-config
```

Next install kubectl using `homebrew`:
```bash
brew install kubectl
```

To verify the k3s install across all nodes run the kubectl test on our client config file:
```bash
 % export KUBECONFIG=~/Documents/Cluster/.kube/blade-config
 % kubectl version
```
This command should identify a client and a server :
```
Client Version: version.Info{Major:"1", Minor:"19", GitVersion:"v1.19.2", GitCommit:"f5743093fd1c663cb0cbc89748f730662345d44d", GitTreeState:"clean", BuildDate:"2020-09-16T21:51:49Z", GoVersion:"go1.15.2", Compiler:"gc", Platform:"darwin/amd64"}
Server Version: version.Info{Major:"1", Minor:"17", GitVersion:"v1.17.5+k3s1", GitCommit:"58ebdb2a2ec5318ca40649eb7bd31679cb679f71", GitTreeState:"clean", BuildDate:"2020-05-06T23:42:31Z", GoVersion:"go1.13.8", Compiler:"gc", Platform:"linux/arm"}
```

Now you can check the status of the cluster by running:
```bash
 % kubectl get nodes
NAME      STATUS   ROLES    AGE    VERSION
master    Ready    master   15h    v1.17.5+k3s1
slave-2   Ready    <none>   131m   v1.17.5+k3s1
slave-3   Ready    <none>   131m   v1.17.5+k3s1
slave-1   Ready    <none>   131m   v1.17.5+k3s1
```