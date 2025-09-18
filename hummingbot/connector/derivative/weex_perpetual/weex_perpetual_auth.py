import hashlib
import hmac
import json
from collections import OrderedDict
from typing import Any, Dict
from urllib.parse import urlencode
import base64

from hummingbot.connector.time_synchronizer import TimeSynchronizer
from hummingbot.core.web_assistant.auth import AuthBase
from hummingbot.core.web_assistant.connections.data_types import RESTMethod, RESTRequest, WSRequest


class WeexPerpetualAuth(AuthBase):
    """
    Auth class for Weex Perpetual API, adapted for Hummingbot
    """

    def __init__(self, api_key: str, api_secret: str, access_passphrase: str, time_provider: TimeSynchronizer):
        self._api_key: str = api_key
        self._api_secret: str = api_secret
        self._access_passphrase: str = access_passphrase
        self._time_provider: TimeSynchronizer = time_provider

    def generate_signature(self, timestamp: str, method: str, request_path: str, query_string: str, body: str = "") -> str:
        """
        Generate HMAC-SHA256 signature for Weex API as per the provided example.
        """
        message = timestamp + method.upper() + request_path + query_string + body
        signature = hmac.new(
            self._api_secret.encode("utf-8"),
            message.encode("utf-8"),
            hashlib.sha256
        ).digest()
        return base64.b64encode(signature).decode()

    async def rest_authenticate(self, request: RESTRequest) -> RESTRequest:
        """
        Add authentication headers and parameters to REST requests.
        """
        timestamp = str(int(self._time_provider.time() * 1000))  # Timestamp in milliseconds
        method = request.method.value  # RESTMethod to string (GET, POST, etc.)
        request_path = request.url.split("https://contract-openapi.weex.com")[-1]  # Extract path
        query_string = ""
        body = ""

        # Handle query parameters for GET requests
        if request.params:
            query_string = urlencode(request.params)
            request.url = f"{request.url}?{query_string}"

        # Handle body for POST requests
        if request.method == RESTMethod.POST and request.data:
            body = json.dumps(json.loads(request.data))  # Ensure body is JSON string

        # Generate signature
        signature = self.generate_signature(
            timestamp=timestamp,
            method=method,
            request_path=request_path,
            query_string=query_string,
            body=body
        )

        # Add authentication headers
        headers = {
            "ACCESS-KEY": self._api_key,
            "ACCESS-SIGN": signature,
            "ACCESS-TIMESTAMP": timestamp,
            "ACCESS-PASSPHRASE": self._access_passphrase,
            "Content-Type": "application/json",
            "locale": "zh-CN"
        }
        request.headers = headers

        return request

    async def ws_authenticate(self, request: WSRequest) -> WSRequest:
        """
        WebSocket authentication (currently pass-through as per Weex API).
        """
        return request  # Weex API may require specific WS auth; adjust if needed

    def add_auth_to_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add timestamp and signature to parameters (optional, kept for compatibility).
        """
        timestamp = int(self._time_provider.time() * 1e3)
        request_params = OrderedDict(params or {})
        request_params["timestamp"] = timestamp
        payload = urlencode(request_params)
        request_params["signature"] = self.generate_signature_from_payload(payload=payload)
        return request_params

    def generate_signature_from_payload(self, payload: str) -> str:
        """
        Fallback signature generation for parameters (for compatibility with Binance-style logic).
        """
        secret = bytes(self._api_secret.encode("utf-8"))
        signature = hmac.new(secret, payload.encode("utf-8"), hashlib.sha256).hexdigest()
        return signature

    def header_for_authentication(self) -> Dict[str, str]:
        """
        Fallback header generation (for compatibility, but overridden by rest_authenticate).
        """
        return {"ACCESS-KEY": self._api_key}