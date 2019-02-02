"""
    GUI for displaying data found when querying sinkhole API
"""

from asyncio import get_running_loop
from typing import Dict

import PySimpleGUI as gui
from whispers import _LOGGER
from whispers.sinkhole import connection


async def main(start: Dict = None) -> None:
    """
    Build GUI for showing data returned from SinkholeQueryData
    """

    _LOGGER.debug("Building connection with hostname %s", start["hostname"])
    conn = connection.SinkholeQueryData(
        tls=start["https"],
        verify_tls=start["verify"],
        auth=start["password"],
        host=start["hostname"],
        loop=get_running_loop(),
    )
    records = await conn.order_data()
    _LOGGER.info("Found %s total records when querying server", len(records))
    values = []

    for record in records:
        name = record[0]
        frequency = record[1]

        if frequency < 100:
            _LOGGER.debug("Encountered %s %s times", name, frequency)
            values.append([name, frequency])
        else:
            # 100 instances is totally arbitrary but weeds out lots that I already know about
            _LOGGER.debug("Skipping %s since encountered more than 100 times", name)

    # GUI set up
    headings = ["Requested Name", "Count"]
    column_layout = [
        [
            gui.Table(
                values=values,
                headings=headings,
                auto_size_columns=True,
                justification="left",
                num_rows=len(values),
                alternating_row_color="gray",
                tooltip="Interesting DNS requests on your network",
            )
        ]
    ]
    layout = [[gui.Column(column_layout, scrollable=True)]]
    window = gui.Window("Table", grab_anywhere=False).Layout(layout)
    event, display_values = window.Read()  # pylint: disable=unused-variable
