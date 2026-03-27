# Analysis for Lithium-Ion Battery Core Temperature Prediction using Physics Informed Machine Learning

**Authors:** Anirudh Mittal | Praneel Joshi  
**Contact:** anirudh.mittal@iitgn.ac.in | praneel.joshi@iitgn.ac.in  
**Institution:** Indian Institute of Technology Gandhinagar  

---

## Project Overview & Motivation
Real-time prediction of a lithium-ion battery's internal core temperature is critical for preventing thermal runaway; however, directly measuring it remains physically impossible in commercial cells. Traditional electrochemical models are too computationally heavy for real-time use, creating a gap between complex physics and the lightweight processing requirements of a practical Battery Management System (BMS). 

We aim to bridge this gap by using coupled electrical and thermal models to engineer precise ground-truth labels. This enables lightweight machine learning algorithms to accurately monitor battery health directly on embedded microcontrollers for vehicular safety.

## Data Sources & Harmonization
To enable generalized training, we unified heterogeneous battery degradation datasets from multiple academic and research sources:
* **CALCE:** NMC, LFP, LiCoO2, NCA, Other (Cycle-Aging)
* **NASA:** Cycle-Aging
* **Stanford:** LFP (Cycle-Aging)
* **CALB:** NMC, LFP (Cycle-Aging)

These datasets containing raw time-series features (Voltage, Current, Surface Temperature, Time) were unified into a standardized, feature-extracted Parquet format.

<img width="1380" height="752" alt="image" src="https://github.com/user-attachments/assets/43208cac-f40c-45e4-96bc-b0dc607c80ea" />

*(Fig 1. Battery Degradation Dataset and Master Parquet Dataset)*

## Methodology

### 1. Physics-Informed Electrical and Thermal Modeling
To bypass the physical impossibility of placing sensors inside a battery core, we engineered theoretical labels using a coupled electrical-thermal approach.
* A second-order RC equivalent circuit was implemented to capture polarization effects and internal resistance dynamics.
* The generated heat power was fed into a lumped-parameter thermal model.
* Using convective cooling rates and heating gains, we accurately estimated the core temperature from the measurable surface temperature.

<img width="1380" height="752" alt="image" src="https://github.com/user-attachments/assets/0ecc7958-09f9-4468-8863-903796e00e56" />

*(Fig 2. RC Electrical and Thermal Model of Battery)*

### 2. Feature Engineering
We transformed raw time-series data into highly descriptive, cycle-level features. This included:
* **Statistical baselines:** Mean, Max, Min
* **Temporal dynamics:** Rate of change (dV/dt)
* **Spectral transforms:** Fast Fourier Transforms (FFT)
* **High-Frequency:** Wavelet Transforms
* **State of Health (SOH):** Computed using capacity degradation trends across cycles.

### 3. Machine Learning Pipeline
To prevent data leakage, training pipelines utilized strict Group K-Fold cross-validation (grouped by Cell ID). We evaluated a suite of machine learning models prioritized for low inference latency on embedded systems, including Decision Trees, K-Nearest Neighbors (KNN), Support Vector Regressors (SVR), Random Forests, Multi-Layer Perceptrons (MLP), XGBoost, and Linear Regression.

<img width="1408" height="768" alt="image" src="https://github.com/user-attachments/assets/15acfad3-b53c-42ca-8109-911e10cefc49" />

*(Fig 3. Complete Pipeline from labelling to ML Modelling)*

## Achievements & Results

After evaluating the suite of models against our unified dataset, we found that:
* Tree-based and proximity models demonstrated exceptional capability in capturing non-linear thermal dynamics.
* **The Decision Tree regressor outperformed all candidates**, achieving an RMSE of **0.063** and an R-squared of **0.999** for core temperature prediction, while also leading in SOH predictions.
* Heavier gradient boosters like XGBoost over-penalized localized anomalies in the drive cycles, and simple Linear Regression failed to capture complex thermal inertia. This proved that highly localized, non-linear interpolations (like Decision Trees) are optimally suited for this feature space.

<img width="1189" height="590" alt="image" src="https://github.com/user-attachments/assets/52f8ea01-190e-493e-bef9-97b6677a152c" />

*(Fig 4. Model Comparison on Core Temperature Predictions)*

<img width="1189" height="590" alt="image" src="https://github.com/user-attachments/assets/91e26bc1-84ff-4e6f-8d5c-dbd5c35192f0" />

*(Fig 5. Model Comparison on State-of-Health Predictions)*

## Repository Structure

```text
├── Code_Notebooks_Praneel/   # Python notebooks of praneel
├── Code_Notebooks_Anirudh/   # python notebooks of anirudh
├── src/                      # Source code directory
├── Final_Processed_Data/     # Unified master Parquet datasets
├── Models_Anirudh/           # Models we got after ml training - work till week 7
├── Models_Praneel/           # Models we got after ml training - work till week 7
├── Results_Praneel/          # Figures depicting result of ml models
├── Results_Anirudh/          # Figures depicting result of ml models
└── Midesm_Poster/            # Midsem poster files
```

---

## Acknoledgement
We extend our sincere gratitude to Prof. Pallavi Bharadwaj for providing this research opportunity under the Advanced Transportation and Electrification Technology course. Special thanks to the SPEL Lab for their continued support, guidance, and resources.
