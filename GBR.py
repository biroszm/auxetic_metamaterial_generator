import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import itertools

# Load your data
data = pd.read_csv('c_results.csv', sep=',')  # Replace with your actual file path

# Split the data into inputs (X) and output (y)
X = data[['M', 'T', 'B', 'L']]  # Include 'M' directly as it is an integer
y = data['Elasticity']  # Replace with your actual result column name

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

# Create a model and fit it to the training data
model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)

# Perform 5-fold cross-validation
cv_scores = cross_val_score(model, X_train, y_train, cv=5)

# Output the cross-validation scores
print("Cross-validation scores:", cv_scores)
print("Mean CV Score:", np.mean(cv_scores))

# Fit the model to the training data
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = mean_squared_error(y_test, y_pred, squared=False)
r2 = r2_score(y_test, y_pred)
print(f"MAE: {mae}, MSE: {mse}, RMSE: {rmse}, R^2: {r2}")

# Define the target elasticity
target_elasticity = 12000  # Replace with your target elasticity

# Define parameter bounds for T, B, and L
M_values = [1, 2, 3]  # Discrete values for M
T_range = np.arange(0.8, 3.2, 0.1)  # Adjust the range as needed
B_range = np.arange(4, 6.1, 0.1)  # B values from 4 to 6 with a step of 0.1
L_range = np.arange(8, 12.1, 0.1)  # L values from 9 to 10 with a step of 0.1

# Initialize variables to store the best parameters and the minimum residual
best_params = None
min_residual = float('inf')

# Iterate over each combination of M, T, B, and L
for M in M_values:
    for T, B, L in itertools.product(T_range, B_range, L_range):
        params_df = pd.DataFrame([[M, T, B, L]], columns=['M', 'T', 'B', 'L'])
        predicted_elasticity = model.predict(params_df)
        residual = abs(predicted_elasticity - target_elasticity)
        
        if residual < min_residual:
            min_residual = residual
            best_params = [M, T, B, L]
            best_predicted_elasticity = predicted_elasticity

# Output the best result
if best_params is not None:
    print(f"Best Parameters: M={best_params[0]}, T={best_params[1]}, B={best_params[2]}, L={best_params[3]}")
    print(f"Predicted Elasticity: {best_predicted_elasticity}, Residual: {min_residual}")
else:
    print("No optimal parameters found")
