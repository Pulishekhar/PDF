import frontend.api.gggg as gggg

# Set the path to your virtual environment's nltk_data folder
gggg.data.path.append('/path/to/your/venv/nltk_data')  # Adjust this to your venv path

# Now download the resources
gggg.download('punkt')
gggg.download('punkt_tab')
