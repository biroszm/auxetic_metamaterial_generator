import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from scipy.optimize import differential_evolution
import matplotlib.pyplot as plt

# Load your data
data = pd.read_csv('c_results.csv')  # Replace with your actual file path

# Split the data into inputs (X) and output (y)
X = data[['T', 'B', 'L']]  # Replace with your actual parameter names
y = data['Elasticity']  # Replace with your actual result column name

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train the Random Forest model
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)

# Perform 5-fold cross-validation
cv_scores = cross_val_score(rf_model, X_train, y_train, cv=5)

# Output the cross-validation scores
print("Cross-validation scores:", cv_scores)
print("Mean CV Score:", np.mean(cv_scores))

# Fit the model to the training data
rf_model.fit(X_train, y_train)

# Evaluate the model
y_pred = rf_model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = mean_squared_error(y_test, y_pred, squared=False)
r2 = r2_score(y_test, y_pred)

print(f"Mean Absolute Error: {mae}")
print(f"Mean Squared Error: {mse}")
print(f"Root Mean Squared Error: {rmse}")
print(f"R-squared: {r2}")

# Cross-validation
scores = cross_val_score(rf_model, X, y, cv=5, scoring='neg_mean_squared_error')
average_rmse = np.sqrt(-scores.mean())
print(f"Cross-Validated RMSE: {average_rmse}")

# Scatter plot of Predicted vs. Actual Values
plt.scatter(y_test, y_pred)
plt.xlabel('Actual Values')
plt.ylabel('Predicted Values')
plt.title('Predicted vs. Actual Values')
plt.show()

# Residual plot
residuals = y_test - y_pred
plt.scatter(y_pred, residuals)
plt.xlabel('Predicted Values')
plt.ylabel('Residuals')
plt.title('Residuals vs. Predicted Values')
plt.axhline(y=0, color='r', linestyle='-')
plt.show()

# Define the objective function for optimization
def objective_function(params):
    params_df = pd.DataFrame([params], columns=X_train.columns)
    predicted_elasticity = rf_model.predict(params_df)
    target_elasticity = 4000  # Replace with your target elasticity
    return abs(predicted_elasticity - target_elasticity)

# Define parameter bounds
param_bounds = [(1.6, 3.2), (4, 6), (8, 12)]  # Replace with your actual bounds

# Perform the global optimization using Differential Evolution
result = differential_evolution(objective_function, param_bounds)

# Output the result
if result.success:
    optimized_params = result.x
    print(f"Optimized parameters: {optimized_params}")
else:
    print("Optimization did not converge:", result.message)
