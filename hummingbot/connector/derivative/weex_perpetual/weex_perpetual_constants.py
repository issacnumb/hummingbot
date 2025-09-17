from hummingbot.core.api_throttler.data_types import LinkedLimitWeightPair, RateLimit
from hummingbot.core.data_type.in_flight_order import OrderState

EXCHANGE_NAME = "weex_perpetual"
BROKER_ID = "weex"
MAX_ORDER_ID_LEN = 39

DOMAIN = EXCHANGE_NAME
TESTNET_DOMAIN = "weex_perpetual_testnet"

PERPETUAL_BASE_URL = "https://api-contract.weex.com"
TESTNET_BASE_URL = "https://api-contract.weex.com"

PERPETUAL_WS_URL = "wss://ws-spot.weex.com/v2/ws"
TESTNET_WS_URL = "wss://ws-spot.weex.com/v2/ws"

PUBLIC_WS_ENDPOINT = "/public"
PRIVATE_WS_ENDPOINT = "/private"

TIME_IN_FORCE_GTC = "0"  # "GTC"  # Good till cancelled 成交为止（下单后仅有1年有效期，1年后自动取消）
TIME_IN_FORCE_GTX = "1"  # "GTX"  # Good Till Crossing 无法成为挂单方就撤销
TIME_IN_FORCE_IOC = "2"  # "IOC"  # Immediate or cancel 无法立即成交(吃单)的部分就撤销
TIME_IN_FORCE_FOK = "3"  # "FOK"  # Fill or kill 无法全部立即成交就撤销

# Public API v1 Endpoints
SNAPSHOT_REST_URL = "/capi/v2/market/depth"  # 行情接口-获取深度数据
TICKER_PRICE_URL = "v1/ticker/bookTicker"  # 行情接口-获取某个ticker信息
TICKER_PRICE_CHANGE_URL = "v1/ticker/bookTicker"  # 行情接口-获取某个ticker信息
EXCHANGE_INFO_URL = "/capi/v2/market/contracts"  # 行情接口-获取合约信息
RECENT_TRADES_URL = "/capi/v2/market/trades"  # 行情接口-获取成交数据
PING_URL = "/capi/v2/market/time"  # 原本为连通性测试, 这里修改为 获取服务器时间接口
"""
{
    "symbol": "BTCUSDT",				// 交易对
    "markPrice": "11793.63104562",		// 标记价格
    "indexPrice": "11781.80495970",		// 指数价格
    "estimatedSettlePrice": "11781.16138815",  // 预估结算价,仅在交割开始前最后一小时有意义
    "lastFundingRate": "0.00038246",	// 最近更新的资金费率
    "interestRate": "0.00010000",		// 标的资产基础利率
    "nextFundingTime": 1597392000000,	// 下次资金费时间
    "time": 1597370495002				// 更新时间
}
这个接口融合了获取 标记价格/指数价格 资金费率 和资金费率时间等信息. 需要重新组合Weex那边没有相关接口需要组合一下
"""
# TODO Weex那边没有相关接口需要组合一下
# MARK_PRICE_URL = "v1/premiumIndex"
MARK_PRICE_URL = "Weex暂无此接口"
SERVER_TIME_PATH_URL = "/capi/v2/market/time"

# Private API v1 Endpoints
ORDER_URL = "/capi/v2/order/placeOrder"  # 交易接口-下单
# TODO 需要做出修改
CANCEL_ALL_OPEN_ORDERS_URL = "/capi/v2/order/cancel_batch_orders"  # 原本为撤销所有订单接口, 这里修改为批量撤单接口
ACCOUNT_TRADE_LIST_URL = "/capi/v2/order/history"  # 交易接口-获取订单历史委托
SET_LEVERAGE_URL = "/capi/v2/account/leverage"  # 账户接口-/capi/v2/account/leverage
# TODO 无此接口,作用:获取期权资金流水下载Id (USER_DATA)
GET_INCOME_HISTORY_URL = "v1/income"
# TODO 无此接口,作用:更改持仓模式(TRADE)
CHANGE_POSITION_MODE_URL = "v1/positionSide/dual"

# TODO 这俩也没用, 需要把引用的地方处理掉
POST_POSITION_MODE_LIMIT_ID = f"POST{CHANGE_POSITION_MODE_URL}"
GET_POSITION_MODE_LIMIT_ID = f"GET{CHANGE_POSITION_MODE_URL}"

# Private API v2 Endpoints
ACCOUNT_INFO_URL = "v2/account"  # 原始含义:账户信息V2 (USER_DATA)
POSITION_INFORMATION_URL = "v2/positionRisk"  # 原始含义:用户持仓风险V2 (USER_DATA)

# TODO weex没有这个鬼东西
# Private API Endpoints
BINANCE_USER_STREAM_ENDPOINT = "v1/listenKey"

# Funding Settlement Time Span
FUNDING_SETTLEMENT_DURATION = (0, 30)  # seconds before snapshot, seconds after snapshot

# Order Statuses 订单状态已经映射完毕
ORDER_STATE = {
    "pending": OrderState.PENDING_CREATE,
    "open": OrderState.OPEN,
    "filled": OrderState.FILLED,
    "canceling": OrderState.PENDING_CANCEL,
    "canceled": OrderState.CANCELED,
    "untriggered": OrderState.OPEN,
}

# Rate Limit Type
REQUEST_WEIGHT = "REQUEST_WEIGHT"
ORDERS_1MIN = "ORDERS_1MIN"
ORDERS_1SEC = "ORDERS_1SEC"

DIFF_STREAM_ID = 1
TRADE_STREAM_ID = 2
FUNDING_INFO_STREAM_ID = 3
HEARTBEAT_TIME_INTERVAL = 30.0

# Rate Limit time intervals
ONE_HOUR = 3600
ONE_MINUTE = 60
ONE_SECOND = 1
ONE_DAY = 86400

MAX_REQUEST = 2400

# TODO 速率限制最后再来做
RATE_LIMITS = [
    # Pool Limits
    RateLimit(limit_id=REQUEST_WEIGHT, limit=2400, time_interval=ONE_MINUTE),
    RateLimit(limit_id=ORDERS_1MIN, limit=1200, time_interval=ONE_MINUTE),
    RateLimit(limit_id=ORDERS_1SEC, limit=300, time_interval=10),
    # Weight Limits for individual endpoints
    RateLimit(limit_id=SNAPSHOT_REST_URL, limit=MAX_REQUEST, time_interval=ONE_MINUTE,
              linked_limits=[LinkedLimitWeightPair(REQUEST_WEIGHT, weight=20)]),
    RateLimit(limit_id=TICKER_PRICE_URL, limit=MAX_REQUEST, time_interval=ONE_MINUTE,
              linked_limits=[LinkedLimitWeightPair(REQUEST_WEIGHT, weight=2)]),
    RateLimit(limit_id=TICKER_PRICE_CHANGE_URL, limit=MAX_REQUEST, time_interval=ONE_MINUTE,
              linked_limits=[LinkedLimitWeightPair(REQUEST_WEIGHT, weight=1)]),
    RateLimit(limit_id=EXCHANGE_INFO_URL, limit=MAX_REQUEST, time_interval=ONE_MINUTE,
              linked_limits=[LinkedLimitWeightPair(REQUEST_WEIGHT, weight=40)]),
    RateLimit(limit_id=RECENT_TRADES_URL, limit=MAX_REQUEST, time_interval=ONE_MINUTE,
              linked_limits=[LinkedLimitWeightPair(REQUEST_WEIGHT, weight=1)]),
    RateLimit(limit_id=BINANCE_USER_STREAM_ENDPOINT, limit=MAX_REQUEST, time_interval=ONE_MINUTE,
              linked_limits=[LinkedLimitWeightPair(REQUEST_WEIGHT, weight=1)]),
    RateLimit(limit_id=PING_URL, limit=MAX_REQUEST, time_interval=ONE_MINUTE,
              linked_limits=[LinkedLimitWeightPair(REQUEST_WEIGHT, weight=1)]),
    RateLimit(limit_id=SERVER_TIME_PATH_URL, limit=MAX_REQUEST, time_interval=ONE_MINUTE,
              linked_limits=[LinkedLimitWeightPair(REQUEST_WEIGHT, weight=1)]),
    RateLimit(limit_id=ORDER_URL, limit=MAX_REQUEST, time_interval=ONE_MINUTE,
              linked_limits=[LinkedLimitWeightPair(REQUEST_WEIGHT, weight=1),
                             LinkedLimitWeightPair(ORDERS_1MIN, weight=1),
                             LinkedLimitWeightPair(ORDERS_1SEC, weight=1)]),
    RateLimit(limit_id=CANCEL_ALL_OPEN_ORDERS_URL, limit=MAX_REQUEST, time_interval=ONE_MINUTE,
              linked_limits=[LinkedLimitWeightPair(REQUEST_WEIGHT, weight=1)]),
    RateLimit(limit_id=ACCOUNT_TRADE_LIST_URL, limit=MAX_REQUEST, time_interval=ONE_MINUTE,
              linked_limits=[LinkedLimitWeightPair(REQUEST_WEIGHT, weight=5)]),
    RateLimit(limit_id=SET_LEVERAGE_URL, limit=MAX_REQUEST, time_interval=ONE_MINUTE,
              linked_limits=[LinkedLimitWeightPair(REQUEST_WEIGHT, weight=1)]),
    RateLimit(limit_id=GET_INCOME_HISTORY_URL, limit=MAX_REQUEST, time_interval=ONE_MINUTE,
              linked_limits=[LinkedLimitWeightPair(REQUEST_WEIGHT, weight=30)]),
    RateLimit(limit_id=POST_POSITION_MODE_LIMIT_ID, limit=MAX_REQUEST, time_interval=ONE_MINUTE,
              linked_limits=[LinkedLimitWeightPair(REQUEST_WEIGHT, weight=1)]),
    RateLimit(limit_id=GET_POSITION_MODE_LIMIT_ID, limit=MAX_REQUEST, time_interval=ONE_MINUTE,
              linked_limits=[LinkedLimitWeightPair(REQUEST_WEIGHT, weight=30)]),
    RateLimit(limit_id=ACCOUNT_INFO_URL, limit=MAX_REQUEST, time_interval=ONE_MINUTE,
              linked_limits=[LinkedLimitWeightPair(REQUEST_WEIGHT, weight=5)]),
    RateLimit(limit_id=POSITION_INFORMATION_URL, limit=MAX_REQUEST, time_interval=ONE_MINUTE, weight=5,
              linked_limits=[LinkedLimitWeightPair(REQUEST_WEIGHT, weight=5)]),
    RateLimit(limit_id=MARK_PRICE_URL, limit=MAX_REQUEST, time_interval=ONE_MINUTE, weight=1,
              linked_limits=[LinkedLimitWeightPair(REQUEST_WEIGHT, weight=1)]),
]

ORDER_NOT_EXIST_ERROR_CODE = -2013
ORDER_NOT_EXIST_MESSAGE = "Order does not exist"
UNKNOWN_ORDER_ERROR_CODE = -2011
UNKNOWN_ORDER_MESSAGE = "Unknown order sent"

"""
0	操作成功
9999	公共异常
500	内部错误
501	系统繁忙
401	未授权
402	api_key过期
406	访问ip不在白名单
506	未知的请求来源
510	请求过于频繁
511	接口禁止访问
513	请求无效(针对open api 请求时间大于服务器时间2秒或者小于服务器时间10秒以上)
600	参数错误
601	数据解析错误
602	验签失败
603	重复请求
701	需要账户读权限
702	需要账户写权限
703	需要交易读权限
704	需要交易写权限
1000	账户不存在
1001	合约不存在
1002	合约未启用
1003	风险限额等级错误
1004	金额错误
2001	订单方向错误
2002	开仓类型错误
2003	买单价格过高
2004	卖单价格过低
2005	余额不足
2006	杠杆倍数错误
2007	订单价格错误
2008	可平数量不足
2009	仓位不存在或已平仓
2011	订单数量错误
2013	取消订单数量超过最大限制
2014	批量下单数量超限
2015	价格或者数量精度错误
2016	计划委托超过最大委托数量
2018	超过最大可减保证金
2019	存在开仓活跃委托
2021	下单杠杆倍数和已有仓位杠杆倍数不一致
2022	持仓类型错误
2023	存在大于新档位最大杠杆倍数的持仓
2024	存在大于新档位最大杠杆倍数的订单
2025	当前持仓数量大于新档位最大允许数量
2026	全仓不支持修改杠杆
2027	同一方向全仓和逐仓只能存在一个
2028	超过最大下单数量
2029	订单类型错误
2030	外部订单id过长(最大32位长度)
2031	超过当前风险限额最大允许持仓数量
2032	下单价格小于多仓强平价
2033	下单价格大于空仓强平价
2034	批量查询数量超限
2035	不支持的市价单档位
3001	计划委托价格类型错误
3002	计划委托触发类型错误
3003	执行周期错误
3004	触发价格错误
4001	不支持的币种
2036	下单次数超过上限，请联系客服
2037	交易频繁,请稍后再试
2038	超过最大允许持仓数量，请联系客服!
5001	止盈价和止损价不能同时为空
5002	止盈止损单不存在或已关闭
5003	止盈止损价设置有误
5004	止盈止损单总挂单量大于仓位可平数量
6001	禁止交易
6002	禁止开仓
6003	时间范围错误
6004	必须传交易对和状态
6005	交易对未开放
"""