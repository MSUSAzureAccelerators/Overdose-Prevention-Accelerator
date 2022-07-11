# Opioid Overdose Risk Calculator

This tool determines the risk that an individual has for overdosing on opioids in the next year based on an individual's demographics, prior substance use, and involvement in the criminal justice system.  

The individual's attributes are run against a model trained on data from the National Survey of Drug Use and Health (NSDUH) collected yearly from 2015 to 2020.  

## Descriptions of Files
`data_preprocessing.py`: This file loads the raw data from the NSDUH, selects features, and preprocesses the data. The data are then saved in the `data/processed` directory to be used for modelling.  

`data_modelling.py`: This file loads the preprocessed data and runs the model through Logistic Regression and Extreme Boosted Gradient Trees model. These models and their artifacts are then saved in the `models` directory.  

`data_pipeline.py`: This file takes an indivduals demographics, substance use history, and criminal justice system history and runs them against the saved model and then returns an individual's risk scores.