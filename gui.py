import dearpygui.dearpygui as dpg
import json
import autoImportStats

with open("db.json", "r") as file:
    db = json.load(file)

if "teams" not in db:
    db["teams"] = {}
    db["teams"]["White"] = ["APO Boby", "Morvatch",
        "Dreadless", "LA MERE A WAKZ", "PtitHeri"]
    db["teams"]["who"] = ["JH en légende"]


def update_sheet():
    summonerNames = [player for t in db["teams"] for player in db["teams"][t]]
    autoImportStats.getStatsUpdateSheet(summonerNames)

dpg.create_context()


with dpg.window(tag="main", label="Manage teams:", width=200, height=500, no_collapse=True, no_close=True):
    """dpg.add_text("Hello world")
    dpg.add_button(label="Save", callback=save_callback)
    dpg.add_input_text(label="string")
    dpg.add_slider_float(label="float")"""
    with dpg.collapsing_header(label="Teams", default_open=True):
        for team in db["teams"]:
            with dpg.collapsing_header(label=team, indent=10, default_open=True):
                players = db["teams"][team]
                with dpg.table(header_row=False):
                    dpg.add_table_column()
                    for i in range(len(players)):
                        with dpg.table_row():
                            with dpg.group(horizontal=True):
                                dpg.add_checkbox()
                                dpg.add_text(f"{players[i]}")
    
    dpg.add_button(label="Update Sheet",callback=update_sheet)
    dpg.add_input_text(label="string")

dpg.create_viewport(title="Apophisen",width=500,height=800)
dpg.setup_dearpygui()
dpg.show_viewport()

dpg.set_primary_window("main", True)


dpg.start_dearpygui()

with open("db.json", "w") as file:
    json.dump(db, file)

dpg.destroy_context()