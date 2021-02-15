# Voice2Command

A very simple "virtual assistant" type application. It includes a custom wake word detector and an extensbile command executor. 


---

Installing:
```
pip install -r requirements.txt
```

Starting:
```
python main.py
```

## Custom wake word
A new custom wake word detector can be built using the script from `experiments\trigger_word.ipynb`.
You will need to download the background noise dataset used in the notebook.

## New commands
To add new a command you need to:
*  edit the `commands_config.json` with the new command
* add a new command type extend the `CommandBase`
* add in the run_command function from Processor the condition for the new command type

---

Resources:
* PocketSphinx source: https://cmusphinx.github.io/wiki/download/
* Sentence embeddings: https://github.com/UKPLab/sentence-transformers