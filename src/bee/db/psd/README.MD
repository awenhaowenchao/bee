# psd

psd is a lightweight, fluent SQL data access library. It supports various types of database, like mysql/mssql/sqlite etc.

* High performance
* Support context.Context
* Support opentracing

## Configure

**psd** use **bee/config** package to manage database options. There is a sample config file in the package(app.yml):

```yaml
bee:
  data:
    sql:
      test:
        provider: mysql
        host: localhost
        port: 3306
        database: test
        user: root
        password: '000000'
        charset: utf8mb4
        max_open_conns: 100
        max_idle_conns: 1
        conn_lifetime: 5m
        trace:
          enabled: True
          time: 200
        options:
          max_open_conns: 100
          max_idle_conns: 1
```

Once you add configuration to app.yml, you can open a database like this:


