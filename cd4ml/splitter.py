import os
import pandas as pd
from cd4ml.filenames import file_names


def get_validation_period(latest_date_train, days_back=15):
    # for Kaggle we want from Wednesday to Thursday for a 15 day period
    offset = (latest_date_train.weekday() - 3) % 7
    end_of_validation_period = latest_date_train - pd.DateOffset(days=offset)
    begin_of_validation_period = end_of_validation_period - pd.DateOffset(days=days_back)
    return (begin_of_validation_period, end_of_validation_period)


def split_validation_train_by_validation_period(train, validation_begin_date, validation_end_date):
    train_validation = train[(train['date'] >= validation_begin_date) & (train['date'] <= validation_end_date)]
    train_train = train[train['date'] < validation_begin_date]
    return train_train, train_validation


def write_data(table, filename):
    print("Writing to data/splitter/{}".format(filename))
    table.to_csv(filename, index=False)


def main():
    print("Loading data...")
    train = pd.read_csv(file_names['raw_data'])

    train['date'] = pd.to_datetime(train['date'], format="%Y-%m-%d")

    latest_date = train['date'].max()

    begin_of_validation, end_of_validation = get_validation_period(latest_date, days_back=57)

    print("Splitting data between {} and {}".format(begin_of_validation, end_of_validation))
    train_train, train_validation = split_validation_train_by_validation_period(train, begin_of_validation,
                                                                                end_of_validation)
    write_data(train_train, file_names['train'])

    write_data(train_validation, file_names['validation'])

    print("Finished splitting")
