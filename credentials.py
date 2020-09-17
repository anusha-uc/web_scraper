class Credential:
    def __init__(self):
        self.user_name = "root"
        self.password = ""
        self.host = "localhost"
        self.database_name = "scrape"    
    
    @staticmethod
    def get_username(obj):
        return obj.user_name

    @staticmethod
    def get_password(obj):
        return obj.password

    @staticmethod
    def get_host(obj):
        return obj.host

    @staticmethod
    def get_databaseName(obj):
        return obj.database_name