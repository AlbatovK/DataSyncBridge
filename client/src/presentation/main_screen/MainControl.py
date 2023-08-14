import flet
from flet_core import FilePickerResultEvent, Page

from domain.model.StorageEvent import StorageEvent
from presentation.main_screen.MainControlViewModel import MainControlViewModel
from presentation.utility.Observer import Observer


class MainControl(flet.UserControl):

    def __init__(
            self,
            view_model: MainControlViewModel,
            page: Page,
            on_navigate_back: callable
    ):
        super().__init__()
        self.page = page
        self.file_picker = flet.FilePicker()
        self.view_model = view_model
        self.page.overlay.append(self.file_picker)
        self.page.update()

        self.opacity = 0
        self.animate_opacity = 1000

        self.on_navigate_back = on_navigate_back

    def setup_banner(self):
        def close_banner():
            self.page.banner.open = False
            self.page.update()

        def on_exit_confirmed():
            self.view_model.on_user_exit()
            self.animate_opacity = 200
            self.opacity = 0
            self.on_animation_end = lambda _: self.on_navigate_back()
            close_banner()

        def on_exit_cancel():
            close_banner()

        self.page.banner = flet.Banner(
            bgcolor=flet.colors.AMBER_100,
            content_padding=16,
            leading=flet.Icon(
                flet.icons.WARNING_AMBER_ROUNDED,
                color=flet.colors.AMBER,
                size=60
            ),
            content=flet.Text(
                size=16,
                color=flet.colors.BLACK,
                value='Are you sure you want to exit your user account?\n' +
                      'It would require you to authenticate again after reboot.'
            ),
            actions=[
                flet.TextButton(
                    'Exit',
                    on_click=lambda _: on_exit_confirmed()
                ),
                flet.TextButton(
                    'Cancel',
                    on_click=lambda _: on_exit_cancel()
                )
            ]
        )

    def build(self):
        self.setup_banner()

        def on_directory_chosen(e: FilePickerResultEvent):
            self.view_model.on_download_directory_chosen(e.path)

        self.file_picker.on_result = on_directory_chosen

        def on_exit_clicked():
            self.page.banner.open = True
            self.page.update()

        def on_file_chooser_clicked():
            self.file_picker.get_directory_path()

        connection_state_txt = flet.Text('Connecting...')

        connection_state_icon = flet.Icon(flet.icons.WIFI_LOCK)

        path_info_txt = flet.Text(
            value=f".../users/{self.view_model.get_user().user_id}/photos/...",
            size=12,
            color=flet.colors.GREY_600
        )

        state_info_tile = flet.ListTile(
            width=350,
            leading=connection_state_icon,
            title=connection_state_txt,
            subtitle=path_info_txt,
            trailing=flet.PopupMenuButton(
                icon=flet.icons.MORE_VERT,
                items=[
                    flet.PopupMenuItem(
                        text="Retry",
                        icon=flet.icons.RESET_TV,
                        on_click=lambda _: self.view_model.on_connection_retry_clicked()
                    ),
                    flet.PopupMenuItem(
                        text="Stop",
                        icon=flet.icons.TV_OFF,
                        on_click=lambda _: self.view_model.on_connection_stop_clicked()
                    )
                ]
            )
        )

        user_name_txt = flet.Text(
            max_lines=1,
            overflow=flet.TextOverflow.ELLIPSIS,
            size=24,
            color=flet.colors.BLUE_200,
            value=self.view_model.get_user().name
        )

        user_info_card = flet.Card(
            width=200,
            elevation=2,
            shadow_color=flet.colors.BLUE_300,
            content=flet.Container(
                padding=10,
                content=flet.Column(
                    controls=[
                        user_name_txt,
                        flet.Text(
                            size=12,
                            color=flet.colors.GREY_500,
                            value=f"# {self.view_model.get_user().user_id}"
                        )
                    ]
                )
            )
        )

        icon_grid_view = flet.GridView(
            expand=1,
            runs_count=5,
            max_extent=150,
            spacing=10,
            run_spacing=10,
            auto_scroll=True,
        )

        def on_remote_storage_changed(new_files):
            print(new_files)
            icon_grid_view.clean()
            icon_grid_view.controls = [
                flet.Image(
                    src=file,
                    width=200,
                    height=200,
                    fit=flet.ImageFit.FILL
                ) for file in new_files
            ]
            icon_grid_view.update()

        self.view_model.remote_storage_files_live_data.add_observer(
            Observer(on_remote_storage_changed)
        )

        def on_storage_state_changed(event: StorageEvent):
            if event is StorageEvent.ConnectionLostEvent:
                user_info_card.shadow_color = flet.colors.RED_400
                user_name_txt.color = flet.colors.RED_400
                connection_state_txt.value = 'Connection lost'
                connection_state_txt.update()
                user_info_card.update()
            elif event is StorageEvent.ConnectionStoppedEvent:
                user_info_card.shadow_color = flet.colors.GREY_200
                user_name_txt.color = flet.colors.GREY_500
                connection_state_txt.value = 'Connection stopped'
                connection_state_txt.update()
                user_info_card.update()
            else:
                user_info_card.shadow_color = flet.colors.BLUE_300
                user_name_txt.color = flet.colors.BLUE_200
                connection_state_txt.value = 'Connected'
                connection_state_txt.update()
                user_info_card.update()

        self.view_model.storage_event_live_data.add_observer(
            Observer(on_storage_state_changed)
        )

        return flet.Container(
            width=self.page.width,
            height=self.page.height,
            margin=10,
            alignment=flet.alignment.top_left,
            content=flet.Column(
                scroll=flet.ScrollMode.AUTO,
                alignment=flet.MainAxisAlignment.START,
                controls=[
                    flet.Container(
                        padding=15,
                        content=flet.Column(
                            controls=[
                                flet.Row(
                                    width=self.page.width,
                                    vertical_alignment=flet.CrossAxisAlignment.START,
                                    controls=[
                                        flet.Column(
                                            controls=[
                                                flet.Icon(
                                                    name=flet.icons.PERSON_OUTLINE_ROUNDED,
                                                    size=100
                                                ),
                                                flet.Container(
                                                    width=100,
                                                    alignment=flet.alignment.center,
                                                    content=flet.Row(
                                                        alignment=flet.MainAxisAlignment.CENTER,
                                                        controls=[
                                                            flet.ElevatedButton(
                                                                text='Exit',
                                                                color=flet.colors.RED_200,
                                                                on_click=lambda e: on_exit_clicked()
                                                            )
                                                        ]
                                                    )
                                                )
                                            ]
                                        ),
                                        user_info_card,
                                        flet.Container(
                                            width=500,
                                            content=flet.Column(
                                                controls=[
                                                    state_info_tile,
                                                    flet.Container(
                                                        margin=20,
                                                        content=flet.ElevatedButton(
                                                            "Choose download directory",
                                                            on_click=lambda _: on_file_chooser_clicked()
                                                        )
                                                    )
                                                ]
                                            )
                                        )
                                    ]
                                ),
                                flet.Container(
                                    margin=15,
                                    content=flet.Divider(
                                        height=2,
                                        thickness=2,
                                    )
                                ),
                                flet.Container(
                                    padding=20,
                                    width=self.width,
                                    content=icon_grid_view
                                )
                            ],
                        )
                    )
                ]
            )
        )
