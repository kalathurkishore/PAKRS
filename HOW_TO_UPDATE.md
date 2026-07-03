# How to Update PAKRS with New Notes

As you continue using Google Keep, you will naturally save more notes, reels, and videos. To update your local PAKRS database with these new notes, follow these steps.

## Step 1: Export your new notes
1. Go to [Google Takeout](https://takeout.google.com/).
2. Deselect all, and select **Keep**.
3. Create the export and download the `.zip` file.
4. Extract the `.zip` file. Inside, you will find a `Takeout/Keep/` folder containing your notes as `.json` or `.html` files.

## Step 2: Prepare the Data Directory
Currently, the ingestion script (`keep_parser.py`) processes every file placed in the `data/` directory and adds it to the database.

> [!WARNING]
> To prevent duplicate notes from appearing in your search results, you must **only place the NEW files** into the `data/` directory. 
> 
> **Do not** drop your entire new export over the old one unless you intend to wipe the database and start fresh.

**The recommended workflow:**
1. Open the `/home/kishore/PAKRS/data/` folder.
2. Delete the old `.json` or `.html` files that have already been imported (do not delete the `pakrs.db` file!).
3. Copy your newly exported `.json` or `.html` files from the new Takeout folder into `/home/kishore/PAKRS/data/`.

## Step 3: Run the Ingestion Parser
Once your new notes are in the `data` directory, open your terminal and run the ingestion script from the `PAKRS` directory:

```bash
cd /home/kishore/PAKRS
conda run -n idp env PYTHONPATH=. python ingestion/keep_parser.py
```

The script will read the new files, extract the links, and seamlessly insert them into the existing SQLite database.

## Step 4: Restart the App
Because Streamlit caches the database statistics on startup, it is a good practice to restart the UI so it reflects your latest note count.

1. Go to your terminal where Streamlit is running.
2. Stop it by pressing `Ctrl + C`.
3. Start it again:
   ```bash
   conda run -n idp streamlit run app/main.py
   ```

Your new notes will now be instantly searchable alongside your old ones!
