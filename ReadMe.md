# Discord Bot

## Setup
### Environment Setup
1. Make sure you have python `3.10` installed
   - Download via [python.org](https://www.python.org/downloads/)
   - Or install via `pyenv` if cmd is available
     - Check with `pyenv --version`
     - Install with `pyenv install 3.10.18`
2. To install packages within project, set the environment variable:
   - Mac/Linx - `export PIPENV_VENV_IN_PROJECT=1`
   - Windows - `setx PIPENV_VENV_IN_PROJECT 1 ` - permanent
3. Run `pipenv install`

### Running Application
1. Create a `credentials.py` at the `src` folder (this will be ignored for git)
2. Provide the following values, include the discord token. Currently, its:
```python
discord_bot_token = ''
discord_guild_id = ''
discord_nonsense_guild_id = ''
nonsense_general_ch_id = ''
```
3. Run `bot.py`
   - In Pycharm, right click and run the file