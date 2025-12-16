### K3s via Ansible

You can run the ansible setup tasks with:

```bash
$ ansible-playbook ansible/main.yaml -i ansible/private_inventory.yaml
```

You can ssh into the machine with (note the IP outputted by Pulumi):

```bash
$ ssh -i ./ssh_keys/id_rsa ubuntu@{IP_ADDRESS}
```

On the machine, the following commands are helpful to check the k3s state:

```bash
$ kubectl get pod bla -n whoami
$ kubectl describe pod bla -n whoami
```
