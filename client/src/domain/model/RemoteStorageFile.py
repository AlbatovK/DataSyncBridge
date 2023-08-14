from datetime import datetime


class RemoteStorageFile:

    def __init__(self, file_name: str, last_modified: datetime, e_tag):
        self.file_name = file_name
        self.last_modified = last_modified
        self.e_tag = e_tag

    @classmethod
    def from_dto(cls, remote_file_dto: dict):
        return cls(
            file_name=remote_file_dto['Key'],
            last_modified=remote_file_dto['LastModified'],
            e_tag=remote_file_dto['ETag']
        )

    def __repr__(self):
        return f'{self.file_name} {self.last_modified} {self.e_tag}'
