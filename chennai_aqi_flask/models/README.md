# aqi_model.pkl

This is the real deployed model, trained by `train_model.py` on
`chennai_aqi_weather_merged.csv`, exactly reproducing Part 3 (cell 34) of
`Chennai_AQI_Full_Pipeline-2.ipynb`:

- **Algorithm**: RandomForestRegressor(n_estimators=300, max_depth=12, random_state=42)
- **Features**: AQI lags (1/2/3/7 days) + rolling 3/7-day means, today's
  weather (T2M, RH2M, WS2M, WD2M, PRECTOTCORR, PS), target day-of-week/
  month/is_weekend, and one-hot station dummies (21 features total).
- **Trained on**: all 2,918 historical daily readings across the 5 stations.

The bundle is a dict: `{"model", "feature_cols", "stations", "reduced_features"}`.

## Retraining

If you get fresh/updated historical data, just re-run:
```
python train_model.py
```
It overwrites `aqi_model.pkl` in place — no other code changes needed.
