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
