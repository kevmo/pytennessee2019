"""
    Code for startup GUI design.  Should establish arguments for
    connection to sinkhole and pass them through to other code
"""

import asyncio

import PySimpleGUI as gui
import whispers.gui.sinkhole as hole
from whispers import _LOGGER


def startup() -> None:
    """
    Starting GUI
    """

    layout = [
        [
            gui.Text(
                "Whispers!  Query your popular DNS sinkhole!",
                auto_size_text=True,
                font=("Helvetica", 20),
            )
        ],
        [
            gui.Text("What's the hostname of your sinkhole instance?"),
            gui.Text(
                "What's the password hash used to authenticate to the sinkhole API?"
            ),
        ],
        [
            gui.InputText("pi.hole", key="hostname", do_not_clear=True),
            gui.InputText(key="password", password_char="*", do_not_clear=True),
            gui.ReadButton("Connect"),
            gui.ReadButton("Exit"),
        ],
        [
            gui.Checkbox("HTTPS?", key="https", default=True),
            gui.Checkbox("TLS verify?", key="verify", default=True),
        ],
        [
            gui.Text("Save settings for later?", auto_size_text=True),
            gui.ReadButton("Save"),
            gui.ReadButton("Load"),
        ],
    ]

    window = gui.Window(
        "Sinkhole Whipsers", default_element_size=(40, 1), grab_anywhere=True
    )
    window.Layout(layout)

    while True:
        event, values = window.Read()
        if event == "Save":
            filename = gui.PopupGetFile("Save Settings", save_as=True)
            window.SaveToDisk(filename)
        elif event == "Load":
            filename = gui.PopupGetFile("Load Settings")
            window.LoadFromDisk(filename)
        elif event == "Connect":
            asyncio.run(hole.main(values))
        elif event in ["Exit", None]:
            break


if __name__ == "__main__":
    startup()
