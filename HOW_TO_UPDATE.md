# How to Update PAKRS with New Notes

As you continue using Google Keep, you will naturally save more notes, reels, and videos. To update your local PAKRS database AND your live Streamlit Cloud website with these new notes, follow these steps.

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

The script will read the new files, extract the links, and seamlessly insert them into the existing SQLite database (`data/pakrs.db`).

## Step 4: Sync to Streamlit Cloud (Live Website)
Now that your local `data/pakrs.db` database contains the new notes, you need to push it to your GitHub repository so that Streamlit Cloud can update your live website.

Run the following commands in your terminal:
```bash
cd /home/kishore/PAKRS
git add data/pakrs.db
git commit -m "Added new notes to database"
git push
```

**That's it!** Streamlit Cloud is permanently linked to your GitHub repository. The moment you run that `git push` command, Streamlit will detect the new database file, refresh itself in the background, and your live website will instantly show your new notes!
