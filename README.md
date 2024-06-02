# Fantacalcio ETL

Fantacalcio ETL is a project aimed at Extracting, Transforming, and Loading data related to Serie A football players and teams from various sources, with the goal of populating a database for fantasy football application.

## Project Objective

The main objective of Fantacalcio ETL is to gather updated and comprehensive data about Serie A players and teams from various online sources, including statistical data, performance information, transfers, injuries, and more. These data will then be transformed and loaded into a sqlite database.

## Key Features

- Extraction of data from various online sources, including official websites, APIs, and other publicly available resources.
- Transformation of data to ensure uniformity and consistency, as well as to adapt it to the database data model.
- Loading of extracted and transformed data into the database.

## Project Structure

The project is structured as follows:

- `scripts/`: Contains Python scripts for data extraction, transformation, and loading.
- `models/`: Contains SQLAlchemy class definitions for database modeling.
- `config.py`: Configuration file for the project, including parameters such as the database path and API keys.
- `main.py`: Main file for running scripts and ETL operations.
- `README.md`: This file, which provides an overview of the project, its features, and its structure.

## Usage

To use Fantacalcio ETL, follow these steps:

1. Configure the `config.py` file with the appropriate parameters, such as the database path and required API keys.
2. Run the Python script in the `main.py` to perform ETL operations, such as data extraction from various sources and loading into the database.
3. Verify the outcome of the ETL operations and the integrity of the data in the database.
