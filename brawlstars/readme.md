# So what is this?

This is a prototype work to store and analyse battle logs of brawl stars

# How does one use it?

1. You need to have python 3.x and git installed on your system. Then you run the following in order:

- `git clone https://github.com/smyaknti/ScratchPad.git` (I will move it to a proper repo later)

- `cd ScratchPad`

- `cd brawlstars`

- `python -m pip install -r requirements.txt` 
(If you are on linux, you need to make it `python3` and `pip3` instead.)

2. Edit the files and fill in your player tag and your API token from [this website.](https://developer.brawlstars.com)

3. Run `python store_battle_logs.py` (`python3` for linux)

4. You should see three files pop up in your working directory namely `data.bak`, `data.dat` and `data.dir`.

5. You can repeat step 3 as long as you like as it will keep adding to the database.

6. Run `python analyze_battle_logs.py` to see your battle log being printed comprehensively. ( again `python3` for linux)
