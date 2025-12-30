### AWS EKS via Pulumi

TODO:

- Pulumi code to
  - [x] start an EKS cluster
  - run the whoami deployment there
  - create an ecr
  - build and upload a docker image to the ecr
  - run built and uploaded dockerimage

https://www.pulumi.com/docs/iac/clouds/aws/guides/eks/

```bash
$ pulumi up
$ pulumi stack output kubeconfig > kubeconfig.yml
$ KUBECONFIG=./kubeconfig.yml kubectl get nodes
```

Note: You'll need to pass `-C aws/ec2` if the current working directory is not the `aws/ec2` dir.
