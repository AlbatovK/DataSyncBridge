import boto3
import requests.exceptions
import urllib3
from pyrebase import pyrebase

from data.local.LocalStorageApi import LocalStorageApi
from data.remote.firebase.FirebaseDao import FirebaseDao
from data.remote.firebase.FirebaseStreamService import FirebaseStreamService
from data.remote.s3.S3Api import S3Api
from data.repository.ClientLocalRepositoryImpl import ClientLocalRepositoryImpl
from data.repository.RemoteFileStorageRepositoryImpl import RemoteFileStorageRepositoryImpl
from data.repository.UserRepositoryImpl import UserRepositoryImpl
from domain.di.AbstractModule import AbstractModule
from presentation.auth_screen.AuthControlViewModel import AuthControlViewModel
from presentation.main_screen.MainControlViewModel import MainControlViewModel


class MainAppModule(AbstractModule):
    @classmethod
    def inject_dependencies(cls, firebase_config, s3_config, local_storage, on_fall_back):
        try:
            firebase = pyrebase.initialize_app(firebase_config)

            RemoteFileStorageRepositoryImpl.initialize(
                FirebaseStreamService(firebase),
                S3Api(
                    s3_config['bucket_name'],
                    boto3.client(
                        's3',
                        aws_access_key_id=s3_config['aws_access_key_id'],
                        aws_secret_access_key=s3_config['aws_secret_access_key'],
                        region_name=s3_config['region_name'],
                        endpoint_url=s3_config['endpoint_url'],
                    ),
                )
            )

            UserRepositoryImpl.initialize(
                FirebaseDao(
                    firebase
                )
            )

            ClientLocalRepositoryImpl.initialize(
                LocalStorageApi(
                    local_storage
                )
            )

        except (requests.exceptions.ConnectionError, urllib3.exceptions.MaxRetryError) as e:
            on_fall_back(e)

    @classmethod
    def provideRemoteFileStorageRepository(cls):
        return RemoteFileStorageRepositoryImpl.get_instance()

    @classmethod
    def provideClientLocalRepository(cls):
        return ClientLocalRepositoryImpl.get_instance()

    @classmethod
    def provideUserRepository(cls):
        return UserRepositoryImpl.get_instance()

    @classmethod
    def provideMainControlViewModel(cls):
        return MainControlViewModel(
            UserRepositoryImpl.get_instance(),
            ClientLocalRepositoryImpl.get_instance(),
            RemoteFileStorageRepositoryImpl.get_instance()
        )

    @classmethod
    def provideAuthControlViewModel(cls):
        return AuthControlViewModel(
            UserRepositoryImpl.get_instance(),
            ClientLocalRepositoryImpl.get_instance()
        )
