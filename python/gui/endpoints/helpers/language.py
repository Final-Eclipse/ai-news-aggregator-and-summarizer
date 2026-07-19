class Language():
    codes = {
        "Arabic": "ar",
        "German": "de",
        "English": "en",
        "Spanish": "sp",
        "French": "fr",
        "Hebrew": "he",
        "Italian": "it",
        "Dutch": "nl",
        "Norwegian": "no",
        "Portuguese": "pt",
        "Russian": "ru",
        "Swedish": "sv",
        "Chinese": "zh"
    }

    qcombobox_options = ["Select language"] + [code for code in codes]