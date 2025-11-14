"""
Fitness Nutrition Analysis Script
A comprehensive OOP-based analysis of Workout, Nutrition, and Health Metrics dataset
Author: Data Science Expert
"""

import os
import warnings
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import kagglehub
from dataclasses import dataclass
from typing import Dict, Optional

warnings.filterwarnings('ignore')
sns.set_style('whitegrid')
plt.rcParams['figure.dpi'] = 100


@dataclass
class Config:
    """Configuration class containing all constants and paths"""
    KAGGLE_DATASET: str = "zeesolver/final-dataset"
    OUTPUT_DIR: str = 'final_output'
    CHART_DIR: str = 'final_output/charts'
    PROCESSED_DATA_PATH: str = 'final_output/processed_data.csv'
    RAW_DATA_BACKUP_PATH: str = 'final_output/raw_data.csv'
    TARGET_COLUMN: str = 'Calories_Burned'
    NUMERIC_COLS: tuple = (
        'Age', 'Weight (kg)', 'Height (m)', 'Session_Duration (hours)',
        'Calories_Burned', 'Avg_BPM', 'Fat_Percentage', 'Water_Intake (liters)',
        'Workout_Frequency (days/week)'
    )
    CATEGORICAL_COLS: tuple = (
        'Gender', 'Workout_Type', 'Experience_Level'
    )


class OutputManager:
    """Manages output directory structure and file saving operations"""
    
    def __init__(self, chart_dir: str):
        self.chart_dir = chart_dir
    
    def setup_output_directories(self) -> None:
        """Create output directories if they don't exist"""
        os.makedirs(self.chart_dir, exist_ok=True)
        print(f"✓ Output directories created: {self.chart_dir}")
    
    def save_dataframe(self, df: pd.DataFrame, filename: str) -> None:
        """Save DataFrame to CSV file"""
        df.to_csv(filename, index=True)
        print(f"✓ Saved: {filename}")
    
    def save_plot(self, fig: plt.Figure, filename: str) -> None:
        """Save matplotlib figure to file"""
        fig.savefig(filename, bbox_inches='tight', dpi=300)
        plt.close(fig)
        print(f"✓ Saved: {filename}")


class DataIngestor:
    """Handles data loading and backup operations"""
    
    def load_data(self) -> pd.DataFrame:
        """Load data from Kaggle using kagglehub"""
        print("📥 Downloading dataset from Kaggle...")
        print(f"   Dataset: {Config.KAGGLE_DATASET}")
        
        try:
            # Download dataset using kagglehub
            path = kagglehub.dataset_download(Config.KAGGLE_DATASET)
            print(f"✓ Dataset downloaded to: {path}")
            
            # Find the CSV file in the downloaded path
            csv_files = []
            for root, dirs, files in os.walk(path):
                for file in files:
                    if file.endswith('.csv'):
                        csv_files.append(os.path.join(root, file))
            
            if not csv_files:
                raise FileNotFoundError(f"No CSV files found in downloaded dataset at {path}")
            
            # Use the first CSV file found (or the one matching expected name)
            data_file = csv_files[0]
            for csv_file in csv_files:
                if 'Final_data' in csv_file or 'final' in csv_file.lower():
                    data_file = csv_file
                    break
            
            print(f"✓ Loading data from: {os.path.basename(data_file)}")
            df = pd.read_csv(data_file)
            print(f"✓ Loaded data: {df.shape[0]} rows, {df.shape[1]} columns")
            
            return df
            
        except Exception as e:
            print(f"❌ Error loading data from Kaggle: {str(e)}")
            print("\n⚠️  Please ensure:")
            print("   1. You have kagglehub installed: pip install kagglehub")
            print("   2. Your Kaggle API credentials are configured")
            print("   3. You have internet connection")
            raise
    
    def backup_raw_data(self, df: pd.DataFrame, path: str) -> None:
        """Create backup of raw data"""
        df.to_csv(path, index=False)
        print(f"✓ Raw data backed up to: {path}")


class DataCleaner:
    """Handles all data cleaning operations"""
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Orchestrate all cleaning operations"""
        print("  → Handling missing values...")
        df = self._handle_missing_values(df)
        
        print("  → Correcting data types...")
        df = self._correct_data_types(df)
        
        print("  → Removing duplicates...")
        df = self._remove_duplicates(df)
        
        print("  → Capping outliers...")
        for col in ['Age', 'Weight (kg)', 'Height (m)', 'Avg_BPM']:
            if col in df.columns:
                df = self._cap_outliers(df, col)
        
        return df
    
    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Fill missing values: median for numeric, mode for categorical"""
        for col in Config.NUMERIC_COLS:
            if col in df.columns and df[col].isnull().any():
                df[col].fillna(df[col].median(), inplace=True)
        
        for col in Config.CATEGORICAL_COLS:
            if col in df.columns and df[col].isnull().any():
                mode_val = df[col].mode()[0] if not df[col].mode().empty else 'Unknown'
                df[col].fillna(mode_val, inplace=True)
        
        return df
    
    def _correct_data_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """Convert columns to appropriate data types"""
        for col in Config.NUMERIC_COLS:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        for col in Config.CATEGORICAL_COLS:
            if col in df.columns:
                df[col] = df[col].astype('category')
        
        return df
    
    def _remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove duplicate rows"""
        original_shape = df.shape[0]
        df = df.drop_duplicates()
        removed = original_shape - df.shape[0]
        if removed > 0:
            print(f"  → Removed {removed} duplicate rows")
        return df
    
    def _cap_outliers(self, df: pd.DataFrame, column: str) -> pd.DataFrame:
        """Cap outliers using IQR method"""
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        original_min = df[column].min()
        original_max = df[column].max()
        
        df[column] = df[column].clip(lower=lower_bound, upper=upper_bound)
        
        if original_min < lower_bound or original_max > upper_bound:
            print(f"  → Capped outliers in {column}: [{lower_bound:.2f}, {upper_bound:.2f}]")
        
        return df


class FeatureEngineer:
    """Creates new features from existing data"""
    
    def create_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate all engineered features"""
        # BMI
        df['BMI'] = df.apply(
            lambda row: row['Weight (kg)'] / (row['Height (m)'] ** 2) 
            if row['Height (m)'] > 0 else np.nan,
            axis=1
        )
        
        # Age Group
        df['Age_Group'] = pd.cut(
            df['Age'],
            bins=[0, 25, 35, 45, 55, 100],
            labels=['18-25', '26-35', '36-45', '46-55', '55+']
        )
        
        # Session Duration in Minutes
        df['Session_Duration_Minutes'] = df['Session_Duration (hours)'] * 60
        
        # Calories Burned Per Minute
        df['Calories_Burned_Per_Minute'] = df.apply(
            lambda row: row['Calories_Burned'] / row['Session_Duration_Minutes']
            if row['Session_Duration_Minutes'] > 0 else 0,
            axis=1
        )
        
        print(f"✓ Created 4 new features: BMI, Age_Group, Session_Duration_Minutes, Calories_Burned_Per_Minute")
        
        return df


class DataExplorer:
    """Performs exploratory data analysis"""
    
    def get_descriptive_stats(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate descriptive statistics"""
        return df.describe(include='all')
    
    def calculate_correlation(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate correlation matrix for numeric columns"""
        return df.select_dtypes(include=[np.number]).corr()
    
    def perform_group_analysis(self, df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """Perform various group-by analyses"""
        results = {}
        
        # Workout Type Summary
        results['workout_summary'] = df.groupby('Workout_Type')['Calories_Burned'].agg([
            'count', 'mean', 'std', 'min', 'max'
        ]).round(2).sort_values('mean', ascending=False)
        
        # Intensity Ranking (Calories per Minute)
        results['intensity_ranking'] = df.groupby('Workout_Type')['Calories_Burned_Per_Minute'].agg([
            'mean', 'median'
        ]).round(3).sort_values('mean', ascending=False)
        
        # Gender Analysis
        results['gender_summary'] = df.groupby('Gender')['Calories_Burned'].agg([
            'count', 'mean', 'std'
        ]).round(2)
        
        # Age Group Analysis
        results['age_group_summary'] = df.groupby('Age_Group')['Calories_Burned'].agg([
            'count', 'mean', 'median'
        ]).round(2)
        
        # Interaction: Workout Type × Gender
        results['workout_gender_interaction'] = df.groupby(
            ['Workout_Type', 'Gender']
        )['Calories_Burned'].mean().unstack().round(2)
        
        # Experience Level Analysis
        if 'Experience_Level' in df.columns:
            results['experience_summary'] = df.groupby('Experience_Level')['Calories_Burned'].agg([
                'count', 'mean', 'median'
            ]).round(2)
        
        print(f"✓ Completed {len(results)} group analyses")
        
        return results


class Visualizer:
    """Handles all visualization generation"""
    
    def __init__(self, output_manager: OutputManager):
        self.output_manager = output_manager
    
    def create_summary_dashboard(self, df: pd.DataFrame, corr_matrix: pd.DataFrame, filename: str) -> None:
        """Create comprehensive summary dashboard with 4 key visualizations"""
        fig, axes = plt.subplots(2, 2, figsize=(18, 12))
        fig.suptitle('Fitness Performance Analysis Dashboard', fontsize=20, fontweight='bold', y=0.995)
        
        # Subplot 1: Calories Burned Distribution (Histogram with KDE)
        axes[0, 0].hist(df['Calories_Burned'], bins=50, color='steelblue', alpha=0.7, edgecolor='black')
        ax_twin = axes[0, 0].twinx()
        df['Calories_Burned'].plot(kind='kde', ax=ax_twin, color='red', linewidth=2.5)
        
        axes[0, 0].set_xlabel('Calories Burned', fontsize=11, fontweight='bold')
        axes[0, 0].set_ylabel('Frequency', fontsize=11, fontweight='bold')
        ax_twin.set_ylabel('Density', fontsize=11, fontweight='bold', color='red')
        axes[0, 0].set_title('Calories Burned Distribution', fontsize=14, fontweight='bold')
        axes[0, 0].grid(axis='y', alpha=0.3)
        
        # Add statistics
        mean_cal = df['Calories_Burned'].mean()
        median_cal = df['Calories_Burned'].median()
        axes[0, 0].axvline(mean_cal, color='green', linestyle='--', linewidth=2, label=f'Mean: {mean_cal:.0f}')
        axes[0, 0].axvline(median_cal, color='orange', linestyle='--', linewidth=2, label=f'Median: {median_cal:.0f}')
        axes[0, 0].legend(loc='upper right', fontsize=9)
        
        # Subplot 2: Average BPM vs Calories (Hexbin for density)
        hexbin = axes[0, 1].hexbin(df['Avg_BPM'], df['Calories_Burned'], 
                                   gridsize=25, cmap='YlOrRd', mincnt=1)
        axes[0, 1].set_xlabel('Average BPM', fontsize=11, fontweight='bold')
        axes[0, 1].set_ylabel('Calories Burned', fontsize=11, fontweight='bold')
        axes[0, 1].set_title('Heart Rate vs Calories Burned (Density)', fontsize=14, fontweight='bold')
        cb = plt.colorbar(hexbin, ax=axes[0, 1])
        cb.set_label('Count', fontsize=10)
        axes[0, 1].grid(alpha=0.3)
        
        # Subplot 3: Workout Performance Comparison (Grouped Bar Chart)
        workout_stats = df.groupby('Workout_Type').agg({
            'Calories_Burned': 'mean',
            'Session_Duration_Minutes': 'mean',
            'Avg_BPM': 'mean'
        }).round(1)
        
        # Normalize for better visualization
        workout_stats_norm = workout_stats.copy()
        workout_stats_norm['Calories_Burned'] = workout_stats_norm['Calories_Burned'] / 10
        workout_stats_norm['Session_Duration_Minutes'] = workout_stats_norm['Session_Duration_Minutes']
        workout_stats_norm['Avg_BPM'] = workout_stats_norm['Avg_BPM']
        
        x = np.arange(len(workout_stats_norm.index))
        width = 0.25
        
        bars1 = axes[1, 0].bar(x - width, workout_stats_norm['Calories_Burned'], width, 
                              label='Calories (÷10)', color='#FF6B6B', alpha=0.8)
        bars2 = axes[1, 0].bar(x, workout_stats_norm['Session_Duration_Minutes'], width, 
                              label='Duration (min)', color='#4ECDC4', alpha=0.8)
        bars3 = axes[1, 0].bar(x + width, workout_stats_norm['Avg_BPM'], width, 
                              label='BPM', color='#FFA07A', alpha=0.8)
        
        axes[1, 0].set_xlabel('Workout Type', fontsize=11, fontweight='bold')
        axes[1, 0].set_ylabel('Normalized Values', fontsize=11, fontweight='bold')
        axes[1, 0].set_title('Workout Performance Metrics Comparison', fontsize=14, fontweight='bold')
        axes[1, 0].set_xticks(x)
        axes[1, 0].set_xticklabels(workout_stats_norm.index, rotation=45, ha='right')
        axes[1, 0].legend(loc='upper left', fontsize=9)
        axes[1, 0].grid(axis='y', alpha=0.3)
        
        # Add value labels on bars
        for bars in [bars1, bars2, bars3]:
            for bar in bars:
                height = bar.get_height()
                axes[1, 0].text(bar.get_x() + bar.get_width()/2., height,
                              f'{height:.0f}', ha='center', va='bottom', fontsize=7)
        
        # Subplot 4: Gender vs Workout Type Performance Heatmap
        gender_workout = df.pivot_table(
            values='Calories_Burned', 
            index='Gender', 
            columns='Workout_Type', 
            aggfunc='mean'
        )
        
        im = axes[1, 1].imshow(gender_workout.values, cmap='RdYlGn', aspect='auto')
        
        # Set ticks
        axes[1, 1].set_xticks(np.arange(len(gender_workout.columns)))
        axes[1, 1].set_yticks(np.arange(len(gender_workout.index)))
        axes[1, 1].set_xticklabels(gender_workout.columns, rotation=45, ha='right')
        axes[1, 1].set_yticklabels(gender_workout.index)
        
        # Add text annotations
        for i in range(len(gender_workout.index)):
            for j in range(len(gender_workout.columns)):
                text = axes[1, 1].text(j, i, f'{gender_workout.values[i, j]:.0f}',
                                      ha="center", va="center", color="black", 
                                      fontsize=11, fontweight='bold')
        
        axes[1, 1].set_title('Calories by Gender × Workout Type', fontsize=14, fontweight='bold')
        cbar = plt.colorbar(im, ax=axes[1, 1])
        cbar.set_label('Avg Calories', fontsize=10)
        
        plt.tight_layout()
        self.output_manager.save_plot(fig, filename)
    
    def create_advanced_insights_dashboard(self, df: pd.DataFrame, grouped_stats: Dict[str, pd.DataFrame], filename: str) -> None:
        """Create fitness insights dashboard with business-oriented visualizations"""
        fig = plt.figure(figsize=(18, 10))
        gs = fig.add_gridspec(2, 2, hspace=0.35, wspace=0.3)
        fig.suptitle('Fitness Insights Dashboard', fontsize=22, fontweight='bold', y=0.98)
        
        # 1. ENHANCED Workout Intensity Ranking (Top performers with values)
        ax1 = fig.add_subplot(gs[0, :])  # Span full width for emphasis
        intensity = grouped_stats['intensity_ranking'].head(7).sort_values('mean')
        
        # Create gradient colors from low to high
        colors = plt.cm.RdYlGn(np.linspace(0.3, 0.9, len(intensity)))
        bars = ax1.barh(intensity.index, intensity['mean'], color=colors, alpha=0.85, edgecolor='black', linewidth=1.5)
        
        # Add value labels on bars
        for i, (idx, row) in enumerate(intensity.iterrows()):
            ax1.text(row['mean'] + 0.15, i, f"{row['mean']:.2f} cal/min", 
                    va='center', fontsize=11, fontweight='bold')
            # Add median as vertical line
            ax1.plot([row['median'], row['median']], [i-0.3, i+0.3], 
                    color='darkblue', linewidth=2, alpha=0.7)
        
        ax1.set_xlabel('Calories Burned per Minute', fontsize=12, fontweight='bold')
        ax1.set_title('🔥 Workout Intensity Ranking - Calories Burned per Minute', 
                     fontsize=14, fontweight='bold', pad=15)
        ax1.grid(axis='x', alpha=0.4, linestyle='--')
        ax1.set_xlim(0, max(intensity['mean']) * 1.15)
        
        # Add legend for median line
        from matplotlib.lines import Line2D
        legend_elements = [Line2D([0], [0], color='darkblue', linewidth=2, label='Median')]
        ax1.legend(handles=legend_elements, loc='lower right', fontsize=10)
        
        # 2. BMI Distribution by Gender (Enhanced with stats)
        ax2 = fig.add_subplot(gs[1, 0])
        violin_parts = ax2.violinplot([df[df['Gender']=='Female']['BMI'].dropna(),
                                       df[df['Gender']=='Male']['BMI'].dropna()],
                                      positions=[0, 1], showmeans=True, showmedians=True)
        
        # Color violins
        colors_violin = ['#66c2a5', '#fc8d62']
        for pc, color in zip(violin_parts['bodies'], colors_violin):
            pc.set_facecolor(color)
            pc.set_alpha(0.7)
        
        ax2.set_xticks([0, 1])
        ax2.set_xticklabels(['Female', 'Male'], fontsize=11)
        ax2.set_ylabel('BMI', fontsize=11, fontweight='bold')
        ax2.set_title('📊 BMI Distribution by Gender', fontsize=13, fontweight='bold')
        ax2.grid(axis='y', alpha=0.3)
        
        # Add mean values as text
        female_mean = df[df['Gender']=='Female']['BMI'].mean()
        male_mean = df[df['Gender']=='Male']['BMI'].mean()
        ax2.text(0, female_mean + 2, f'μ={female_mean:.1f}', ha='center', fontsize=10, fontweight='bold')
        ax2.text(1, male_mean + 2, f'μ={male_mean:.1f}', ha='center', fontsize=10, fontweight='bold')
        
        # 3. Workout Type × Gender Heatmap
        ax3 = fig.add_subplot(gs[1, 1])
        interaction_data = grouped_stats['workout_gender_interaction']
        sns.heatmap(interaction_data.T, annot=True, fmt='.0f', cmap='YlOrRd', ax=ax3, 
                   cbar_kws={'label': 'Avg Calories'}, linewidths=1, linecolor='white')
        ax3.set_title('🔥 Workout × Gender Performance', fontsize=13, fontweight='bold')
        ax3.set_xlabel('Workout Type', fontsize=11, fontweight='bold')
        ax3.set_ylabel('Gender', fontsize=11, fontweight='bold')
        plt.setp(ax3.get_xticklabels(), rotation=45, ha='right')
        
        self.output_manager.save_plot(fig, filename)


class FitnessDataAnalyzer:
    """Main orchestrator class that coordinates the entire analysis pipeline"""
    
    def __init__(self):
        self.config = Config()
        self.output_manager = OutputManager(self.config.CHART_DIR)
        self.ingestor = DataIngestor()
        self.cleaner = DataCleaner()
        self.feature_engineer = FeatureEngineer()
        self.explorer = DataExplorer()
        self.visualizer = Visualizer(self.output_manager)
    
    def run_analysis(self) -> None:
        """Execute the complete analysis pipeline"""
        print("\n" + "="*70)
        print("  FITNESS & NUTRITION DATA ANALYSIS PIPELINE")
        print("="*70 + "\n")
        
        # Step 1: Setup
        print("[1/6] Setting up output directories...")
        self.output_manager.setup_output_directories()
        
        # Step 2: Data Loading
        print("\n[2/6] Loading data...")
        raw_df = self.ingestor.load_data()
        self.ingestor.backup_raw_data(raw_df, self.config.RAW_DATA_BACKUP_PATH)
        
        # Step 3: Data Cleaning
        print("\n[3/6] Cleaning data...")
        clean_df = self.cleaner.clean_data(raw_df.copy())
        
        # Step 4: Feature Engineering
        print("\n[4/6] Engineering features...")
        featured_df = self.feature_engineer.create_features(clean_df)
        self.output_manager.save_dataframe(featured_df, self.config.PROCESSED_DATA_PATH)
        
        # Step 5: Data Exploration
        print("\n[5/6] Running data exploration...")
        
        # Correlation Analysis
        corr_matrix = self.explorer.calculate_correlation(featured_df)
        
        # Group Analyses
        grouped_stats = self.explorer.perform_group_analysis(featured_df)
        
        # Step 6: Visualizations
        print("\n[6/6] Generating visualizations...")
        
        # Core comprehensive dashboards only
        print("  → Creating summary dashboard...")
        self.visualizer.create_summary_dashboard(featured_df, corr_matrix,
                                                f"{self.config.CHART_DIR}/summary_dashboard.png")
        
        print("  → Creating fitness insights dashboard...")
        self.visualizer.create_advanced_insights_dashboard(featured_df, grouped_stats,
                                                           f"{self.config.CHART_DIR}/fitness_insights_dashboard.png")
        
        # Final Summary
        print("\n" + "="*70)
        print("  ✓ ANALYSIS COMPLETE")
        print("="*70)
        print(f"\nAll outputs saved to '{self.config.OUTPUT_DIR}' folder:")
        print(f"  • Charts: {self.config.CHART_DIR}/")
        print(f"  • Processed Data: {self.config.PROCESSED_DATA_PATH}")
        
        # Key Findings
        self._print_key_findings(featured_df, corr_matrix, grouped_stats)
    
    def _print_key_findings(self, df: pd.DataFrame, corr: pd.DataFrame, 
                           grouped: Dict[str, pd.DataFrame]) -> None:
        """Print key findings from the analysis"""
        print("\n" + "="*70)
        print("  KEY FINDINGS")
        print("="*70 + "\n")
        
        # Finding 1: Correlation insights
        target_corr = corr[self.config.TARGET_COLUMN].drop(self.config.TARGET_COLUMN).sort_values(ascending=False)
        top_correlates = target_corr.head(3)
        print("1. STRONGEST PREDICTORS OF CALORIES BURNED:")
        for feature, corr_val in top_correlates.items():
            print(f"   • {feature}: {corr_val:.3f} correlation")
        
        # Finding 2: Workout intensity ranking
        print("\n2. WORKOUT INTENSITY RANKING (Calories/Minute):")
        intensity = grouped['intensity_ranking'].head(3)
        for idx, (workout, row) in enumerate(intensity.iterrows(), 1):
            print(f"   {idx}. {workout}: {row['mean']:.3f} cal/min (median: {row['median']:.3f})")
        
        # Finding 3: Gender differences
        print("\n3. GENDER ANALYSIS:")
        gender_summary = grouped['gender_summary']
        for gender, row in gender_summary.iterrows():
            print(f"   • {gender}: {row['mean']:.1f} ± {row['std']:.1f} calories (n={int(row['count'])})")
        
        # Finding 4: Age group insights
        print("\n4. AGE GROUP PERFORMANCE:")
        age_summary = grouped['age_group_summary'].sort_values('mean', ascending=False).head(3)
        for age_group, row in age_summary.iterrows():
            print(f"   • {age_group} years: {row['mean']:.1f} calories (median: {row['median']:.1f})")
        
        print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    # Initialize and run the analysis
    analyzer = FitnessDataAnalyzer()
    analyzer.run_analysis()
