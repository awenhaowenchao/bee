class Result():
    name = "Result"

    def rowsAffected(self) -> int:
        pass


class InsertResult(Result):
    name = "InsertResult"

    def lastInsertId(self) -> int:
        pass


class ExecuteResult(Result):
    name = "ExecuteResult"

    def lastInsertId(self) -> int:
        pass


class Reader():
    pass
