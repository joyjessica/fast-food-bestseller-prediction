# Would You Like Fries with That? Predicting Bestselling Food Items at Major Fast Food Restaurants 

## Group Members
Member-1: Ian Alvarado \
Member-2: Akshay Arun \
Member-3: Jessica Joy \
Member-4: Marie Vaughan

## Purpose 
The goal of this project is to predict what makes a menu item a bestseller at fast food restaurants using statistical analysis and machine learning. We focus on features such as new item status, nutritional content, food category, and price to identify the characteristics consumers are most drawn to. Our findings aim to inform both public health initiatives and business strategy.

We used 2022 data from MenuStat.org, a comprehensive database of fast food menu items that includes detailed nutritional information. Price data was scraped from FastFoodMenuPrices.com, and bestseller status was obtained from FastFoodNutrition.org.

## Project Structure  
- /previous-repo-commit-history/: Screenshots documenting the original repository’s commit history prior to transferring work to the classroom repository.
- /scripts/: Contains all source code for data collection and modeling.
    - /data_collection/: Scripts for scraping and processing nutritional information, prices, and bestseller status.
    - /modeling/: Scripts for running predictive models, including Logistic Regression, SVM, LDA, QDA, and Random Forest.
- /README: project overview

## Abstract 
This project investigates the factors that drive consumer preferences at fast food restaurants, with the goal of informing both public health initiatives and business strategies. We employ binary classification techniques to predict which menu items are likely to become bestsellers and to identify the characteristics contributing to their popularity. Multiple models were developed to predict bestseller status, allowing for comparisons of feature importance, accuracy, and overall performance across approaches. More specifically, we then evaluated the nutritional content of bestselling items against the FDA’s daily reference values to assess how popular choices align with recommended dietary guidelines.
The classifications conducted were Support Vector Machine (SVM), Logistic Regression, Linear Discriminant Analysis (LDA), Quadratic Discriminant Analysis (QDA), and Random Forest Classification models. Among these, the Support Vector Machine achieved the highest performance (Accuracy = 0.83, F1 Score = 0.71). Permutation importance analysis revealed total fat, protein, and carbohydrates as the most influential features in predicting bestseller status. This notably aligned with our exploratory data analysis, which revealed that bestselling items exhibited significantly higher levels of these same nutrients compared to non-bestselling items, in some cases reaching nearly 50% of the FDA’s recommended daily intake in a single serving. These findings provide insights into consumer preferences and suggest opportunities for fast food restaurants to prioritize protein-rich options while addressing the high fat content of popular menu items. Additionally, the results can inform public health strategies aimed at improving dietary outcomes among fast food consumers.

