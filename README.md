# Orulo Web Scraper
A web-scraping script using Python and Selenium to extract public information about real estate developments in Brazil, available in the [https://www.orulo.com.br/](Órulo) website.

# Web Scraping Real Estate Developments in Brazil

This Python repository contains a web scraping script that extracts public information about real estate developments in Brazil, which are available for investment. The script gathers basic information about each development available on a specific website and saves it as rows in an Excel (.xlsx) file.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Dependencies](#dependencies)
- [License](#license)

## Introduction

Web scraping is a technique used to gather data from websites automatically. In this project, we scrape information about real estate developments in Brazil, which can be valuable for investors or real estate enthusiasts. The script automates the process of collecting data and organizes it into an Excel file for easy analysis.

## Features

- Scrapes public information about real estate developments in Brazil.
- Extracts basic details of each development, such as name, location, price, and more.
- Saves the collected data as rows in an Excel (.xlsx) file for easy access and analysis.

## Installation

To use this web scraping script, follow these steps:

1. Clone the repository to your local machine:

   ```shell
   git clone https://github.com/igormichetti/orulo-scraper.git 
   
2. Navigate to the project directory:
   ```shell
   cd orulo-scraper 

3. Install the required dependencies (see Dependencies below):
   ```shell
   pip install -r requirements.txt
   
4. Modify the configuration settings in the locators.py file to specify the target website and scraping parameters. (See Configuration section below.)

## Usage

1. Run the main web scraping script:
   ```shell
  python main.py

2. The script will start scraping data from the specified website and save the results in an Excel (.xlsx) file in the output directory.

3. Access and analyze the data in the Excel file for investment opportunities.

## Configuration

Before running the script, assert that you have an account in [https://www.orulo.com.br/](Órulo) configure the variable settings in the locators.py file, such as:
_USER : The email used by the user to sign-in.
_PASS : The user's password.
BUILDINGS_URL: Here you can add one or a list of coordinates url depending on the region you want to scrape.

## License

This project is licensed under the MIT License. See the LICENSE file for more details. Feel free to modify and use this code for your own purposes.

Happy scraping! 
   

