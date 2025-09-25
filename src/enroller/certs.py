import enroller.data as data
import enroller.utils as utils
import typer
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.types import (
    CertificateIssuerPrivateKeyTypes,
)


class CertificateLoader:
    """
    Class to load certificates
    """

    def __init__(self, userdata: data.UserData) -> None:
        self.userdata = userdata

    def __validate_match(
        self, cert: x509.Certificate, private_key: CertificateIssuerPrivateKeyTypes
    ) -> None:
        """
        Validate if the certificate and key match.
        """

        try:
            public_key = private_key.public_key()
            if public_key.public_numbers() != cert.public_key().public_numbers():
                utils.console.print(
                    "Error: Private key does not match the certificate.",
                    style="bold red",
                )
                raise typer.Exit()
        except AttributeError:
            utils.console.print(
                f"Error: Unsupported private key type: {type(private_key).__name__}.",
                style="bold red",
            )
            raise typer.Exit()

    def __extract_cert_details(self, cert: x509.Certificate) -> data.Certificate:
        """
        Extract the certificate details.
        """

        # Get the domain names.
        try:
            san_extension = cert.extensions.get_extension_for_class(
                x509.SubjectAlternativeName
            )
            domain_names = san_extension.value.get_values_for_type(x509.DNSName)
        except x509.ExtensionNotFound:
            domain_names = []

        # Get the expiration date
        expiration_date = cert.not_valid_after_utc

        if self.userdata.verbose:
            utils.console.print("Subject Details:", style="bold")
            for domain in domain_names:
                utils.console.print(f"  - {domain}")

            utils.console.print(
                f"Expiration Date: {expiration_date.strftime('%Y-%m-%d %H:%M:%S')}"
            )

        return data.Certificate(domains=domain_names, expiration_date=expiration_date)

    def load_certificate_file(
        self, cert_path: str, key_path: str | None = None
    ) -> data.Certificate:
        """
        Load a certificate from a file.
        """

        with open(cert_path, "rb") as cert_file:
            cert_data = cert_file.read()
            cert = x509.load_pem_x509_certificate(cert_data, default_backend())

        if key_path:
            with open(key_path, "rb") as key_file:
                key_data = key_file.read()
                private_key = serialization.load_pem_private_key(
                    key_data,
                    password=None,  # ? no password for now.
                    backend=default_backend(),
                )

            self.__validate_match(cert, private_key)

        return self.__extract_cert_details(cert)

    def load_certificate_string(self, cert_data: bytes) -> data.Certificate:
        """
        Load a certificate from a PEM-encoded string.
        """

        cert = x509.load_pem_x509_certificate(cert_data, default_backend())
        return self.__extract_cert_details(cert)
