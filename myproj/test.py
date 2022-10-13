#!/usr/bin/env python

import v20

api = v20.Context(
        hostname="api-fxtrade.oanda.com",
        token="e399afd64c7048d997d83b29f3a5efbd-78cef64066e78f15829afb5a9fe0bfe4"
)

print(api.account.get('001-001-7995786-001'))

response = api.account.get('001-001-7995786-001')

print("Response: {} ({})".format(response.status, response.reason))