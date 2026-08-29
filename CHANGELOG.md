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
