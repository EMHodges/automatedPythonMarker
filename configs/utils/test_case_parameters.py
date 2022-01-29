class TestCaseParameter:

    def __init__(self, inputs, result, msg: str = None):
        self.inputs = inputs
        self.result = result
        self.message = self._set_message(msg)

    def _set_message(self, message) -> str:
        if message:
            return message
        if isinstance(self.inputs, dict):
            message = 'inputs:'
            for key, value in self.inputs.items():
                message += f" {key}: {value},"
            return message
        return f"inputs: {self.inputs}"

    def get_message(self):
        return self.message
