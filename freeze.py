from py2exe import freeze

freeze(windows=['pomo.py'], data_files=[
    ("work.ico", ["work.ico"]), 
    ("walk.ico", ["walk.ico"])
])