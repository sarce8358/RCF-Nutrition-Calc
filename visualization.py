import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def create_nutrition_chart(totals):
    """
    Create a pie chart showing the breakdown of macronutrients
    
    Args:
        totals (dict): Dictionary containing total nutritional values
        
    Returns:
        plotly.graph_objects.Figure: Pie chart figure
    """
    # Calculate calories from each macronutrient
    protein_calories = totals["protein"] * 4  # 4 calories per gram of protein
    carb_calories = totals["carbs"] * 4       # 4 calories per gram of carbs
    fat_calories = totals["fat"] * 9          # 9 calories per gram of fat
    
    # Create data for pie chart
    labels = ['Protein', 'Carbohydrates', 'Fat']
    values = [protein_calories, carb_calories, fat_calories]
    colors = ['#4CAF50', '#2196F3', '#FFC107']
    
    # Calculate percentages
    total_calories = sum(values)
    if total_calories > 0:
        percentages = [round((value / total_calories) * 100, 1) for value in values]
        custom_labels = [f"{labels[i]} ({percentages[i]}%)" for i in range(len(labels))]
    else:
        custom_labels = labels
    
    # Create pie chart
    fig = px.pie(
        names=custom_labels,
        values=values,
        color_discrete_sequence=colors,
        hole=0.4,
    )
    
    # Update layout
    fig.update_layout(
        margin=dict(l=20, r=20, t=30, b=20),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.1,
            xanchor="center",
            x=0.5
        ),
        height=300,
    )
    
    # Add annotation in the center
    fig.update_traces(textinfo='percent+label')
    fig.add_annotation(
        text=f"{int(total_calories)} kcal",
        x=0.5,
        y=0.5,
        font_size=15,
        showarrow=False
    )
    
    return fig

def create_daily_progress_chart(daily_totals, reference_values=None):
    """
    Create a bar chart showing progress toward daily nutrition goals
    
    Args:
        daily_totals (dict): Dictionary containing total nutritional values for the day
        reference_values (dict, optional): Reference daily intake values
        
    Returns:
        plotly.graph_objects.Figure: Bar chart figure
    """
    # Default reference values based on a 2000 calorie diet
    if reference_values is None:
        reference_values = {
            "calories": 2000,
            "protein": 50,    # g
            "carbs": 275,     # g
            "fat": 78         # g
        }
    
    # Calculate percentages of daily goals
    percentages = {}
    for nutrient, total in daily_totals.items():
        if nutrient in reference_values and reference_values[nutrient] > 0:
            percentages[nutrient] = min(100, (total / reference_values[nutrient]) * 100)
        else:
            percentages[nutrient] = 0
    
    # Create data for bar chart
    nutrients = ['Calories', 'Protein', 'Carbohydrates', 'Fat']
    values = [
        percentages.get('calories', 0),
        percentages.get('protein', 0),
        percentages.get('carbs', 0),
        percentages.get('fat', 0)
    ]
    
    # Create horizontal bar chart
    fig = go.Figure()
    
    # Add progress bars
    fig.add_trace(go.Bar(
        x=values,
        y=nutrients,
        orientation='h',
        marker=dict(
            color=['#FF9800', '#4CAF50', '#2196F3', '#FFC107'],
        ),
        text=[f"{v:.1f}%" for v in values],
        textposition='auto',
    ))
    
    # Update layout
    fig.update_layout(
        title="Progress Toward Daily Goals",
        xaxis=dict(
            title="Percentage of Daily Goal",
            range=[0, 100],
            tickvals=[0, 25, 50, 75, 100],
            ticktext=['0%', '25%', '50%', '75%', '100%'],
        ),
        yaxis=dict(
            title="Nutrient"
        ),
        height=300,
        margin=dict(l=20, r=20, t=40, b=20),
    )
    
    # Add a vertical line at 100%
    fig.add_shape(
        type="line",
        x0=100, y0=-0.5,
        x1=100, y1=3.5,
        line=dict(
            color="gray",
            width=2,
            dash="dash",
        )
    )
    
    return fig

def create_nutrition_history_chart(daily_log, nutrient='calories'):
    """
    Create a line chart showing the history of a nutrient over time
    
    Args:
        daily_log (dict): Dictionary containing daily food logs
        nutrient (str): Nutrient to display ('calories', 'protein', 'carbs', 'fat')
        
    Returns:
        plotly.graph_objects.Figure: Line chart figure
    """
    # Extract dates and nutrient values
    dates = list(daily_log.keys())
    values = []
    
    for date in dates:
        # Calculate total nutrient for the day
        daily_total = sum(entry.get(nutrient, 0) for entry in daily_log[date])
        values.append(daily_total)
    
    # Create DataFrame
    df = pd.DataFrame({
        'Date': dates,
        'Value': values
    })
    
    # Convert dates to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Sort by date
    df = df.sort_values('Date')
    
    # Create line chart
    fig = px.line(
        df,
        x='Date',
        y='Value',
        markers=True,
        title=f"{nutrient.capitalize()} History",
    )
    
    # Update layout
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title=f"{nutrient.capitalize()}",
        height=300,
        margin=dict(l=20, r=20, t=40, b=20),
    )
    
    return fig
