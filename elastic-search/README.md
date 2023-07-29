## Document for Elastic search and SQL Server

### Build & Run

```
docker-compose up -d
```

### Configuration

Update SQL Server configuration in file `logstash/config/logstash.conf`:
-  `jdbc_connection_string`


### Usage

Make a search in `ACCOUNT` table, with `query='Khương'`

```
curl --location 'http://192.168.1.24:9200/account/_search' \
--header 'Content-Type: application/json' \
--data '{
  "query": {
    "bool": {
      "should": [
        {
          "multi_match": {
            "query": "Khương",
            "fields": ["CURRENT_FIRST_NAME", "CURRENT_MIDDLE_NAME", "CURRENT_LAST_NAME"]
          }
        }
      ]
    }
  }
}'
```