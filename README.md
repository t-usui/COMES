# INTRODUCTION

COMES is a program to estimate the source compiler and the optimization level
utilized to generate executable files.

# PREREQUISITES

* NumPy
* SciPy
* scikit-learn
* MySQL-python
* IDA Pro (by Hex-Rays)

For installing NumPy, SciPy and scikit-learn, utilizing Anaconda is strongly recommended.


# USAGE
## Data Collection
* Update database of the training set
```
main.py updatedb -d <dir_name>
```

## Feature Extraction
* Generate a data file that includes labels and feature vectors of the training set in SVMlight format
```
main.py extract -m <extraction_method> -l <label_type> -o <output_feature_file_name>

ex.)
main.py extract -m 2-gram -l optimization_level -o ../feature/opt_2-gram.dat
```

## Model Development
* Develope a model by training the classifier
```
main.py learn -a <algorithm> -i <input_feature_file_name> -o <output_model_file_name> -p <param_grid_file_name>

ex.)
main.py learn -a boost+NB -i ../feature/opt_2-gram.dat -o ../model/opt_2-gram_boost+NB.model
```

## Estimate