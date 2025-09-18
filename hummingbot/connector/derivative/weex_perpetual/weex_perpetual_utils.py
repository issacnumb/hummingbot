from decimal import Decimal

from pydantic import ConfigDict, Field, SecretStr

from hummingbot.client.config.config_data_types import BaseConnectorConfigMap
from hummingbot.core.data_type.trade_fee import TradeFeeSchema

DEFAULT_FEES = TradeFeeSchema(
    maker_percent_fee_decimal=Decimal("0.0002"),
    taker_percent_fee_decimal=Decimal("0.0004"),
    buy_percent_fee_deducted_from_returns=True
)

CENTRALIZED = True

EXAMPLE_PAIR = "BTC-USDT"

BROKER_ID = "weex"


class WeexPerpetualConfigMap(BaseConnectorConfigMap):
    connector: str = "weex_perpetual"
    weex_perpetual_api_key: SecretStr = Field(
        default=...,
        json_schema_extra={
            "prompt": "Enter your Weex Perpetual API key",
            "is_secure": True, "is_connect_key": True, "prompt_on_new": True}
    )
    weex_perpetual_api_secret: SecretStr = Field(
        default=...,
        json_schema_extra={
            "prompt": "Enter your Weex Perpetual API secret",
            "is_secure": True, "is_connect_key": True, "prompt_on_new": True}
    )


KEYS = WeexPerpetualConfigMap.model_construct()

OTHER_DOMAINS = ["weex_perpetual_testnet"]
OTHER_DOMAINS_PARAMETER = {"weex_perpetual_testnet": "weex_perpetual_testnet"}
OTHER_DOMAINS_EXAMPLE_PAIR = {"weex_perpetual_testnet": "BTC-USDT"}
OTHER_DOMAINS_DEFAULT_FEES = {"weex_perpetual_testnet": [0.02, 0.04]}


class WeexPerpetualTestnetConfigMap(BaseConnectorConfigMap):
    connector: str = "weex_perpetual_testnet"
    weex_perpetual_testnet_api_key: SecretStr = Field(
        default=...,
        json_schema_extra={
            "prompt": "Enter your Weex Perpetual testnet API key",
            "is_secure": True, "is_connect_key": True, "prompt_on_new": True}
    )
    weex_perpetual_testnet_api_secret: SecretStr = Field(
        default=...,
        json_schema_extra={
            "prompt": "Enter your Weex Perpetual testnet API secret",
            "is_secure": True, "is_connect_key": True, "prompt_on_new": True}
    )
    model_config = ConfigDict(title="weex_perpetual")


OTHER_DOMAINS_KEYS = {"weex_perpetual_testnet": WeexPerpetualTestnetConfigMap.model_construct()}
