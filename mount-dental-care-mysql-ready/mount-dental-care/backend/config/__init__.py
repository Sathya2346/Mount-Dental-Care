# Enable Django's MySQL backend without requiring a native compiler on Windows.
import pymysql
pymysql.install_as_MySQLdb()
