# Programmable Elasticity of Auxetic Lattice Structures Using Machine Learning

This repository contains my project on the **inverse design of sinusoidal auxetic lattice structures** with a target elastic response. In this work, I combined **parametric geometry generation**, **finite element analysis (FEA)**, and **machine learning regression** to build a workflow that can propose geometry–material combinations for a requested stiffness (elasticity) value.

The central idea of the project was simple: instead of only simulating auxetic structures in a forward manner, I wanted to create a method that could also answer the inverse question:

> **Given a desired elasticity, what material and geometric parameters should be selected to obtain it as closely as possible?**

The outcome was a data-driven design workflow in which FEA-generated samples were used to train regression models, and the trained models were then used to search for parameter combinations that satisfy a target mechanical response.

---

## Project motivation

Auxetic metamaterials are structures with a **negative Poisson’s ratio**, which means that they expand laterally when stretched instead of contracting like conventional materials. This unusual behavior is not primarily caused by the raw material itself, but by the **internal geometry of the structure**.

Because of that, auxetic lattices are promising candidates for applications where mechanical response must be tailored, such as:

- impact-resistant structures,
- lightweight protective components,
- additively manufactured polymer lattices,
- mechanically tuned inserts or sandwich cores,
- application-specific metamaterial design.

In this project, I focused on a **sinusoidal auxetic pattern**, because it is more realistic from a manufacturability perspective than many purely theoretical auxetic topologies. The selected geometry avoids some of the severe stress concentration issues commonly associated with sharp-cornered re-entrant designs, while still preserving the desired auxetic response.

---

## What this project is about

The main goal of the project was to investigate how the **elasticity of an auxetic lattice** changes as a function of:

- **material type**,
- **strut thickness** `T`,
- **control point location** `B` of the Bézier-defined curved strut,
- **unit-cell size** `L`.

I first generated a simulation dataset with **375 FEA cases**, then trained multiple machine learning regressors on that dataset, and finally evaluated which model can best support the inverse design task. According to the source paper, the study tested 5 values of control point location, 5 strut thicknesses, 5 unit-cell size conditions through interpolation logic, and 3 common thermoplastic materials used in additive manufacturing, producing 375 simulations in total. fileciteturn0file0L1-L20

The three investigated materials were:

- **PET**
- **ABS**
- **PLA**

The three machine learning models compared in the study were:

- **Random Forest Regressor**
- **Gradient Boosting Regressor**
- **K-Nearest Neighbors Regressor**

These models were trained on the FEA-derived dataset and compared using **MAE**, **RMSE**, and **R²**. The paper reports that Random Forest and Gradient Boosting provided the strongest overall predictive performance, while KNN performed worse on the validation metrics. fileciteturn0file0L1-L20

---

## Research workflow

My workflow can be summarized in six steps.

### 1. Select an auxetic unit-cell family
I selected a **sinusoidal auxetic lattice** with an hourglass-like unit cell. The geometry is periodically repeated and rotated to fill the design domain.

### 2. Parametrize the geometry
The unit cell was controlled with three geometric parameters:

- `L` — unit-cell size,
- `T` — strut thickness,
- `B` — control point location used to define the curvature of the strut.

The curved struts were described with a **quadratic Bézier curve**, which provided a compact and intuitive way to control the geometry while keeping the parameterization simple. The source document explicitly describes the unit-cell size, strut thickness, and Bézier control point location as the three main geometric variables used in the study. fileciteturn0file0L1-L20

### 3. Generate simulation data with FEA
For each selected material and parameter combination, I evaluated the elastic response through **finite element analysis in ANSYS Workbench 2023 R2/2023b**, using a patterned 3D structure built from repeated unit cells. A mesh convergence analysis was carried out so that the results of different parameter combinations remained comparable. The study states that each of the 375 simulations was preceded by mesh convergence refinement until the change in results fell below 1%. fileciteturn0file0L1-L20

### 4. Build a machine-learning dataset
The FEA outputs were transformed into a regression dataset, where the input features were the material and geometry parameters, and the target output was the **elasticity** of the structure.

### 5. Train regression models
I split the dataset into training, testing, and validation subsets and trained three regressors to predict elasticity from the input parameters.

### 6. Solve the inverse design problem
Once trained, the model can be used to search through admissible parameter combinations and find the solution that gives the **smallest residual** to a user-defined target elasticity. The paper also emphasizes that this framework can be extended with additional practical constraints, such as manufacturing feasibility, material availability, cost, or relative density. fileciteturn0file0L1-L20

---

## How the method works in practice

The core logic of the project is shown below:

1. I generate a structured dataset from FEA.
2. I train a regression model that learns the mapping
   `material, T, B, L -> elasticity`.
3. I define a desired target elasticity.
4. I scan the feasible design space.
5. I select the parameter combination for which the predicted elasticity is closest to the target.
6. I verify the selected design against FEA.

This turns a traditionally expensive trial-and-error design process into a much more systematic inverse-design workflow.

---

## Included figures

### 1. Evaluation metrics of the trained models
This figure summarizes the regression quality of the compared models using **MAE**, **RMSE**, and **R²**. In my experiments, Random Forest and Gradient Boosting produced very strong fits, both achieving R² values close to 0.99, while KNN lagged behind. The source text reports MAE values of 205.84 and 214.07 for Random Forest and Gradient Boosting respectively, with corresponding R² values of 0.9896 and 0.9898, whereas KNN reached 0.8702. fileciteturn0file0L1-L20

![Model evaluation metrics](assets/figure_1_metrics.png)

### 2. Predicted vs. actual elasticity values
This figure shows how closely the trained models reproduced the simulated FEA values. The closer the points are to the diagonal line, the better the prediction quality.

![Predicted vs. actual values](assets/figure_2_predictions.png)

### 3. Parameter trends and interpolated surfaces
This figure captures the relationship between elasticity and the main geometric parameters. It illustrates an important conclusion of the study: increasing strut thickness tends to increase elasticity, while increasing the control-point height tends to reduce it. It also shows how multiple parameter combinations can produce similar target responses. The source document explicitly states that thicker struts increased stiffness and larger control-point height reduced elasticity, while a change in unit-cell size produced an approximately 8.5% elasticity shift per 1 mm. fileciteturn0file0L1-L20

![Parameter trends and interpolated surfaces](assets/figure_3_surfaces.png)

### 4. Auxetic behavior, geometry, and simulation concept
This overview figure illustrates the physical intuition behind the project: the difference between conventional and auxetic response, the sinusoidal unit-cell topology, the geometric parameters, and the simulated deformation/stress field.

![Auxetic overview](assets/figure_4_auxetic_overview.png)

---

## Key findings

From this project, I arrived at the following main conclusions:

- The selected **sinusoidal auxetic unit cell** is a suitable geometry for programmable mechanical response and is more practical than several alternative auxetic patterns discussed in the literature.
- The **elasticity is strongly governed by geometry**, especially by strut thickness `T`, control point location `B`, and unit-cell size `L`.
- **Material stiffness matters as expected**: PET produced much higher elastic response than ABS, and PLA followed the same geometric trends with different magnitude.
- A machine learning model trained on FEA results can be used to support **inverse design**, meaning that it can suggest candidate parameter combinations for a desired target elasticity.
- The framework is naturally extensible toward additional engineering objectives, such as **cost**, **manufacturability**, **relative density**, or **yield-limited design constraints**.

The source text concludes that ML-based prediction was effective for programmable elasticity design, with overall engineering accuracy acceptable for this type of application, and that the workflow can be extended with practical constraints such as cost, material limits, and manufacturing limitations. fileciteturn0file0L1-L20

---

## Repository contents

A possible repository structure for this project is the following:

```text
.
├── README.md
├── assets/
│   ├── figure_1_metrics.png
│   ├── figure_2_predictions.png
│   ├── figure_3_surfaces.png
│   └── figure_4_auxetic_overview.png
├── data/
│   ├── fea_results.csv
│   └── processed_dataset.csv
├── notebooks/
│   ├── 01_data_preparation.ipynb
│   ├── 02_model_training.ipynb
│   └── 03_inverse_design_demo.ipynb
├── src/
│   ├── geometry_generation.py
│   ├── preprocessing.py
│   ├── train_models.py
│   ├── inverse_design.py
│   └── utils.py
├── results/
│   ├── trained_models/
│   ├── plots/
│   └── selected_designs/
└── docs/
    └── paper.pdf
```

You can adapt this structure to your actual files, but the `assets/` folder is already aligned with the image paths used in this README.

---

## Suggested README sections for the final GitHub repository

If I publish the full repository, I would typically include the following supporting sections as well:

### Requirements
- Python 3.x
- NumPy
- pandas
- scikit-learn
- matplotlib
- ANSYS-generated or exported simulation data
- OpenSCAD for parametric geometry generation

### Typical pipeline
```bash
# 1. Prepare the dataset from exported simulation results
python src/preprocessing.py

# 2. Train regression models
python src/train_models.py

# 3. Run inverse design for a target elasticity
python src/inverse_design.py --target 6000
```

### Example design question
```text
Target elasticity: 6000 N/mm
Constraint: manufacturable geometry only
Goal: find the material and geometric parameter combination
that gets closest to the requested value
```

---

## Final summary

In this project, I developed a workflow for the **programmable mechanical design of auxetic lattice structures** by combining:

- **parametric sinusoidal geometry generation**,
- **finite element simulation**,
- **machine learning regression**, and
- **inverse search for target elasticity**.

The main contribution of the project is that it does not stop at predicting mechanical response. Instead, it supports a practical design use case: **selecting geometry and material settings for a requested elastic behavior**. That makes it relevant for real engineering scenarios where material choice, manufacturing constraints, and target performance must all be considered together.

---

## Citation

If you use this project or build on the same idea, please cite the associated work:

**Márton Tamás Birosz, Balázs János Villányi, Mátyás Andó**  
*Programmable elasticity of auxetic lattice structure using Machine Learning* fileciteturn0file0L1-L20

---

## Acknowledgment

This work was supported by **Project No. TKP2021-NVA-29**, implemented with support from the Ministry of Innovation and Technology of Hungary through the National Research, Development, and Innovation Fund under the TKP2021-NVA funding scheme. fileciteturn0file0L1-L20
