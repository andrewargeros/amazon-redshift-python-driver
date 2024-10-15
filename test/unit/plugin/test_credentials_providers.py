import configparser
import os
import typing
from test import (
    adfs_idp,
    azure_browser_idp,
    azure_idp,
    idp_arg,
    jumpcloud_browser_idp,
    jwt_azure_v2_idp,
    jwt_google_idp,
    okta_browser_idp,
    okta_idp,
    ping_browser_idp,
    redshift_browser_idc,
    redshift_idp_token_auth_plugin,
)

import pytest  # type: ignore

import redshift_connector

conf: configparser.ConfigParser = configparser.ConfigParser()
root_path: str = os.path.dirname(os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir))))
conf.read(root_path + "/config.ini")


NON_BROWSER_IDP: typing.List[str] = ["okta_idp", "azure_idp", "adfs_idp"]
NON_BROWSER_IDC: typing.List[str] = ["redshift_idp_token_auth_plugin"]

ALL_IDP: typing.List[str] = [
    "okta_browser_idp",
    "azure_browser_idp",
    "jumpcloud_browser_idp",
    "ping_browser_idp",
    "jwt_google_idp",
    "jwt_azure_v2_idp",
] + NON_BROWSER_IDP


@pytest.mark.parametrize("idp_arg", ALL_IDP, indirect=True)
def test_credential_provider_dne_should_fail(idp_arg) -> None:
    idp_arg["credentials_provider"] = "WrongProvider"
    with pytest.raises(
        redshift_connector.InterfaceError, match="Invalid IdP specified in credential_provider connection parameter"
    ):
        redshift_connector.connect(**idp_arg)


@pytest.mark.parametrize("idp_arg", ALL_IDP, indirect=True)
def test_ssl_and_iam_invalid_should_fail(idp_arg) -> None:
    idp_arg["ssl"] = False
    idp_arg["iam"] = True
    with pytest.raises(
        redshift_connector.InterfaceError,
        match="Invalid connection property setting. SSL must be enabled when using IAM",
    ):
        redshift_connector.connect(**idp_arg)

    idp_arg["ssl"] = True
    idp_arg["credentials_provider"] = "OktacredentialSProvider"
    with pytest.raises(
        redshift_connector.InterfaceError,
        match="Invalid IdP specified in credential_provider connection parameter",
    ):
        redshift_connector.connect(**idp_arg)


@pytest.mark.parametrize("idp_arg", NON_BROWSER_IDC, indirect=True)
def test_using_iam_should_fail(idp_arg) -> None:
    idp_arg["iam"] = True
    with pytest.raises(
        redshift_connector.InterfaceError,
        match="You can not use this authentication plugin with IAM enabled.",
    ):
        redshift_connector.connect(**idp_arg)
