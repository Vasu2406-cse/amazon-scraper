# Import required libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.datasets import fetch_california_housing

# Load the California Housing dataset
california = fetch_california_housing()
data = pd.DataFrame(california.data, columns=california.feature_names)
data['PRICE'] = california.target

# Show the first few rows of the dataset
print(data.head())

# Check for missing data
print(data.isnull().sum())

# Normalize/Standardize the features
scaler = StandardScaler()
X = data.drop('PRICE', axis=1)
y = data['PRICE']
X_scaled = scaler.fit_transform(X)

# Split the dataset into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

print(f"Training Set Size: {X_train.shape[0]} samples")
print(f"Test Set Size: {X_test.shape[0]} samples")

# Linear Regression Model
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)

# Ridge Regression Model
ridge_model = Ridge(alpha=1.0)  # You can experiment with the alpha value
ridge_model.fit(X_train, y_train)

# Predict the results
y_pred_lr = lr_model.predict(X_test)
y_pred_ridge = ridge_model.predict(X_test)

# Calculate Mean Squared Error (MSE) and R-squared for both models
mse_lr = mean_squared_error(y_test, y_pred_lr)
r2_lr = r2_score(y_test, y_pred_lr)

mse_ridge = mean_squared_error(y_test, y_pred_ridge)
r2_ridge = r2_score(y_test, y_pred_ridge)

# Display the results
print(f"Linear Regression - MSE: {mse_lr}, R-squared: {r2_lr}")
print(f"Ridge Regression - MSE: {mse_ridge}, R-squared: {r2_ridge}")

# Visualize the predictions vs actual values
plt.figure(figsize=(10,6))
plt.scatter(y_test, y_pred_lr, color='blue', label='Linear Regression', alpha=0.5)
plt.scatter(y_test, y_pred_ridge, color='red', label='Ridge Regression', alpha=0.5)
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='black', lw=2)
plt.xlabel("Actual Prices")
plt.ylabel("Predicted Prices")
plt.title("Predicted vs Actual Prices")
plt.legend()
plt.show()

# Create a correlation heatmap to identify significant features
correlation_matrix = data.corr()
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Heatmap")
plt.show()

# Determine which model performed better
if r2_lr > r2_ridge:
    print("Linear Regression model performs better.")
else:
    print("Ridge Regression model performs better.")