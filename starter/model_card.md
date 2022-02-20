Model Card
================
This model predicts the income level of a given individual based on information
 about education level, work class, marital status, sex, among other features.
 For additional information, see the Model Card [paper](https://arxiv.org/pdf/1810.03993.pdf).


## Model Details
This project used a Random Forest Classifier implementation with the default
 hypermaratemers, from scikit-learn `0.24.1`.


## Intended Use
The problem was set as a binary classification, where the prediction task is to
 determine whether a person makes over 50K a year.


## Training Data
The data set is available to download in UCI ML Repository and, according to the
 website, it was extracted from the 1994 Census database. There are 48842
 instances, each presenting 14 different features - 6 continuous and 8
 categorical. More information on the dataset can be found
 [here](https://archive.ics.uci.edu/ml/datasets/census+income).

The training process used `train_test_split`, from scikit-learn, to split the
 data into random train and test subsets. The train subset is composed of 80% of
 the entire dataset.


## Evaluation Data
The evaluation subset comprises 20% randomly selected instances from the entire
dataset.


## Metrics
 <table>
  <tr>
    <th>Metric</th>
    <th>On Training data</th>
    <th>On Test data</th>
  </tr>
  <tr>
    <td>Precision</td>
    <td>1.0000</td>
    <td>0.7535</td>
  </tr>
  <tr>
    <td>Recall</td>
    <td>1.0000</td>
    <td>0.6190</td>
  </tr>
  <tr>
    <td>F1 score</td>
    <td>1.0000</td>
    <td>0.6797</td>
  </tr>
</table>


## Ethical Considerations
The data were collected in 1994 and contain features that can potentially
 discriminate individuals, such as rance and country of origin.


## Caveats and Recommendations
The model was not optimized, nor were other models considered. Using more
 up-to-date data, a better model selection routine, and hyperparameter tuning
 is recommended.
