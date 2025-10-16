import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
import requests
import json
import os
from datetime import datetime, timedelta
import numpy as np
from streamlit_chat import message
from streamlit_option_menu import option_menu
from st_aggrid import AgGrid, GridOptionsBuilder
import dotenv
import asyncio
from health_agent_integration import health_integration

# Load environment variables
dotenv.load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Health Intelligence Hub",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for healthcare theme
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 4px solid #2a5298;
    }
    
    .risk-high {
        background: linear-gradient(90deg, #ff6b6b, #ee5a52);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    
    .risk-medium {
        background: linear-gradient(90deg, #feca57, #ff9ff3);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    
    .risk-low {
        background: linear-gradient(90deg, #48dbfb, #0abde3);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    
    .chat-container {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #e9ecef;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-left: 20px;
        padding-right: 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #2a5298;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'user_role' not in st.session_state:
    st.session_state.user_role = 'Public Health Staff'
if 'selected_location' not in st.session_state:
    st.session_state.selected_location = 'San Francisco, CA'

# Sample data for demonstration
@st.cache_data
def load_sample_data():
    """Load sample health data for demonstration"""
    # Sample chronic disease indicators
    chronic_disease_data = pd.DataFrame({
        'Location': ['San Francisco', 'Oakland', 'San Jose', 'Fresno', 'Sacramento'],
        'Diabetes_Rate': [8.2, 12.1, 9.8, 15.3, 11.7],
        'Heart_Disease_Rate': [5.8, 8.9, 6.2, 12.1, 9.4],
        'Obesity_Rate': [18.5, 28.3, 22.1, 35.2, 26.8],
        'Population': [873965, 433031, 1035317, 542107, 513624],
        'Median_Income': [126187, 78778, 125075, 54995, 71000],
        'Uninsured_Rate': [4.2, 8.1, 5.9, 12.3, 7.8]
    })
    
    # Sample resource allocation data
    resource_data = pd.DataFrame({
        'Resource_Type': ['Primary Care Clinics', 'Emergency Services', 'Mental Health', 'Preventive Care', 'Community Health Workers'],
        'Current_Capacity': [85, 92, 67, 78, 45],
        'Demand': [95, 88, 89, 82, 78],
        'Gap': [10, -4, 22, 4, 33],
        'Priority': ['High', 'Low', 'High', 'Medium', 'High']
    })
    
    # Sample risk indicators
    risk_data = pd.DataFrame({
        'Risk_Factor': ['Air Quality', 'Food Access', 'Housing Stability', 'Transportation', 'Social Isolation'],
        'Current_Level': [3.2, 4.1, 2.8, 3.9, 3.5],
        'Trend': ['Improving', 'Stable', 'Worsening', 'Stable', 'Worsening'],
        'Impact_Score': [7.5, 6.2, 8.9, 5.1, 7.8]
    })
    
    return chronic_disease_data, resource_data, risk_data

async def get_health_insights(location, user_role):
    """Generate health insights using ADK agents"""
    try:
        insights = await health_integration.get_health_insights(location, user_role)
        return insights
    except Exception as e:
        st.error(f"Error getting insights: {e}")
        # Fallback to static insights
        fallback_insights = {
            'Public Health Staff': [
                f"High diabetes prevalence in {location} (15.3%) requires targeted intervention programs",
                "Mental health services are at 67% capacity with 22% demand gap",
                "Community health worker shortage (45% capacity) affects preventive care outreach",
                "Air quality improvements show positive trend but housing stability declining"
            ],
            'Community Organizations': [
                f"Food access programs needed in {location} - current score 4.1/10",
                "Social isolation increasing - community engagement programs recommended",
                "Transportation barriers affecting healthcare access for 39% of residents",
                "Housing instability rising - emergency assistance programs needed"
            ],
            'Residents': [
                f"Your area has good primary care access (85% capacity)",
                "Preventive care services available - schedule annual checkups",
                "Mental health resources available but may have wait times",
                "Community health programs can help with chronic disease management"
            ]
        }
        return fallback_insights.get(user_role, fallback_insights['Public Health Staff'])

def create_risk_heatmap():
    """Create a risk assessment heatmap"""
    risk_factors = ['Diabetes', 'Heart Disease', 'Obesity', 'Mental Health', 'Air Quality', 'Food Access']
    locations = ['San Francisco', 'Oakland', 'San Jose', 'Fresno', 'Sacramento']
    
    # Generate sample risk scores
    risk_scores = np.random.uniform(1, 10, (len(locations), len(risk_factors)))
    
    fig = px.imshow(
        risk_scores,
        x=risk_factors,
        y=locations,
        color_continuous_scale='RdYlBu_r',
        title="Health Risk Assessment by Location",
        labels=dict(x="Risk Factors", y="Locations", color="Risk Score")
    )
    
    fig.update_layout(
        height=400,
        title_font_size=16,
        font=dict(size=12)
    )
    
    return fig

def create_resource_allocation_chart():
    """Create resource allocation visualization"""
    _, resource_data, _ = load_sample_data()

    fig = go.Figure()

    fig.add_trace(go.Bar(
        name='Current Capacity',
        x=resource_data['Resource_Type'],
        y=resource_data['Current_Capacity'],
        marker_color='lightblue'
    ))

    fig.add_trace(go.Bar(
        name='Demand',
        x=resource_data['Resource_Type'],
        y=resource_data['Demand'],
        marker_color='orange'
    ))

    fig.update_layout(
        title='Resource Capacity vs Demand',
        xaxis_title='Resource Type',
        yaxis_title='Percentage',
        barmode='group',
        height=400
    )

    return fig

def create_geographic_map():
    """Create interactive map showing health indicators"""
    chronic_data, _, _ = load_sample_data()
    
    # Sample coordinates for California cities
    coordinates = {
        'San Francisco': [37.7749, -122.4194],
        'Oakland': [37.8044, -122.2712],
        'San Jose': [37.3382, -121.8863],
        'Fresno': [36.7378, -119.7871],
        'Sacramento': [38.5816, -121.4944]
    }
    
    m = folium.Map(location=[37.7749, -122.4194], zoom_start=7)
    
    for _, row in chronic_data.iterrows():
        location = row['Location']
        if location in coordinates:
            lat, lon = coordinates[location]
            
            # Color based on diabetes rate
            color = 'red' if row['Diabetes_Rate'] > 12 else 'orange' if row['Diabetes_Rate'] > 9 else 'green'
            
            folium.CircleMarker(
                [lat, lon],
                radius=row['Diabetes_Rate'] * 2,
                popup=f"""
                <b>{location}</b><br>
                Diabetes Rate: {row['Diabetes_Rate']}%<br>
                Heart Disease: {row['Heart_Disease_Rate']}%<br>
                Obesity Rate: {row['Obesity_Rate']}%<br>
                Population: {row['Population']:,}
                """,
                color=color,
                fill=True,
                fillOpacity=0.6
            ).add_to(m)
    
    return m

async def chat_with_health_agent(user_input, user_role, location):
    """Chat with ADK health agent"""
    try:
        response = await health_integration.chat_with_health_agent(user_input, user_role, location)
        return response
    except Exception as e:
        st.error(f"Error in chat: {e}")
        # Fallback responses
        fallback_responses = {
            'Public Health Staff': [
                "Based on current data, I recommend focusing on diabetes prevention programs in high-risk areas.",
                "Resource allocation should prioritize mental health services and community health workers.",
                "Consider implementing mobile health units for underserved communities."
            ],
            'Community Organizations': [
                "Your organization could partner with local clinics for health screening events.",
                "Consider developing food access programs in areas with limited grocery stores.",
                "Transportation assistance programs could improve healthcare access for residents."
            ],
            'Residents': [
                "I can help you find local health resources and preventive care options.",
                "Based on your area, I recommend scheduling regular health screenings.",
                "There are community programs available to help with chronic disease management."
            ]
        }
        import random
        return random.choice(fallback_responses.get(user_role, fallback_responses['Public Health Staff']))

# Main app
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🏥 Health Intelligence Hub</h1>
        <p>Conversational Hyper-Local Health Intelligence for Public Health Empowerment</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/200x100/2a5298/ffffff?text=Health+Hub", width=200)
        
        # User role selection
        st.session_state.user_role = st.selectbox(
            "Select Your Role",
            ["Public Health Staff", "Community Organizations", "Residents"],
            index=0
        )
        
        # Location selection
        st.session_state.selected_location = st.selectbox(
            "Select Location",
            ["San Francisco, CA", "Oakland, CA", "San Jose, CA", "Fresno, CA", "Sacramento, CA"],
            index=0
        )
        
        st.markdown("---")
        
        # Quick stats
        st.markdown("### 📊 Quick Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Health Score", "7.2", "0.3")
        with col2:
            st.metric("Risk Level", "Medium", "-0.1")
        
        st.markdown("### 🎯 Priority Actions")
        st.markdown("""
        - **High**: Mental Health Services
        - **Medium**: Community Health Workers
        - **Low**: Emergency Services
        """)
    
    # Main content tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏠 Dashboard", 
        "💬 Health Assistant", 
        "📊 Data Insights", 
        "🗺️ Geographic View", 
        "📋 Resource Planning"
    ])
    
    with tab1:
        st.markdown(f"### Welcome, {st.session_state.user_role}")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h3>Health Score</h3>
                <h2 style="color: #2a5298;">7.2/10</h2>
                <p>↑ 0.3 from last month</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h3>Risk Level</h3>
                <h2 style="color: #feca57;">Medium</h2>
                <p>↓ 0.1 from last month</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <h3>Resources</h3>
                <h2 style="color: #48dbfb;">78%</h2>
                <p>Average capacity</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="metric-card">
                <h3>Community</h3>
                <h2 style="color: #ff6b6b;">High</h2>
                <p>Engagement level</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Health insights
        st.markdown("### 🎯 Key Insights for Your Role")
        insights = asyncio.run(get_health_insights(st.session_state.selected_location, st.session_state.user_role))
        
        for insight in insights:
            st.info(f"💡 {insight}")
        
        # Risk indicators
        st.markdown("### ⚠️ Risk Indicators")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="risk-high">
                <strong>High Risk</strong><br>
                Mental Health Services: 22% capacity gap
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="risk-medium">
                <strong>Medium Risk</strong><br>
                Housing Stability: Declining trend
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="risk-medium">
                <strong>Medium Risk</strong><br>
                Community Health Workers: 33% shortage
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="risk-low">
                <strong>Low Risk</strong><br>
                Air Quality: Improving trend
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### 💬 Chat with Health Intelligence Assistant")
        st.markdown("Ask questions about health data, resources, or get recommendations for your community.")
        
        # Chat interface
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask about health data, resources, or recommendations..."):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate response
            response = asyncio.run(chat_with_health_agent(prompt, st.session_state.user_role, st.session_state.selected_location))
            
            # Add assistant response
            st.session_state.messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.markdown(response)
    
    with tab3:
        st.markdown("### 📊 Data Insights & Analytics")
        
        # Risk heatmap
        st.plotly_chart(create_risk_heatmap(), use_container_width=True)
        
        # Resource allocation
        st.plotly_chart(create_resource_allocation_chart(), use_container_width=True)
        
        # Data table
        chronic_data, resource_data, risk_data = load_sample_data()
        
        st.markdown("### 📋 Detailed Data View")
        selected_data = st.selectbox("Select Dataset", ["Chronic Disease Indicators", "Resource Allocation", "Risk Factors"])
        
        if selected_data == "Chronic Disease Indicators":
            AgGrid(chronic_data, height=300, fit_columns_on_grid_load=True)
        elif selected_data == "Resource Allocation":
            AgGrid(resource_data, height=300, fit_columns_on_grid_load=True)
        else:
            AgGrid(risk_data, height=300, fit_columns_on_grid_load=True)
    
    with tab4:
        st.markdown("### 🗺️ Geographic Health View")
        st.markdown("Interactive map showing health indicators across locations")
        
        # Create and display map
        health_map = create_geographic_map()
        st_folium(health_map, width=700, height=500)
        
        # Map legend
        st.markdown("""
        **Map Legend:**
        - 🔴 Red: High risk (Diabetes rate > 12%)
        - 🟠 Orange: Medium risk (Diabetes rate 9-12%)
        - 🟢 Green: Low risk (Diabetes rate < 9%)
        - Circle size represents diabetes prevalence
        """)
    
    with tab5:
        st.markdown("### 📋 Resource Planning & Allocation")
        
        chronic_data, resource_data, risk_data = load_sample_data()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🎯 Resource Gap Analysis")
            AgGrid(resource_data, height=400, fit_columns_on_grid_load=True)
        
        with col2:
            st.markdown("#### 📈 Resource Recommendations")
            
            # Generate recommendations based on data
            recommendations = [
                "**Priority 1**: Increase mental health services capacity by 25%",
                "**Priority 2**: Recruit 15 additional community health workers",
                "**Priority 3**: Expand preventive care programs in underserved areas",
                "**Priority 4**: Implement mobile health units for remote areas"
            ]
            
            for rec in recommendations:
                st.markdown(f"✅ {rec}")
            
            st.markdown("#### 💰 Budget Impact")
            st.metric("Estimated Cost", "$2.3M", "15% increase")
            st.metric("Expected ROI", "3.2x", "Health outcomes improvement")
        
        # Action planning
        st.markdown("#### 📝 Action Planning Tool")
        
        with st.form("action_plan"):
            st.selectbox("Select Priority Area", ["Mental Health", "Community Health Workers", "Preventive Care", "Emergency Services"])
            st.text_area("Action Description", placeholder="Describe the action to be taken...")
            st.date_input("Target Date")
            st.number_input("Budget Required ($)", min_value=0, step=1000)
            
            if st.form_submit_button("Add to Action Plan"):
                st.success("Action added to plan!")

if __name__ == "__main__":
    main()
