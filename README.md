# Release Notes Generator

## Installation
To install, run
```bash
pip install -r requirements.txt
```

## Setup
In order to use this script, you will need a GitHub personal access token, which is a secret code used to access your account. If you don't have one, [click here](https://github.com/settings/tokens/new) to create one. You'll be asked to enter a name -- choose anything you like. You'll also be asked to choose "scopes"; this limits what you'll be able to do with the API using this token. If you're not sure, click "repo" and "gist". Then click "Generate Token" at the bottom of the screen, and copy the token (the long string of letters and numbers shown). You can easily do that by clicking the little clipboard icon next to the token. If you need to authorize the token to access some of your organizations please do so at this moment.

Rather than pasting that token into every script, it's easiest to save it as a config value. 

Create an `.env` file in the root level of this reposioty and add 
```
GITHUB_TOKEN=xxx
```
...replacing the xxx with the token you just copied.

## Usage
```bash
% python main.py --help
Usage: python main.py [--help] | [-o <owner>] [-r <repositories,as,csv>] [-s <start YYYY/MM/DD>] [-e <end YYYY/MM/DD>]
```
### Available options
* `-o`, `--owner`: The owner of the repositiories, it can be your own username or the name of an organization. *required* 
* `-r`, `--repositories`: A list of repositories names as comma separated values. The repositories must belong to `--owner`. No spaces allowed. *required*
* `-s`, `--start`: The date from which we want to extract the release notes for each repo. Format `YYYY/MM/DD`. *required*
* `-e`, `--end`: The end date from which we want to extract the release notes for each repo. *optional, defaults to "today"*