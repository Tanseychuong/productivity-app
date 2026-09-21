import pymysql

# Django expects a recent mysqlclient version, so report one
pymysql.version_info = (2, 2, 1, "final", 0)
pymysql.install_as_MySQLdb()