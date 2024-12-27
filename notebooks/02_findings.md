# Options Market Analysis: Predicting Price Movements Using Skew Data

## Table of Contents
1. [Modeling Journey & Evolution](#modeling-journey--evolution)
2. [Feature Engineering Evolution](#feature-engineering-evolution)
3. [Key Findings](#key-findings)
4. [Technical Challenges & Solutions](#technical-challenges--solutions)
5. [Final Model Configuration](#final-model-configuration)
6. [Recommendations](#recommendations-for-future-work)
7. [Limitations](#limitations)

## Modeling Journey & Evolution

### Initial Approach
- Started with simple neural networks
- Base features: skew trends, volatility, volume metrics
- Initial ROC AUC: ~0.56 for 5-day predictions

### Model Iterations

#### 1. Simple Neural Network
- Base features: AUC 0.5550
- Enhanced features: AUC 0.5557
- Architecture: (50, 25) hidden layers

#### 2. Deep Neural Network
- Base features: AUC 0.5498
- Enhanced features: AUC 0.5568
- Architecture: (200, 100, 50) hidden layers

#### 3. Ensemble Methods
- GBM: AUC 0.5551
- Random Forest: AUC 0.5526
- Provided valuable feature importance insights

#### 4. Final Focused GBM
- AUC 0.5579 (best performance)
- More stable features
- Better handling of edge cases

## Feature Engineering Evolution

### Base Features
python
base_features = [
'skew_trend_10d', 'skew_volatility', 'log_moneyness_skew',
'log_option_volume', 'volume_spread'
]

### Enhanced Features
- Added non-linear transformations (squared, cubed)
- EMAs with different windows (3d, 5d, 10d)
- RSI indicators
- Volatility adjustments

### Final Focused Features
python
focused_features = [
'skew_ema_10d', 'skew_volatility', 'volume_spread',
'skew_ema_3d', 'vol_adj_skew',
'ema_ratio', 'ema_diff', 'ema_trend',
'vol_weighted_spread', 'volume_trend', 'spread_momentum'
]


## Key Findings

### Most Important Features (by final GBM importance)
1. skew_ema_10d (30.2%)
2. skew_volatility (11.1%)
3. volume_trend (10.0%)
4. volume_spread (9.4%)
5. spread_momentum (7.8%)

### Performance Characteristics
- Consistent AUC around 0.55-0.56
- Better at predicting 5-day vs 10-day horizons
- Trade-off between precision and recall

## Technical Challenges & Solutions

### 1. Data Quality
- Handled NaN values through dropna
- Implemented safe division operations
- Clipped extreme values

### 2. Feature Engineering
- Added bounds to percentage changes (-10, 10)
- Used safe mathematical operations
- Normalized features appropriately

### 3. Model Stability
- Increased min_samples_leaf for stability
- Used conservative learning rates
- Implemented early stopping

## Final Model Configuration
python
focused_gbm = GradientBoostingClassifier(
n_estimators=300,
learning_rate=0.03,
max_depth=4,
min_samples_leaf=30,
subsample=0.85,
random_state=42
)

## Recommendations for Future Work

### 1. Feature Engineering
- Explore more sophisticated technical indicators
- Add cross-asset relationships
- Consider market regime features

### 2. Model Improvements
- Try stacking multiple models
- Experiment with different time windows
- Implement dynamic feature selection

### 3. Risk Management
- Add position sizing based on prediction confidence
- Implement stop-loss mechanisms
- Consider transaction costs

### 4. Data Enhancements
- Add market sentiment indicators
- Include macro-economic features
- Consider alternative data sources

## Limitations

### 1. Predictive Power
- Modest improvement over random chance
- Challenge in maintaining consistent performance

### 2. Data Constraints
- Limited to options market data
- Potential look-ahead bias in some features

### 3. Model Complexity
- Trade-off between complexity and performance
- Risk of overfitting with more complex models