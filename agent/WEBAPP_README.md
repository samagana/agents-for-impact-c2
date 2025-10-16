# 🏥 Health Intelligence Hub - Web Application

## Overview

The Health Intelligence Hub is a comprehensive web application that provides **conversational hyper-local health intelligence** to empower public health staff, community organizations, and residents to mitigate risks and justify resource allocation decisions.

## 🎯 Key Features

### **Multi-Role Interface**
- **Public Health Staff**: Data analysis, resource planning, intervention strategies
- **Community Organizations**: Community needs assessment, partnership opportunities
- **Residents**: Health resources, preventive care, community programs

### **Conversational AI**
- Integrated with Google ADK Health Agents
- Context-aware responses based on user role and location
- Natural language queries for health data and insights

### **Interactive Dashboards**
- Real-time health metrics and KPIs
- Risk assessment heatmaps
- Resource allocation visualizations
- Geographic health mapping

### **Data Intelligence**
- Chronic disease indicators
- Resource capacity analysis
- Risk factor assessment
- Trend analysis and forecasting

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Google Cloud Project with BigQuery access
- Google API Key for Gemini models

### Installation

1. **Install Dependencies**
```bash
cd agent
uv sync
```

2. **Set Environment Variables**
Create a `.env` file with:
```env
GOOGLE_API_KEY=your-google-api-key
GOOGLE_CLOUD_PROJECT=your-gcp-project-id
GOOGLE_CLOUD_LOCATION=us-central1
```

3. **Run the Application**
```bash
# Option 1: Run both services together
python run_webapp.py

# Option 2: Run services separately
# Terminal 1: Start ADK server
uv run adk web --host 0.0.0.0 --port 8080

# Terminal 2: Start Streamlit app
streamlit run app.py --server.port 8501
```

4. **Access the Application**
- **Web Interface**: http://localhost:8501
- **ADK API**: http://localhost:8080

## 🏗️ Architecture

### **Frontend (Streamlit)**
- **Dashboard**: Health metrics, insights, and quick actions
- **Chat Interface**: Conversational AI for health queries
- **Data Visualization**: Interactive charts and maps
- **Resource Planning**: Allocation tools and recommendations

### **Backend (ADK Agents)**
- **Health Agent**: Main conversational interface
- **Data Agent**: Health data analysis and insights
- **Insights Agent**: Risk assessment and recommendations

### **Data Sources**
- BigQuery health datasets
- Chronic disease indicators
- Resource capacity data
- Geographic health metrics

## 📊 User Interface Components

### **1. Dashboard Tab**
- **Health Score**: Overall community health rating
- **Risk Level**: Current risk assessment
- **Resource Capacity**: Available health services
- **Community Engagement**: Participation metrics

### **2. Health Assistant Tab**
- **Chat Interface**: Natural language health queries
- **Role-based Responses**: Tailored to user type
- **Context Awareness**: Location and role-specific insights

### **3. Data Insights Tab**
- **Risk Heatmap**: Visual risk assessment by location
- **Resource Allocation**: Capacity vs demand analysis
- **Interactive Data Tables**: Detailed health metrics

### **4. Geographic View Tab**
- **Interactive Map**: Health indicators by location
- **Risk Visualization**: Color-coded risk levels
- **Population Data**: Demographics and health metrics

### **5. Resource Planning Tab**
- **Gap Analysis**: Resource needs assessment
- **Recommendations**: AI-generated action plans
- **Budget Planning**: Cost-benefit analysis
- **Implementation Timeline**: Project planning tools

## 🎨 UI/UX Features

### **Healthcare-Focused Design**
- Medical color scheme (blues, whites, clean layouts)
- Accessibility-compliant interface
- Mobile-responsive design
- Intuitive navigation

### **Role-Based Customization**
- **Public Health Staff**: Data-heavy dashboards, analysis tools
- **Community Organizations**: Partnership opportunities, community needs
- **Residents**: Simple interface, resource finder, health tips

### **Interactive Elements**
- Real-time chat with health AI
- Interactive maps and charts
- Drag-and-drop resource planning
- Export capabilities for reports

## 🔧 Configuration

### **Environment Variables**
```env
# Required
GOOGLE_API_KEY=your-api-key
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1

# Optional
ADK_API_URL=http://localhost:8080
STREAMLIT_SERVER_PORT=8501
```

### **Customization**
- **Locations**: Modify location list in `app.py`
- **User Roles**: Add new roles in session state
- **Data Sources**: Update data loading functions
- **Styling**: Modify CSS in the main app

## 📈 Data Integration

### **BigQuery Integration**
- Chronic disease indicators
- Population health metrics
- Resource capacity data
- Geographic health data

### **Real-time Updates**
- Live data refresh capabilities
- Automated insight generation
- Trend analysis and alerts
- Performance monitoring

## 🚀 Deployment

### **Docker Deployment**
```bash
# Build and run with Docker
docker build -t health-intelligence-hub .
docker run -p 8501:8501 -p 8080:8080 --env-file .env health-intelligence-hub
```

### **Cloud Run Deployment**
```bash
# Deploy to Google Cloud Run
gcloud run deploy health-intelligence-hub \
    --image gcr.io/your-project/health-intelligence-hub \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --memory=2048Mi \
    --cpu=2
```

## 🔒 Security & Privacy

### **Data Protection**
- No personal health information stored
- Aggregate data only
- HIPAA-compliant data handling
- Secure API communications

### **Access Control**
- Role-based permissions
- Location-based data filtering
- Audit logging capabilities
- Secure authentication (optional)

## 📱 Mobile Support

- **Responsive Design**: Works on all device sizes
- **Touch-Friendly**: Optimized for mobile interaction
- **Offline Capabilities**: Basic functionality without internet
- **Progressive Web App**: Installable on mobile devices

## 🎯 Use Cases

### **Public Health Departments**
- Monitor community health trends
- Identify intervention opportunities
- Justify budget allocations
- Track program effectiveness

### **Community Organizations**
- Assess community needs
- Find partnership opportunities
- Access health resources
- Plan community programs

### **Healthcare Providers**
- Understand community health context
- Identify service gaps
- Plan resource allocation
- Improve patient outcomes

### **Residents**
- Find local health resources
- Understand community health
- Access preventive care
- Connect with health programs

## 🔮 Future Enhancements

- **Predictive Analytics**: AI-powered health forecasting
- **Mobile App**: Native iOS/Android applications
- **Integration APIs**: Connect with health systems
- **Advanced Visualization**: 3D health mapping
- **Multi-language Support**: International deployment
- **Blockchain Integration**: Secure health data sharing

## 📞 Support

For technical support or feature requests:
- **Documentation**: Check this README and code comments
- **Issues**: Report bugs via GitHub issues
- **Community**: Join our health tech community forum

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Built with ❤️ for Public Health Empowerment**
