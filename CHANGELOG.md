# Changelog

## 0.1.0

- Initial release

## 0.2.0

### Fixed
- Added support for Elliptic Curve (EC) private keys in certificate validation
- Improved private key type handling to support all certificate-compatible key types (RSA, EC, Ed25519, Ed448, DSA)
- Replaced instanceof checks with duck typing for better maintainability and future compatibility

### Changed
- Updated certificate validation logic to use `CertificateIssuerPrivateKeyTypes` from cryptography library

## 1.0.0

First tagged release. No functional change from 0.2.0.

### Added
- Installation instructions for `uv tool install`, pinned to a release tag

### Fixed
- `--version` reported `0.1.0` while the package version was `0.2.0`; both now
  report the same value

## 1.1.0

### Added
- `--context` / `-context` option on `list` and `patch` to select the kubeconfig
  context explicitly, with validation and an error listing the available
  contexts on a typo
- `patch` now prints the target context and cluster, and the full list of
  secrets it is about to overwrite, before asking for confirmation

### Changed
- `patch` discovers the target secrets *before* prompting. Previously the
  confirmation prompt showed only the certificate, so the operation was
  confirmed without knowing which secrets in which namespaces, or which
  cluster, would be modified
- `patch` exits early with a message when no secret matches, instead of
  prompting for a no-op
- Kubernetes clients are built with `config.new_client_from_config(context=...)`
  rather than `load_kube_config()` plus a bare `ApiClient()`, so the global
  default client configuration is no longer mutated

### Fixed
- `requires-python` declared `>= 3.8`, but the code uses PEP 604 unions
  (`str | None`) in a dataclass field annotation and a function signature, both
  evaluated at import time. Installing on 3.8/3.9 resolved cleanly and then
  raised `TypeError` on first run. Now declares `>=3.12`, matching the README
  and `.python-version`

## 1.2.0

### Fixed
- Cluster API errors were caught inside `find_secrets`, so they never reached
  the `@retry` decorator (which therefore never retried) and surfaced to the
  user as an empty result. An unreachable cluster or expired token rendered as
  "No secrets found that use the specified certificate" and exited 0
- `patch` reported success when the cluster call failed, so a certificate
  rotation against a cluster it could not reach silently did nothing and still
  exited 0
- Individual secrets that failed to patch were printed but not counted; a run
  where most patches failed still exited 0. Failures are now listed and exit 1
- A secret whose `tls.crt` was missing, empty, or unparseable raised and
  aborted the entire run. cert-manager creates such placeholder secrets before
  issuance, and they match the `type=kubernetes.io/tls` selector. They are now
  skipped by name and the run continues

### Changed
- `list` and `patch` exit 1 on cluster failures instead of 0
- Skipped secrets are reported by `namespace/name`, and `patch` warns about
  them before asking for confirmation, since an unreadable secret may be one
  that needed patching

