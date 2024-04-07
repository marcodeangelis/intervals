
# Install 

## Virtual environment

Set up your Python3 virtual environment to safely install the dependencies.

On MacOS/Linux:

```bash
$ python3 -m venv myenv 

$ source myenv/bin/activate 

# On Windows replace the second line with: 

#$ myenv\Scripts\activate

(myenv) $ pip install -r requirements.txt
```

## Install using pip

Upon activation of your virtual environment, return the following line in your CLI or terminal:

`pip install git+https://github.com/marcodeangelis/intervals.git`

## Install using `git clone`

First, download or clone this repository on your local drive.

If you don't have Github ssh keys (you may have to enter your github password) use:

`git clone  https://github.com/marcodeangelis/intervals.git`

Otherwise:

`git clone git@github.com:marcodeangelis/intervals.git`


> If you don't have a Github account, just click on the code green button, and hit Download. This will download the code in your designated downloads folder.

Then, open a code editor in the cloned or downloaded folder, or copy the folder `intervals` in your project directory.

## Dependencies

There is only one mandatory dependency to use `intervals`. 

```
numpy>=1.22
```

We recommend also installing `matplotlib` for plotting. 

