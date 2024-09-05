
### Table of Contents

1. [Installation](#installation)
2. [Project Motivation](#motivation)
3. [File Descriptions](#files)
4. [Results](#results)
5. [Licensing, Authors, and Acknowledgements](#licensing)

## Installation <a name="installation"></a>

The code should run with no issues using Python versions 3.* and libraries as in [requirements](requirements.txt).

## Project Motivation<a name="motivation"></a>

For this project, I was interested in using Stack Overflow data from multiple years, from 2011, to better understand:

1. What languages were the most popular in each year?
2. What trends are in top 10 languages popularity?
3. Does the country of origin influence the preferred/mostly used language?
4. Does the amount of years in programming influence the preferred/mostly used language?

## File Descriptions <a name="files"></a>

There will be 4 notebooks available here to showcase work related to the above questions.<br/>
Each of the notebooks will be exploratory in searching through the data pertaining to the questions showcased by the
notebook title.<br/>
Markdown cells were used to assist in walking through the thought process for individual steps.
</br>Here follows the list of Jupyter Notebooks part of the analysis (each of them will give an answer to the above
listed questions):

1. [What languages were the most popular in each year?](notebooks/1.LanguagesPopularityByYear.ipynb)
2. [Referring specifically to Android paltform, are there any visible shifts in languages popularity between two or more of the top ten languages over the years?](notebooks/3.AndroidPlatformLaguagesInDepthAnalysis.ipynb)
3. [What trends are in top 10 languages popularity?](notebooks/2.Top10LanguagesPopularityTrends.ipynb)
4. Does the country of origin influence the preferred/mostly used language?
5. Does the amount of years in programming influence the preferred/most used programming language?

In addition to above listed notebooks, a presentational notebook, containing also all data load operations, named
[Analysis Presentation](notebooks/0.AnalysisPresentation.ipynb).

Also, a set of python files where used as support for preparation (data load, transformation, etc.):

5. [data_load](preparation/data_load.py)
6. [data_clean](preparation/data_clean.py)
7. [data_transform](preparation/data_transform.py)

## Results<a name="results"></a>

As soon as the analysis will be ready, the main findings of the code will be found at the post
available [here](https://medium.com/TBD).

## Licensing, Authors, Acknowledgements<a name="licensing"></a>

Must give credit to Stack Overflow for the data. You can find the Licensing for the data and other descriptive
information at the Kaggle link available [here](https://www.kaggle.com/stackoverflow/so-survey-2017/data). Otherwise,
feel free to use the code here as you would like! 

