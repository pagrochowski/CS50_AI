import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    filename = "shopping.csv"

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(filename)
    load_data(filename)

    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    model = train_model(X_train, y_train)
    print(model)
    print(model.score(X_test, y_test))

    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")

def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    # Compute how well we performed
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    for label, prediction in zip(labels, predictions):
        if label == 1:
            if label == prediction:
                tp += 1
            else:
                fp += 1
        else:
            if label == prediction:
                tn += 1
            else:
                fn += 1
    sensitivity = tp / (tp + fp)
    specificity = tn / (tn + fn)
    return sensitivity, specificity


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model


def test_load_data():
    evidence, labels = load_data("shopping.csv")

    # Test first ten rows of evidence
    assert evidence[:10] == [[0, 0.0, 0, 0.0, 1, 0.0, 0.2, 0.2, 0.0, 0.0, 1, 1, 1, 1, 1, 1, 0], 
                             [0, 0.0, 0, 0.0, 2, 64.0, 0.0, 0.1, 0.0, 0.0, 1, 2, 2, 1, 2, 1, 0], 
                             [0, 0.0, 0, 0.0, 1, 0.0, 0.2, 0.2, 0.0, 0.0, 1, 4, 1, 9, 3, 1, 0], 
                             [0, 0.0, 0, 0.0, 2, 2.666666667, 0.05, 0.14, 0.0, 0.0, 1, 3, 2, 2, 4, 1, 0], 
                             [0, 0.0, 0, 0.0, 10, 627.5, 0.02, 0.05, 0.0, 0.0, 1, 3, 3, 1, 4, 1, 1], 
                             [0, 0.0, 0, 0.0, 19, 154.2166667, 0.015789474, 0.024561404, 0.0, 0.0, 1, 2, 2, 1, 3, 1, 0], 
                             [0, 0.0, 0, 0.0, 1, 0.0, 0.2, 0.2, 0.0, 0.4, 1, 2, 4, 3, 3, 1, 0], 
                             [1, 0.0, 0, 0.0, 0, 0.0, 0.2, 0.2, 0.0, 0.0, 1, 1, 2, 1, 5, 1, 1], 
                             [0, 0.0, 0, 0.0, 2, 37.0, 0.0, 0.1, 0.0, 0.8, 1, 2, 2, 2, 3, 1, 0], 
                             [0, 0.0, 0, 0.0, 3, 738.0, 0.0, 0.022222222, 0.0, 0.4, 1, 2, 4, 1, 2, 1, 0]]


    
    # Test first ten rows of labels
    assert labels[:10] == [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0
    ]



def data_test():
    """
    Load the CSV and provide a list of unique names of the month from column Month
    """
    filename = "shopping.csv"

    unique_names = set()

    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Month"] not in unique_names:
                print(row["Month"])
                unique_names.add(row["Month"])


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    def month_to_num(month):
        months = [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "June",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ]
        return months.index(month)
    
    evidence = []
    labels = []

    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            evidence.append([
                int(row["Administrative"]),
                float(row["Administrative_Duration"]),
                int(row["Informational"]),
                float(row["Informational_Duration"]),
                int(row["ProductRelated"]),
                float(row["ProductRelated_Duration"]),
                float(row["BounceRates"]),
                float(row["ExitRates"]),
                float(row["PageValues"]),
                float(row["SpecialDay"]),
                month_to_num(row["Month"]),
                int(row["OperatingSystems"]),
                int(row["Browser"]),
                int(row["Region"]),
                int(row["TrafficType"]),
                1 if row["VisitorType"] == "Returning_Visitor" else 0,
                1 if row["Weekend"] == "TRUE" else 0
            ])
            labels.append(1 if row["Revenue"] == "TRUE" else 0)

    return (evidence, labels)

if __name__ == "__main__":
    main()