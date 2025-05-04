class NotImplementedMethodError(NotImplementedError):
    def __init__(self, class_name: str, method_name: str) -> None:
        self.class_name = class_name
        self.method_name = method_name
        super().__init__(f'Метод {method_name} класса {class_name} не реализован')
