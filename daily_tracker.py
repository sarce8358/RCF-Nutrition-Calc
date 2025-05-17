import streamlit as st
import pandas as pd
from datetime import date, timedelta
import plotly.express as px

# Import local modules
from data.food_database import food_database
from utils.calculator import calculate_nutrients, calculate_percent_daily_values, calculate_points
from utils.visualization import create_nutrition_chart, create_daily_progress_chart, create_nutrition_history_chart

def app():
    st.title("📊 Daily Nutrition Tracker")
    st.write("Track your daily nutrition intake and view your progress over time")
    
    # Initialize session state variables if not present
    if 'daily_log' not in st.session_state:
        st.session_state.daily_log = {}
        
    if 'current_date' not in st.session_state:
        st.session_state.current_date = str(date.today())
    
    # Date selection
    selected_date = st.date_input("Select date:", value=date.today())
    st.session_state.current_date = str(selected_date)
    
    # Display daily log for selected date
    if st.session_state.current_date in st.session_state.daily_log and st.session_state.daily_log[st.session_state.current_date]:
        st.subheader(f"Foods logged for {st.session_state.current_date}")
        
        # Convert daily log for the selected date to DataFrame
        daily_foods = st.session_state.daily_log[st.session_state.current_date]
        daily_df = pd.DataFrame(daily_foods)
        
        # Format the DataFrame for display
        display_df = daily_df.copy()
        if not display_df.empty:
            # Round numeric columns
            numeric_cols = ['quantity', 'calories', 'protein', 'carbs', 'fat']
            for col in numeric_cols:
                if col in display_df.columns:
                    display_df[col] = display_df[col].round(1)
        
        # Select columns to display
        display_cols = ["food", "quantity", "calories", "protein", "carbs", "fat"]
        
        # Add category and subcategory if available
        if "category" in display_df.columns:
            display_cols.append("category")
            
        if "subcategory" in display_df.columns and not display_df["subcategory"].isnull().all():
            display_cols.append("subcategory")
            
        # Display the table with selected columns
        st.dataframe(display_df[display_cols])
        
        # Option to remove items
        if st.button("Remove Last Item"):
            if st.session_state.daily_log[st.session_state.current_date]:
                st.session_state.daily_log[st.session_state.current_date].pop()
                st.success("Removed last food item")
                st.rerun()
        
        # Calculate daily nutrients
        daily_totals = calculate_nutrients(daily_foods)
        
        # Calculate daily points
        daily_points = calculate_points(daily_totals)
        
        st.subheader("Daily Nutritional Summary")
        
        # Create columns for the nutritional summary
        col_prot, col_carbs, col_fat, col_cal, col_points = st.columns(5)
        
        with col_prot:
            st.metric("Daily Protein", f"{daily_totals['protein']:.1f} g")
            
        with col_carbs:
            st.metric("Daily Carbs", f"{daily_totals['carbs']:.1f} g")
            
        with col_fat:
            st.metric("Daily Fat", f"{daily_totals['fat']:.1f} g")
            
        with col_cal:
            st.metric("Daily Calories", f"{daily_totals['calories']:.1f} kcal")
            
        with col_points:
            st.metric("Daily Points", f"{daily_points:.1f}")
        
        # Clear daily log button
        if st.button("Clear Daily Log"):
            st.session_state.daily_log[st.session_state.current_date] = []
            st.success(f"Cleared log for {st.session_state.current_date}")
            st.rerun()
    else:
        st.info(f"No foods logged for {st.session_state.current_date}. Add foods to your daily log from the calculator.")
        
        # Add sample data button (for demonstration)
        if st.button("Add Sample Data for Today"):
            if st.session_state.current_date not in st.session_state.daily_log:
                st.session_state.daily_log[st.session_state.current_date] = []
            
            # Add some sample foods with categories
            sample_foods = [
                {
                    "food": "Oatmeal (Cooked)",
                    "quantity": 200,
                    "calories": food_database["Oatmeal (Cooked)"]["calories"] * 2,
                    "protein": food_database["Oatmeal (Cooked)"]["protein"] * 2,
                    "carbs": food_database["Oatmeal (Cooked)"]["carbs"] * 2,
                    "fat": food_database["Oatmeal (Cooked)"]["fat"] * 2,
                    "category": food_database["Oatmeal (Cooked)"]["category"],
                    "subcategory": food_database["Oatmeal (Cooked)"]["subcategory"]
                },
                {
                    "food": "Banana",
                    "quantity": 120,
                    "calories": food_database["Banana"]["calories"] * 1.2,
                    "protein": food_database["Banana"]["protein"] * 1.2,
                    "carbs": food_database["Banana"]["carbs"] * 1.2,
                    "fat": food_database["Banana"]["fat"] * 1.2,
                    "category": food_database["Banana"]["category"],
                    "subcategory": food_database["Banana"]["subcategory"]
                },
                {
                    "food": "Chicken Breast",
                    "quantity": 150,
                    "calories": food_database["Chicken Breast"]["calories"] * 1.5,
                    "protein": food_database["Chicken Breast"]["protein"] * 1.5,
                    "carbs": food_database["Chicken Breast"]["carbs"] * 1.5,
                    "fat": food_database["Chicken Breast"]["fat"] * 1.5,
                    "category": food_database["Chicken Breast"]["category"]
                },
                {
                    "food": "Avocado",
                    "quantity": 50,
                    "calories": food_database["Avocado"]["calories"] * 0.5,
                    "protein": food_database["Avocado"]["protein"] * 0.5,
                    "carbs": food_database["Avocado"]["carbs"] * 0.5,
                    "fat": food_database["Avocado"]["fat"] * 0.5,
                    "category": food_database["Avocado"]["category"]
                },
                {
                    "food": "Broccoli",
                    "quantity": 100,
                    "calories": food_database["Broccoli"]["calories"],
                    "protein": food_database["Broccoli"]["protein"],
                    "carbs": food_database["Broccoli"]["carbs"],
                    "fat": food_database["Broccoli"]["fat"],
                    "category": food_database["Broccoli"]["category"],
                    "subcategory": food_database["Broccoli"]["subcategory"]
                }
            ]
            
            st.session_state.daily_log[st.session_state.current_date].extend(sample_foods)
            st.success("Added sample data for today")
            st.rerun()
    
    # Footer
    st.markdown("---")
    st.caption("Made by S. RC for RCF")
    
    # Daily nutrition targets
    st.header("Set Daily Nutrition Targets")
    
    col1, col2 = st.columns(2)
    
    with col1:
        target_calories = st.number_input("Target Calories (kcal):", 
                                         min_value=500, 
                                         max_value=5000, 
                                         value=st.session_state.get('target_calories', 2000))
    
    with col2:
        target_protein = st.number_input("Target Protein (g):", 
                                        min_value=10, 
                                        max_value=300, 
                                        value=st.session_state.get('target_protein', 50))
    
    with col1:
        target_carbs = st.number_input("Target Carbohydrates (g):", 
                                      min_value=50, 
                                      max_value=500, 
                                      value=st.session_state.get('target_carbs', 275))
    
    with col2:
        target_fat = st.number_input("Target Fat (g):", 
                                    min_value=10, 
                                    max_value=200, 
                                    value=st.session_state.get('target_fat', 78))
    
    # Save button
    if st.button("Save Targets"):
        st.session_state.target_calories = target_calories
        st.session_state.target_protein = target_protein
        st.session_state.target_carbs = target_carbs
        st.session_state.target_fat = target_fat
        st.success("Saved your nutrition targets")
    
    # Button to return to main page
    if st.button("Return to Calculator"):
        st.switch_page("app.py")

# This allows the page to be run directly
if __name__ == "__main__":
    app()
