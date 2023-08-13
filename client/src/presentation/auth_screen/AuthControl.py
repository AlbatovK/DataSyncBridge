import flet
from flet_core import Page

from presentation.auth_screen.AuthControlViewModel import AuthControlViewModel
from presentation.utility.Observer import Observer


class AuthControl(flet.UserControl):

    def __init__(self, view_model: AuthControlViewModel, page: Page, on_navigate: callable):
        super().__init__()
        self.page = page
        self.view_model = view_model
        self.container = None
        self.on_navigate = on_navigate

        self.animate_opacity = 400
        self.opacity = 0

    def build(self):
        def on_txt_field_data_changed():
            txt_field.error_text = ''
            txt_field.update()

        def on_submit_clicked():
            data = txt_field.value
            self.view_model.on_data_submit(data)

        pr_ring = flet.ProgressRing(
            opacity=0,
            width=70,
            height=70,
            stroke_width=7,
            animate_opacity=200,
        )

        pr_container = flet.Container(
            margin=30,
            content=pr_ring,
        )

        txt_field = flet.TextField(
            password=True,
            prefix_icon=flet.icons.VERIFIED_USER,
            can_reveal_password=True,
            border_color=flet.colors.BLUE_200,
            keyboard_type=flet.KeyboardType.NUMBER,
            label='Enter user code',
            on_change=lambda _: on_txt_field_data_changed()
        )

        btn = flet.ElevatedButton(
            text='Submit',
            on_click=lambda _: on_submit_clicked(),
        )

        column = flet.Column(
            alignment=flet.MainAxisAlignment.CENTER,
            horizontal_alignment=flet.CrossAxisAlignment.CENTER,
            spacing=30,
            controls=[
                pr_container,
                txt_field,
                btn,
            ]
        )

        self.container = flet.Container(
            margin=70,
            padding=10,
            opacity=1,
            animate_opacity=700,
            content=column,
        )

        def on_auth_state_changed(auth_state: AuthControlViewModel.AuthState):
            if auth_state is AuthControlViewModel.AuthState.AuthDataInvalid:
                txt_field.error_text = 'Неверный ввод данных'
                txt_field.update()
            elif auth_state is AuthControlViewModel.AuthState.AuthStarted:
                pr_ring.opacity = 1
                pr_ring.color = flet.colors.BLUE_200
                pr_ring.update()
            elif auth_state is AuthControlViewModel.AuthState.AuthConnectionFailedError:
                txt_field.error_text = 'Отсутствие подключения к серверу'
                pr_ring.opacity = 0
                pr_ring.update()
                txt_field.update()
            elif auth_state is AuthControlViewModel.AuthState.AuthUserNotFoundError:
                txt_field.error_text = 'Данный пользователь не существует'
                txt_field.update()
                pr_ring.opacity = 0
                pr_ring.color = flet.colors.RED
                pr_ring.update()
            elif auth_state is AuthControlViewModel.AuthState.AuthSuccess:
                pr_ring.color = flet.colors.GREEN_400
                pr_ring.opacity = 0
                pr_ring.update()
                self.container.on_animation_end = lambda _: self.on_navigate()
                self.container.opacity = 0
                self.container.update()

        self.view_model.auth_state.add_observer(
            Observer(callback=on_auth_state_changed)
        )

        return self.container
