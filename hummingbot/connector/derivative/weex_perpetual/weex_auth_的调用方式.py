import json

from hummingbot.connector.derivative.weex_perpetual.weex_perpetual_auth import WeexPerpetualAuth
from hummingbot.connector.time_synchronizer import TimeSynchronizer
from hummingbot.core.web_assistant.connections.data_types import RESTRequest, RESTMethod
from hummingbot.core.web_assistant.connections.rest_connection import RESTConnection

# 初始化认证
time_synchronizer = TimeSynchronizer()
auth = WeexPerpetualAuth(
    api_key="your_api_key",
    api_secret="your_api_secret",
    access_passphrase="your_passphrase",
    time_provider=time_synchronizer
)

# 示例 GET 请求：获取账户资产
request = RESTRequest(
    method=RESTMethod.GET,
    url="https://contract-openapi.weex.com/api/spot/v1/account/assets",
    params={},
    is_auth_required=True
)
request = await auth.rest_authenticate(request)

# 发送请求
connection = RESTConnection()
response = await connection.execute(request)
print(response.status, await response.text())

# 示例 POST 请求：获取交易记录
request = RESTRequest(
    method=RESTMethod.POST,
    url="https://contract-openapi.weex.com/api/spot/v1/trade/fills",
    data=json.dumps({"symbol": "ETHUSDT_SPBL", "limit": "2"}),
    is_auth_required=True
)
request = await auth.rest_authenticate(request)
response = await connection.execute(request)
print(response.status, await response.text())
