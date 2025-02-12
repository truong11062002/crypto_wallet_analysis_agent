# API Specifications

## Blockchain APIs

### Etherscan API

Base URL: https://api.etherscan.io/api

#### Endpoints

1. Get Wallet Balance

```
GET /api
    ?module=account
    &action=balance
    &address={address}
    &apikey={apikey}
```

2. Get Token Transfers

```
GET /api
    ?module=account
    &action=tokentx
    &address={address}
    &apikey={apikey}
```

## Rate Limits

- Etherscan: 5 requests per second
- Infura: Depends on subscription tier
