# kubectl-enroller

A kubectl plugin that allows you to manage certificates in Kubernetes.

## Requirements

- Python 3.12.6 or later
- [uv](https://docs.astral.sh/uv/) or pipx

## Installation

### uv

```sh
uv tool install --python 3.12 git+https://github.com/User-Piotr/kubectl-enroller
uv tool update-shell
kubectl enroller --help
```

### pipx

```sh
pipx install git+https://github.com/User-Piotr/kubectl-enroller
```

Either method installs the plugin and makes it available as `kubectl enroller`.

## Usage

`kubectl enroller` - compares a local certificate with all secrets across multiple namespaces in the cluster. If a matching certificate is found, it updates the secret with the new certificate.

---

![CLI](img/kubectl-enroller.png "kubectl enroller")

For example, with a certificate that already exists in the cluster across multiple namespaces, the plugin will update the corresponding secrets with the new certificate.

![Example](img/kubectl-enroller-list-patch.png "kubectl enroller - patching certificate")
