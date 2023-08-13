class User:

    def __init__(self, name: str, user_id: int):
        self.name = name
        self.user_id = user_id

    @classmethod
    def from_dto(cls, user_dto: dict):
        return cls(
            name=user_dto['name'],
            user_id=user_dto['user_id']
        )

    def to_dto(self):
        return self.__dict__
