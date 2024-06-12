# Fantacalcio ETL

Fantacalcio ETL is a project aimed at Extracting, Transforming, and Loading data related to Serie A football players and teams from various sources, with the goal of populating a database for a fantasy football application.

## Project Objective

The main objective of Fantacalcio ETL is to gather updated and comprehensive data about Serie A players and teams from various online sources, including statistical data, performance information, transfers, injuries, and more. These data will then be transformed and loaded into an SQLite database.

## Key Features

- **Extraction**: Collect data from various online sources, including official websites, APIs, and other publicly available resources.
- **Transformation**: Ensure data uniformity and consistency, adapting it to the database data model.
- **Loading**: Load the extracted and transformed data into an SQLite database.

## Project Structure

The project is structured as follows:

- **models/**: Contains SQLAlchemy class definitions for database modeling and related functions.
- **scrapers/**: Contains the various scrapers and related classes and functions for ETL (Extract, Transform, Load) operations.
- **utils/**: Contains useful functions.
- **config.py**: Configuration file for the project, including parameters such as the database path and API keys.
- **main.py**: Main file for running scripts and ETL operations.

## Usage

To use Fantacalcio ETL, follow these steps:

1. **Configure**: Edit the `config.py` file with the appropriate parameters, such as the database path and required API keys.
2. **Run**: Execute the Python script in `main.py` to perform ETL operations, such as data extraction from various sources and loading into the database.
3. **Verify**: Check the outcome of the ETL operations and the integrity of the data in the SQLite database.
