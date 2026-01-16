"""
XGBoost Model Training
Train a gradient boosting model to predict PEC footfall
"""

import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split, TimeSeriesSplit
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, mean_absolute_percentage_error
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os
from datetime import datetime

class PECDemandModel:
    """XGBoost-based PEC demand forecasting model"""
    
    def __init__(self):
        self.model = None
        self.feature_names = None
        self.training_date = None
        
    def train_model(self, input_path='data/processed/pec_features.csv',
                   model_dir='models', test_size=0.2):
        """
        Train XGBoost model on processed features
        
        Args:
            input_path: Path to processed features CSV
            model_dir: Directory to save trained model
            test_size: Proportion of data for testing (time-based split)
        """
        print("🤖 Starting XGBoost Model Training...")
        print("=" * 60)
        
        # Load processed data
        df = pd.read_csv(input_path)
        df['date'] = pd.to_datetime(df['date'])
        
        print(f"📊 Loaded {len(df):,} records")
        
        # Prepare features and target
        X, y, feature_names = self._prepare_data(df)
        self.feature_names = feature_names
        
        # Time-based train-test split (important for time series)
        split_index = int(len(df) * (1 - test_size))
        split_date = df.iloc[split_index]['date']
        
        X_train = X[:split_index]
        X_test = X[split_index:]
        y_train = y[:split_index]
        y_test = y[split_index:]
        
        print(f"\n📅 Train period: {df.iloc[0]['date'].date()} to {df.iloc[split_index-1]['date'].date()}")
        print(f"📅 Test period:  {split_date.date()} to {df.iloc[-1]['date'].date()}")
        print(f"📊 Train samples: {len(X_train):,}")
        print(f"📊 Test samples:  {len(X_test):,}")
        
        # Train XGBoost model
        print("\n🚀 Training XGBoost model...")
        self.model = self._train_xgboost(X_train, y_train, X_test, y_test)
        
        # Evaluate on test set
        print("\n📊 Model Evaluation on Test Set:")
        self._evaluate_model(X_test, y_test)
        
        # Feature importance analysis
        print("\n🔍 Top 15 Most Important Features:")
        self._plot_feature_importance(save_dir=model_dir)
        
        # Save model
        self._save_model(model_dir)
        
        # Generate predictions vs actuals plot
        self._plot_predictions(X_test, y_test, df.iloc[split_index:], save_dir=model_dir)
        
        print("\n✅ Model training complete!")
        
        return self.model
    
    def _prepare_data(self, df):
        """Prepare features and target variable"""
        
        # Features to EXCLUDE from training
        exclude_cols = [
            'date', 'footfall',  # Target and date
            'pincode', 'district', 'state', 'center_type',  # Already encoded
            'day_name',  # Redundant with day_of_week
            'footfall_change_7d', 'footfall_change_30d'  # Can cause issues with NaN
        ]
        
        # Select feature columns
        feature_cols = [col for col in df.columns if col not in exclude_cols]
        
        # Prepare X and y
        X = df[feature_cols].copy()
        y = df['footfall'].values
        
        print(f"🔢 Using {len(feature_cols)} features for training")
        
        return X, y, feature_cols
    
    def _train_xgboost(self, X_train, y_train, X_test, y_test):
        """Train XGBoost regressor with optimal parameters"""
        
        # XGBoost parameters (tuned for this problem)
        params = {
            'objective': 'reg:squarederror',
            'max_depth': 8,
            'learning_rate': 0.05,
            'n_estimators': 500,
            'subsample': 0.8,
            'colsample_bytree': 0.8,
            'min_child_weight': 3,
            'gamma': 0.1,
            'reg_alpha': 0.01,  # L1 regularization
            'reg_lambda': 1.0,  # L2 regularization
            'random_state': 42,
            'n_jobs': -1,
            'enable_categorical': True  # Handle categorical features
        }
        
        # Create and train model with early stopping
        model = xgb.XGBRegressor(**params)
        
        model.fit(
            X_train, y_train,
            eval_set=[(X_train, y_train), (X_test, y_test)],
            verbose=50
        )
        
        return model
    
    def _evaluate_model(self, X_test, y_test):
        """Calculate and display evaluation metrics"""
        
        # Make predictions
        y_pred = self.model.predict(X_test)
        
        # Calculate metrics and store as instance variables
        self.mae = mean_absolute_error(y_test, y_pred)
        self.rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        self.r2 = r2_score(y_test, y_pred)
        self.mape = mean_absolute_percentage_error(y_test, y_pred) * 100
        
        # Display metrics
        print(f"  ├─ MAE (Mean Absolute Error):  {self.mae:.2f} residents")
        print(f"  ├─ RMSE (Root Mean Sq Error):  {self.rmse:.2f} residents")
        print(f"  ├─ R² Score:                   {self.r2:.4f}")
        print(f"  └─ MAPE (Mean Abs % Error):    {self.mape:.2f}%")
        
        # Interpretation
        print("\n💡 Model Interpretation:")
        print(f"  • On average, predictions are off by ±{self.mae:.0f} residents")
        print(f"  • Model explains {self.r2*100:.1f}% of demand variance")
        if self.mape < 15:
            print(f"  • MAPE of {self.mape:.1f}% indicates EXCELLENT accuracy ✅")
        elif self.mape < 25:
            print(f"  • MAPE of {self.mape:.1f}% indicates GOOD accuracy 👍")
        else:
            print(f"  • MAPE of {self.mape:.1f}% suggests room for improvement 📈")
    
    def _plot_feature_importance(self, save_dir='models', top_n=15):
        """Plot and save feature importance"""
        
        # Get feature importance
        importance_df = pd.DataFrame({
            'feature': self.feature_names,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        # Print top features
        for i, row in importance_df.head(top_n).iterrows():
            print(f"  {row['feature']:35s} {row['importance']:.4f}")
        
        # Create plot
        plt.figure(figsize=(10, 8))
        sns.barplot(
            data=importance_df.head(top_n),
            y='feature',
            x='importance',
            palette='viridis'
        )
        plt.title('Top 15 Feature Importance (XGBoost)', fontsize=14, fontweight='bold')
        plt.xlabel('Importance Score', fontsize=12)
        plt.ylabel('Feature', fontsize=12)
        plt.tight_layout()
        
        # Save plot
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, 'feature_importance.png')
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"\n📊 Feature importance plot saved to: {save_path}")
    
    def _plot_predictions(self, X_test, y_test, test_df, save_dir='models'):
        """Plot predicted vs actual footfall"""
        
        y_pred = self.model.predict(X_test)
        
        # Create figure with two subplots
        fig, axes = plt.subplots(2, 1, figsize=(14, 10))
        
        # Subplot 1: Time series of predictions vs actuals
        dates = test_df['date'].values
        axes[0].plot(dates, y_test, label='Actual', color='#2E86AB', linewidth=2, alpha=0.7)
        axes[0].plot(dates, y_pred, label='Predicted', color='#A23B72', linewidth=2, alpha=0.7)
        axes[0].fill_between(dates, y_test, y_pred, alpha=0.2, color='gray')
        axes[0].set_xlabel('Date', fontsize=12)
        axes[0].set_ylabel('Footfall', fontsize=12)
        axes[0].set_title('Predicted vs Actual Footfall Over Time', fontsize=14, fontweight='bold')
        axes[0].legend(fontsize=10)
        axes[0].grid(True, alpha=0.3)
        
        # Subplot 2: Scatter plot (predicted vs actual)
        axes[1].scatter(y_test, y_pred, alpha=0.5, s=20, color='#2E86AB')
        
        # Perfect prediction line
        min_val = min(y_test.min(), y_pred.min())
        max_val = max(y_test.max(), y_pred.max())
        axes[1].plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=2, label='Perfect Prediction')
        
        axes[1].set_xlabel('Actual Footfall', fontsize=12)
        axes[1].set_ylabel('Predicted Footfall', fontsize=12)
        axes[1].set_title('Prediction Accuracy Scatter Plot', fontsize=14, fontweight='bold')
        axes[1].legend(fontsize=10)
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Save plot
        save_path = os.path.join(save_dir, 'predictions_vs_actual.png')
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"📊 Predictions plot saved to: {save_path}")
    
    def _save_model(self, model_dir='models'):
        """Save trained model and metadata"""
        
        os.makedirs(model_dir, exist_ok=True)
        
        # Save XGBoost model
        model_path = os.path.join(model_dir, 'pec_demand_model.json')
        self.model.save_model(model_path)
        
        # Save metadata (feature names and metrics)
        metadata = {
            'feature_names': self.feature_names,
            'training_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'train_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'model_type': 'XGBoost Regressor',
            'mae': self.mae,
            'rmse': self.rmse,
            'r2_score': self.r2,
            'mape': self.mape
        }
        metadata_path = os.path.join(model_dir, 'model_metadata.pkl')
        joblib.dump(metadata, metadata_path)
        
        print(f"\n💾 Model saved to: {model_path}")
        print(f"💾 Metadata saved to: {metadata_path}")

def main():
    """Main execution function"""
    print("🏛️  PEC Demand Forecasting - Model Training")
    print("=" * 60)
    
    trainer = PECDemandModel()
    
    # Train the model
    model = trainer.train_model()
    
    print("\n✨ Training pipeline complete!")

if __name__ == "__main__":
    main()
