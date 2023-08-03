from util.FileUtils import get_firebase_config
import pyrebase.pyrebase


def stream_handler(event):
    print(event)


if __name__ == "__main__":
    user_id: str = ""  # TODO: User authentication system
    config = get_firebase_config()
    firebase = pyrebase.initialize_app(config)
    firebase.database().child(user_id).stream(stream_handler).start_stream()
