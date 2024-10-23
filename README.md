
### Table of Contents

1. [Installation](#installation)
2. [Project Motivation](#motivation)
3. [File Descriptions](#files)
4. [Results](#results)
5. [Licensing, Authors, and Acknowledgements](#licensing)

## Installation <a name="installation"></a>

The code should run with no issues using Python versions 3.* and libraries as in [requirements](requirements.txt).

## Project Motivation<a name="motivation"></a>

For this project, I was interested in using Stack Overflow data from multiple years, from 2011, to better understand some insights regarding the popularity of programming languages over time.
Here are the questions that the project is currently covering:


1. Which languages were the most popular each year?
2. Did the Android platform experience visible shifts in language of choice over the years?
3. What trends are in top 10 languages popularity?
4. What is the influence of previous experience on present and future choices?

## File Descriptions <a name="files"></a>

There will be 4 notebooks available here to showcase work related to the above questions.<br/>
Each of the notebooks will be exploratory in searching through the data pertaining to the questions showcased by the
notebook title.<br/>
Markdown cells were used to assist in walking through the thought process for individual steps.
</br>Here follows the list of Jupyter Notebooks part of the analysis (each of them will give an answer to the above
listed questions):

A notebook that presents the analysis and loads all the data, named
[Analysis Presentation](notebooks/0.AnalysisPresentation.ipynb).


1. + 2. [What languages were the most popular in each year? Referring specifically to Android paltform, are there any visible shifts in languages popularity between two or more of the top ten languages over the years?](notebooks/1.LanguagesPopularityByYear.ipynb)
3. [What trends are in top 10 languages popularity?](notebooks/2.Top10LanguagesPopularityTrends.ipynb)
4. [What is the influence of previous experience on present and future choices](notebooks/4.ExperiencePreferenceRelation.ipynb) [TBD]
    1. How the number of years in programming influence the preferred/mostly used language? This could be done using scatterplot or heatmaps... Mabye also have a look at Violin/Box Plots. Faceting? Adaptation of Univariate Plots? I can use the average of the years in programming on Y axis. This is qualitative (most used language) vs quantitative (number of years in programming)
    2. Does the developer's principal language(s) influence the desire to learn a specific language in the future? This could be done usign scatterplot too? Maybe it is better to explore correlation with other features too.


Also, a set of python files where used as support for preparation (data load, transformation, etc.):

5. [data_load](preparation/data_load.py)
6. [data_clean](preparation/data_clean.py)
7. [data_transform](preparation/data_transform.py)
8. [data_stats](preparation/data_stats.py)

## Results<a name="results"></a>

As soon as the analysis will be ready, the main findings of the code will be found at the post
available [here](https://medium.com/@evoagent/trendy-languages-for-old-fashioned-programmers-fd3d3789b1a1).

## Licensing, Authors, Acknowledgements<a name="licensing"></a>

Must give credit to Stack Overflow for the data. You can find the Licensing for the data and other descriptive
information at the link available [here](https://survey.stackoverflow.co/). Otherwise,
feel free to use the code here as you would like! 

