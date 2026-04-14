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

### 4. Phase 3: Condition-Aware Embedded Deployment (Hardware Optimization)
While ensemble models (like Random Forest) provided high accuracy globally, they drastically exceeded the hardware constraints of standard embedded microcontrollers (e.g., STM32) which require a **Hard Memory Cap of < 2.0 MB Flash** and **Inference Latency of < 5 ms**. To deploy this system safely, we developed a dynamic routing methodology:
* **Condition-Specific Micro-Models:** Instead of a generic global model, we trained specialized, kilobyte-sized algorithms exclusively on localized subsets of data (e.g., NMC | Cold | City/Hilly).

* **Real-Time Hot-Swapping:** The BMS fuses sensor data to classify the current operational state and dynamically queries an optimized routing matrix, selecting the best lightweight model for that specific environment.
* **Results:** The condition-aware approach allowed ultra-lean algorithms (like Decision Trees and Linear Regression) to achieve $R^2 > 0.99$ while maintaining memory footprints as small as **0.003 MB**, successfully clearing all hardware constraints for physical deployment.

<img width="1024" height="559" alt="image" src="https://github.com/user-attachments/assets/c3babea0-41fc-42b2-a2c1-2254b7d2356c" />

*(Fig 4. Embedded Hardware Constraint Filtering Mechanism)*

<img width="1024" height="559" alt="image" src="https://github.com/user-attachments/assets/b9bf525d-674e-429b-81ae-d433905a9a5d" />

*(Fig 5. Condition aware Dynamic Model Selection)*

### 5. Interactive BMS Dashboard
We developed a local Streamlit web application (`app.py`) to simulate and visualize the Phase 3 routing logic. The dashboard demonstrates the real-time "hot-swapping" of models based on simulated driving conditions, compares inference metrics against hardware thresholds, and outputs core temperature safety alerts.

## Achievements & Results
* Tree-based and proximity models demonstrated exceptional capability in capturing non-linear thermal dynamics in the global baseline tests.
* Heavy gradient boosters over-penalized localized anomalies, while simple global Linear Regression failed to capture complex thermal inertia.
* By shifting to the Phase 3 **Dynamic Routing Matrix**, we eliminated the trade-off between accuracy and hardware compliance, deploying models that outperform bulky ensembles while utilizing a fraction of the computational power.

<img width="1189" height="590" alt="image" src="https://github.com/user-attachments/assets/52f8ea01-190e-493e-bef9-97b6677a152c" />

*(Fig 6. Model Comparison on Core Temperature Predictions)*

<img width="1189" height="590" alt="image" src="https://github.com/user-attachments/assets/91e26bc1-84ff-4e6f-8d5c-dbd5c35192f0" />

*(Fig 7. Model Comparison on State-of-Health Predictions)*

## Repository Structure

```text
├── Code_Notebooks_Anirudh/       # Python notebooks (Exploration, Training, Phase 3 Logic)
├── Code_Notebooks_Praneel/       # Python notebooks (Data Harmonization, Feature Engineering)
├── Final_Processed_Data/         # Unified master Parquet datasets
├── Midsem_Poster/                # Mid-semester presentation materials and PDFs
├── Models_Anirudh/               # Saved baseline & tuned ML models (.joblib/.pkl)
├── Models_Praneel/               # Saved baseline & tuned ML models (.joblib/.pkl)
├── Results_Anirudh/              # Exported figures, metric visualizations, and scorecards
├── Results_Praneel/              # Exported figures, metric visualizations, and scorecards
├── __pycache__/                  # Compiled Python files
├── app.py                        # Streamlit Dashboard for real-time condition-aware BMS simulation
├── bms_matrix.csv                # Final optimized model routing matrix (Top 1 per condition)
├── bms_matrix_full.csv           # Complete hardware profiling results for all models
├── bms_matrix_top3.csv           # Top 3 deployable models per condition subset
├── bms_predictions_sample.csv    # Sample time-series predictions for dashboard plotting
└── README.md                     # Project documentation
```

---

## Acknowledegement
We extend our sincere gratitude to Prof. Pallavi Bharadwaj for providing this research opportunity under the Advanced Transportation and Electrification Technology course. Special thanks to the SPEL Lab for their continued support, guidance, and resources.
