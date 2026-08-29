# kubectl-enroller

A kubectl plugin that allows you to manage certificates in Kubernetes.

## Requirements

- Python 3.12.6 or later
- [uv](https://docs.astral.sh/uv/) or pipx

## Installation

Both methods install from a tagged release. Replace `v1.1.0` with any tag from
the [releases page](https://github.com/User-Piotr/kubectl-enroller/releases), or
drop the `@v1.1.0` suffix to track the tip of `main`.

### uv

```sh
uv tool install --python 3.12 git+https://github.com/User-Piotr/kubectl-enroller@v1.1.0
uv tool update-shell
kubectl enroller --help
```

To move to a different release later:

```sh
uv tool install --force --python 3.12 git+https://github.com/User-Piotr/kubectl-enroller@v1.0.0
```

### pipx

```sh
pipx install git+https://github.com/User-Piotr/kubectl-enroller@v1.1.0
```

Either method installs the plugin and makes it available as `kubectl enroller`.

## Usage

`kubectl enroller` - compares a local certificate with all secrets across multiple namespaces in the cluster. If a matching certificate is found, it updates the secret with the new certificate.

---

![CLI](img/kubectl-enroller.png "kubectl enroller")

For example, with a certificate that already exists in the cluster across multiple namespaces, the plugin will update the corresponding secrets with the new certificate.

![Example](img/kubectl-enroller-list-patch.png "kubectl enroller - patching certificate")
