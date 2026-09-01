import base64

import enroller.data as data
import enroller.utils as utils
import kubernetes.client
import typer
import urllib3
from enroller.certs import CertificateLoader
from kubernetes import config
from kubernetes.client.rest import ApiException
from retry import retry

# Errors that mean "the cluster call failed", as opposed to "nothing matched".
CLUSTER_ERRORS = (ApiException, urllib3.exceptions.MaxRetryError)


class KubernetesSecretOperator:
    """
    Class to manage Kubernetes secrets.
    """

    def __init__(
        self,
        cert: data.Certificate,
        userdata: data.UserData,
        context: str | None = None,
    ) -> None:
        self.cert = cert
        self.userdata = userdata

        self.kubernetes_certificates: list[data.Secrets] = []
        self.failed_patches: list[str] = []

        self.context, self.cluster = self.__resolve_context(context)
        self.api_client = config.new_client_from_config(context=self.context)
        self.v1 = kubernetes.client.CoreV1Api(self.api_client)

    @staticmethod
    def __resolve_context(context: str | None) -> tuple[str, str]:
        """
        Resolve the kubeconfig context to use. Returns (context, cluster).
        """

        try:
            contexts, active_context = config.list_kube_config_contexts()
        except config.ConfigException as error:
            utils.console.print(
                f"Error reading kubeconfig: {error}", style="bold red"
            )
            raise typer.Exit(code=1)

        available = {entry["name"]: entry for entry in contexts}

        if context is None:
            selected = active_context
        elif context in available:
            selected = available[context]
        else:
            utils.console.print(
                f"Error: context '{context}' not found in kubeconfig.",
                style="bold red",
            )
            utils.console.print(f"Available contexts: {', '.join(available)}")
            raise typer.Exit(code=1)

        return selected["name"], selected["context"].get("cluster", "unknown")

    def close(self) -> None:
        """
        Close the API client.
        """
        if self.api_client:
            self.api_client.close()

    @retry(CLUSTER_ERRORS, tries=3, delay=2)
    def find_secrets(self) -> "KubernetesSecretOperator":
        """
        List Kubernetes secrets and find the ones that use the specified certificate.
        """

        try:
            secrets = self.v1.list_secret_for_all_namespaces(
                field_selector="type=kubernetes.io/tls"
            ).items

            kubernetes_certificate = CertificateLoader(userdata=self.userdata)
            self.kubernetes_certificates.clear()

            for secret in secrets:
                # Decode the certificate
                body = base64.b64decode(secret.data["tls.crt"])

                # Load the certificate
                certificate = kubernetes_certificate.load_certificate_string(
                    cert_data=body
                )

                # Compare the domains
                if set(self.cert.domains).intersection(certificate.domains):
                    self.kubernetes_certificates.append(
                        data.Secrets(
                            name=secret.metadata.name,
                            namespace=secret.metadata.namespace,
                            cert=certificate,
                        )
                    )
                    if self.userdata.verbose:
                        utils.console.print(
                            f"Secret: {secret.metadata.name} in namespace: {secret.metadata.namespace}",  # noqa
                            style="bold yellow",
                        )

        finally:
            self.close()

        return self

    def get_secrets(self) -> list[data.Secrets]:
        return self.kubernetes_certificates

    @retry(CLUSTER_ERRORS, tries=3, delay=2)
    def patch_secret(self) -> list[data.Secrets]:
        """
        Patch the Kubernetes secret.
        """

        secret_data = {
            "data": {
                "tls.crt": self.cert.cert,
                "tls.key": self.cert.key,
            }
        }

        self.failed_patches.clear()

        try:
            for secret in self.kubernetes_certificates:
                try:
                    self.v1.patch_namespaced_secret(
                        name=secret.name,
                        namespace=secret.namespace,
                        body=secret_data,
                        pretty="true",
                    )

                    if self.userdata.verbose:
                        utils.console.print(
                            f"Secret {secret.name} in namespace {secret.namespace} patched successfully.",  # noqa
                            style="bold yellow",
                        )

                except ApiException as error:
                    self.failed_patches.append(f"{secret.namespace}/{secret.name}")
                    utils.console.print(
                        f"Error patching secret {secret.name} in namespace {secret.namespace}: {error}",  # noqa
                        style="bold red",
                    )

            # Prepare the output
            self.find_secrets()

        finally:
            self.close()

        return self.get_secrets()
