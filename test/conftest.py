import configparser
import os
import sys
import typing

import pytest  # type: ignore

import redshift_connector

conf = configparser.ConfigParser()
root_path = os.path.dirname(os.path.abspath(__file__))
conf.read(root_path + "/config.ini")


# @pytest.hookimpl(tryfirst=True, hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     # execute all other hooks to obtain the report object
#     outcome = yield
#     rep = outcome.get_result()
#
#     # we only look at actual failing test calls, not setup/teardown
#     if rep.when == "call" and rep.failed:
#         mode = "a" if os.path.exists("failures") else "w"
#         with open("failures", mode) as f:
#             f.write(rep.longreprtext + "\n")


def _get_default_connection_args() -> typing.Dict[str, typing.Union[str, bool, int]]:
    """
    Helper function defining default database connection parameter values.
    Returns
    -------

    """
    return {
        "database": conf.get("ci-cluster", "database", fallback="mock_database"),
        "host": conf.get("ci-cluster", "host", fallback="mock_host"),
        "port": conf.getint("default-test", "port", fallback="mock_port"),
        "user": conf.get("ci-cluster", "test_user", fallback="mock_test_user"),
        "password": conf.get("ci-cluster", "test_password", fallback="mock_test_password"),
        "ssl": conf.getboolean("default-test", "ssl", fallback="mock_ssl"),
        "sslmode": conf.get("default-test", "sslmode", fallback="mock_sslmode"),
        "region": conf.get("ci-cluster", "region", fallback="mock_region"),
        "cluster_identifier": conf.get("ci-cluster", "cluster_identifier", fallback="mock_cluster_identifier"),
    }


def _get_default_iam_connection_args() -> typing.Dict[str, typing.Union[str, bool, int]]:
    args = _get_default_connection_args()
    del args["host"]
    del args["port"]
    args["password"] = ""
    return args


@pytest.fixture(scope="class")
def db_kwargs() -> typing.Dict[str, typing.Union[str, bool, int]]:
    return _get_default_connection_args()


def db_groups() -> typing.List[str]:
    return conf.get("cluster-setup", "groups", fallback="mock_groups").split(sep=",")


@pytest.fixture(scope="class")
def perf_db_kwargs() -> typing.Dict[str, typing.Union[str, bool]]:
    db_connect = {
        "database": conf.get("performance-database", "database", fallback="mock_database"),
        "host": conf.get("performance-database", "host", fallback="mock_host"),
        "user": conf.get("performance-database", "user", fallback="mock_user"),
        "password": conf.get("performance-database", "password", fallback="mock_password"),
        "ssl": conf.getboolean("performance-database", "ssl", fallback="mock_ssl"),
        "sslmode": conf.get("performance-database", "sslmode", fallback="mock_sslmode"),
    }

    return db_connect


@pytest.fixture(scope="class")
def serverless_native_db_kwargs() -> typing.Dict[str, str]:
    db_connect = {
        "database": conf.get("redshift-serverless", "database", fallback="mock_database"),
        "host": conf.get(
            "redshift-serverless", "host", fallback="testwg1.012345678901.us-east-2.redshift-serverless.amazonaws.com"
        ),
        "user": conf.get("redshift-serverless", "user", fallback="mock_user"),
        "password": conf.get("redshift-serverless", "password", fallback="mock_password"),
    }

    return db_connect


@pytest.fixture(scope="class")
def serverless_iam_db_kwargs() -> typing.Dict[str, typing.Union[str, bool]]:
    db_connect = {
        "database": conf.get("redshift-serverless", "database", fallback="mock_database"),
        "iam": conf.getboolean("redshift-serverless", "iam", fallback=True),
        "access_key_id": conf.get("redshift-serverless", "access_key_id", fallback="mock_access_key_id"),
        "secret_access_key": conf.get("redshift-serverless", "secret_access_key", fallback="mock_secret_access_key"),
        "session_token": conf.get("redshift-serverless", "session_token", fallback="mock_session_token"),
        "host": conf.get(
            "redshift-serverless", "host", fallback="testwg1.012345678901.us-east-2.redshift-serverless.amazonaws.com"
        ),
    }

    return db_connect  # type: ignore


@pytest.fixture(scope="class")
def provisioned_cname_db_kwargs() -> typing.Dict[str, str]:
    db_connect = {
        "database": conf.get("redshift-provisioned-cname", "database", fallback="mock_database"),
        "host": conf.get("redshift-provisioned-cname", "host", fallback="cname.mytest.com"),
        "db_user": conf.get("redshift-provisioned-cname", "db_user", fallback="mock_user"),
        "password": conf.get("redshift-provisioned-cname", "password", fallback="mock_password"),
    }

    return db_connect


@pytest.fixture(scope="class")
def serverless_cname_db_kwargs() -> typing.Dict[str, typing.Union[str, bool]]:
    db_connect = {
        "database": conf.get("redshift-serverless-cname", "database", fallback="mock_database"),
        "host": conf.get("redshift-serverless-cname", "host", fallback="cname.mytest.com"),
        "db_user": conf.get("redshift-serverless-cname", "db_user", fallback="mock_user"),
        "password": conf.get("redshift-serverless-cname", "password", fallback="mock_password"),
        "is_serverless": conf.getboolean("redshift-serverless-cname", "is_serverless", fallback="mockboolean"),
    }

    return db_connect


@pytest.fixture(scope="class")
def ds_consumer_db_kwargs() -> typing.Dict[str, str]:
    db_connect = {
        "database": conf.get("redshift-ds-consumer", "database", fallback="mock_database"),
        "host": conf.get("redshift-ds-consumer", "host", fallback="cname.mytest.com"),
        "user": conf.get("redshift-ds-consumer", "user", fallback="mock_user"),
        "password": conf.get("redshift-ds-consumer", "password", fallback="mock_password"),
        "extra": conf.get("redshift-ds-consumer", "extra", fallback="mock_extra"),
    }

    return db_connect


@pytest.fixture(scope="class")
def ds_producer_db_kwargs() -> typing.Dict[str, str]:
    db_connect = {
        "database": conf.get("redshift-ds-producer", "database", fallback="mock_database"),
        "host": conf.get("redshift-ds-producer", "host", fallback="cname.mytest.com"),
        "user": conf.get("redshift-ds-producer", "user", fallback="mock_user"),
        "password": conf.get("redshift-ds-producer", "password", fallback="mock_password"),
    }

    return db_connect


@pytest.fixture(scope="class")
def okta_idp() -> typing.Dict[str, typing.Union[str, bool, int]]:
    db_connect = {
        "db_user": conf.get("ci-cluster", "test_user", fallback="mock_test_user"),
        "password": conf.get("okta-idp", "password", fallback="mock_password"),
        "iam": conf.getboolean("okta-idp", "iam", fallback="mock_iam"),
        "idp_host": conf.get("okta-idp", "idp_host", fallback="mock_idp_host"),
        "user": conf.get("okta-idp", "user", fallback="mock_user"),
        "app_id": conf.get("okta-idp", "app_id", fallback="mock_app_id"),
        "app_name": conf.get("okta-idp", "app_name", fallback="mock_app_name"),
        "credentials_provider": conf.get("okta-idp", "credentials_provider", fallback="OktaCredentialsProvider"),
    }
    return {**_get_default_iam_connection_args(), **db_connect}


@pytest.fixture(scope="class")
def okta_browser_idp() -> typing.Dict[str, typing.Union[str, bool, int]]:
    db_connect = {
        "db_user": conf.get("ci-cluster", "test_user", fallback="mock_test_user"),
        "password": conf.get("okta-browser-idp", "password", fallback="mock_password"),
        "iam": conf.getboolean("okta-browser-idp", "iam", fallback="mock_iam"),
        "user": conf.get("okta-browser-idp", "user", fallback="mock_user"),
        "credentials_provider": conf.get(
            "okta-browser-idp", "credentials_provider", fallback="SamlCredentialsProvider"
        ),
        "login_url": conf.get("okta-browser-idp", "login_url", fallback="mock_login_url"),
    }
    return {**_get_default_iam_connection_args(), **db_connect}


@pytest.fixture(scope="class")
def azure_browser_idp() -> typing.Dict[str, typing.Union[str, bool, int]]:
    db_connect = {
        "db_user": conf.get("ci-cluster", "test_user", fallback="mock_test_user"),
        "password": conf.get("azure-browser-idp", "password", fallback="mock_password"),
        "iam": conf.getboolean("azure-browser-idp", "iam", fallback="mock_iam"),
        "user": conf.get("azure-browser-idp", "user", fallback="mock_user"),
        "credentials_provider": conf.get(
            "azure-browser-idp", "credentials_provider", fallback="BrowserAzureCredentialsProvider"
        ),
        "idp_tenant": conf.get("azure-browser-idp", "idp_tenant", fallback="mock_idp_tenant"),
        "client_id": conf.get("azure-browser-idp", "client_id", fallback="mock_client_id"),
        "client_secret": conf.get("azure-browser-idp", "client_secret", fallback="mock_client_secret"),
    }
    return {**_get_default_iam_connection_args(), **db_connect}


@pytest.fixture(scope="class")
def jumpcloud_browser_idp() -> typing.Dict[str, typing.Union[str, bool, int]]:
    db_connect = {
        "db_user": conf.get("ci-cluster", "test_user", fallback="mock_test_user"),
        "password": conf.get("jumpcloud-browser-idp", "password", fallback="mock_password"),
        "iam": conf.getboolean("jumpcloud-browser-idp", "iam", fallback="mock_iam"),
        "user": conf.get("jumpcloud-browser-idp", "user", fallback="mock_user"),
        "credentials_provider": conf.get(
            "jumpcloud-browser-idp", "credentials_provider", fallback="SamlCredentialsProvider"
        ),
        "login_url": conf.get("jumpcloud-browser-idp", "login_url", fallback="mock_login_url"),
    }
    return {**_get_default_iam_connection_args(), **db_connect}


@pytest.fixture(scope="class")
def ping_browser_idp() -> typing.Dict[str, typing.Union[str, bool, int]]:
    db_connect = {
        "iam": conf.getboolean("ping-one-idp", "iam", fallback="mock_iam"),
        "credentials_provider": conf.get("ping-one-idp", "credentials_provider", fallback="PingCredentialsProvider"),
        "login_url": conf.get("ping-one-idp", "login_url", fallback="mock_login_url"),
        "listen_port": conf.getint("ping-one-idp", "listen_port", fallback="mock_listen_port"),
        "idp_response_timeout": conf.getint(
            "ping-one-idp", "idp_response_timeout", fallback="mock_idp_response_timeout"
        ),
    }
    return {**_get_default_iam_connection_args(), **db_connect}


@pytest.fixture(scope="class")
def azure_idp() -> typing.Dict[str, typing.Union[str, bool, int]]:
    db_connect = {
        "db_user": conf.get("ci-cluster", "test_user", fallback="mock_test_user"),
        "password": conf.get("azure-idp", "password", fallback="mock_password"),
        "iam": conf.getboolean("azure-idp", "iam", fallback="mock_iam"),
        "user": conf.get("azure-idp", "user", fallback="mock_user"),
        "credentials_provider": conf.get("azure-idp", "credentials_provider", fallback="AzureCredentialsProvider"),
        "idp_tenant": conf.get("azure-idp", "idp_tenant", fallback="mock_idp_tenant"),
        "client_id": conf.get("azure-idp", "client_id", fallback="mock_client_id"),
        "client_secret": conf.get("azure-idp", "client_secret", fallback="mock_client_secret"),
    }
    return {**_get_default_iam_connection_args(), **db_connect}


@pytest.fixture(scope="class")
def adfs_idp() -> typing.Dict[str, typing.Union[str, bool, int]]:
    db_connect = {
        "db_user": conf.get("ci-cluster", "test_user", fallback="mock_test_user"),
        "password": conf.get("adfs-idp", "password", fallback="mock_password"),
        "iam": conf.getboolean("adfs-idp", "iam", fallback="mock_iam"),
        "user": conf.get("adfs-idp", "user", fallback="mock_user"),
        "credentials_provider": conf.get("adfs-idp", "credentials_provider", fallback="AdfsCredentialsProvider"),
        "idp_host": conf.get("adfs-idp", "idp_host", fallback="mock_idp_host"),
        "cluster_identifier": conf.get("adfs-idp", "cluster_identifier", fallback="mock_adfs_cluster_identifier"),
        "region": conf.get("adfs-idp", "region", fallback="mock-region"),
        "ssl_insecure": conf.getboolean("adfs-idp", "ssl_insecure", fallback=False),
    }
    return {**_get_default_iam_connection_args(), **db_connect}


@pytest.fixture(scope="class")
def jwt_google_idp() -> typing.Dict[str, typing.Union[str, bool, int]]:
    db_connect = {
        "db_user": conf.get("ci-cluster", "test_user", fallback="mock_test_user"),
        "iam": conf.getboolean("jwt-google-idp", "iam", fallback="mock_iam"),
        "password": conf.get("jwt-google-idp", "password", fallback="mock_password"),
        "credentials_provider": conf.get(
            "jwt-google-idp", "credentials_provider", fallback="BasicJwtCredentialsProvider"
        ),
        "web_identity_token": conf.get("jwt-google-idp", "web_identity_token", fallback="mock_web_identity_token"),
        "role_arn": conf.get("jwt-google-idp", "role_arn", fallback="mock_role_arn"),
    }
    return {**_get_default_iam_connection_args(), **db_connect}


@pytest.fixture(scope="class")
def jwt_azure_v2_idp() -> typing.Dict[str, typing.Union[str, bool, int]]:
    db_connect = {
        "db_user": conf.get("ci-cluster", "test_user", fallback="mock_test_user"),
        "iam": conf.getboolean("jwt-azure-v2-idp", "iam", fallback="mock_iam"),
        "password": conf.get("jwt-azure-v2-idp", "password", fallback="mock_password"),
        "credentials_provider": conf.get(
            "jwt-azure-v2-idp", "credentials_provider", fallback="BasicJwtCredentialsProvider"
        ),
        "web_identity_token": conf.get("jwt-azure-v2-idp", "web_identity_token", fallback="mock_web_identity_token"),
        "role_arn": conf.get("jwt-azure-v2-idp", "role_arn", fallback="mock_role_arn"),
    }
    return {**_get_default_iam_connection_args(), **db_connect}


@pytest.fixture(scope="class")
def redshift_native_browser_azure_oauth2_idp() -> typing.Dict[str, typing.Union[str, bool, int]]:
    db_connect = {
        "host": conf.get("redshift-native-browser-azure-oauth2", "host", fallback="mock_host"),
        "port": conf.getint("default-test", "port", fallback="mock_port"),
        "database": conf.get("ci-cluster", "database", fallback="mock_database"),
        "credentials_provider": conf.get(
            "redshift-native-browser-azure-oauth2", "credentials_provider", fallback="BasicJwtCredentialsProvider"
        ),
        "scope": conf.get("redshift-native-browser-azure-oauth2", "scope", fallback="mock_scope"),
        "client_id": conf.get("redshift-native-browser-azure-oauth2", "client_id", fallback="mock_client_id"),
        "idp_tenant": conf.get("redshift-native-browser-azure-oauth2", "idp_tenant", fallback="mock_idp_tenant"),
        "cluster_identifier": conf.get("adfs-idp", "cluster_identifier", fallback="mock_adfs_cluster_identifier"),
        "region": conf.get("adfs-idp", "region", fallback="mock-region"),
        "iam": conf.getboolean("jwt-google-idp", "iam", fallback="mock_iam"),
    }
    return db_connect


@pytest.fixture(scope="class")
def redshift_idp_token_auth_plugin() -> typing.Dict[str, typing.Optional[str]]:
    db_connect = {
        "host": conf.get("redshift-idp-token-auth-plugin", "host", fallback=None),
        "region": conf.get("redshift-idp-token-auth-plugin", "region", fallback=None),
        "database": conf.get("redshift-idp-token-auth-plugin", "database", fallback="dev"),
        "credentials_provider": conf.get(
            "redshift-idp-token-auth-plugin", "credentials_provider", fallback="IdpTokenAuthPlugin"
        ),
        "token": conf.get("redshift-idp-token-auth-plugin", "token", fallback=None),
        "token_type": conf.get("redshift-idp-token-auth-plugin", "token_type", fallback=None),
        "identity_namespace": conf.get("redshift-idp-token-auth-plugin", "identity_namespace", fallback=None),
    }
    return db_connect


@pytest.fixture(scope="class")
def redshift_browser_idc() -> typing.Dict[str, typing.Union[str, typing.Optional[bool], int]]:
    db_connect = {
        "host": conf.get("redshift-browser-idc", "host", fallback=None),
        "region": conf.get("redshift-browser-idc", "region", fallback=None),
        "database": conf.get("redshift-browser-idc", "database", fallback="dev"),
        "credentials_provider": conf.get(
            "redshift-browser-idc", "credentials_provider", fallback="BrowserIdcAuthPlugin"
        ),
        "issuer_url": conf.get("redshift-browser-idc", "issuer_url", fallback=None),
        "idc_region": conf.get("redshift-browser-idc", "idc_region", fallback=None),
        "idp_response_timeout": conf.getint("redshift-browser-idc", "idp_response_timeout", fallback=120),
        "listen_port": conf.get("redshift-browser-idc", "listen_port", fallback=7890),
        "idc_client_display_name": conf.get(
            "redshift-browser-idc", "idc_client_display_name", fallback="Amazon Redshift Python connector"
        ),
    }
    return db_connect


@pytest.fixture
def con(request, db_kwargs) -> redshift_connector.Connection:
    conn: redshift_connector.Connection = redshift_connector.connect(**db_kwargs)

    def fin() -> None:
        conn.rollback()
        try:
            conn.close()
        except redshift_connector.InterfaceError:
            pass

    request.addfinalizer(fin)
    return conn


@pytest.fixture
def cursor(request, con) -> redshift_connector.Cursor:
    cursor: redshift_connector.Cursor = con.cursor()

    def fin() -> None:
        cursor.close()

    request.addfinalizer(fin)
    return cursor


@pytest.fixture
def idp_arg(request) -> typing.Dict[str, typing.Union[str, bool, int]]:
    return request.getfixturevalue(request.param)


@pytest.fixture
def is_java() -> bool:
    return "java" in sys.platform.lower()
