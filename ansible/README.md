## K3s via Ansible

You can run the ansible setup tasks with:

```bash
$ ansible-playbook ansible/bootstrap/main.yaml -i ansible/private_inventory.yaml
```

You can ssh into the machine with (note the IP outputted by Pulumi):

```bash
$ ssh -i ./ssh_keys/id_rsa ubuntu@{IP_ADDRESS}
```

You can also download the kubeconfig file from the machine with:

```bash
$ scp -i ./ssh_keys/id_rsa ubuntu@{IP_ADDRESS}:~/.kube/config kubeconfig
```

You just need to change the server name in the downloaded file to be the nip IO hostname:

```diff
-server: https://127.0.0.1:6443
+server: https://{IP_ADDRESS}.nip.io:6443
```

Then you can run commands locally to get the state of the cluster:

```bash
$ export KUBECONFIG=kubeconfig
$ kubectl get pod bla -n whoami
$ kubectl describe pod bla -n whoami
```

### Other applications

In the apps folder are some additional apps you can install in the cluster. You can run them on a per-file basis, e.g.:

```bash
$ ansible-playbook ansible/apps/install-whoami.yaml -i ansible/private_inventory.yaml
```

Most of the applications are installed as helm charts. Here are some helpful helm commands:

```bash
$ helm list -n monitoring
$ helm get values grafana -n monitoring
```
