# BigQuery Public Datasets Guide
## Community Health & Wellness Advisor

### Mission Use Cases & Recommended Datasets

---

## 📊 **Use Case 1: Mobile Clinic Deployment**
**Question:** "What are the top five zip codes where we should prioritize mobile health clinic deployment based on poverty levels?"

**Datasets to Use:**
```sql
-- Area Deprivation Index (socioeconomic disadvantage by zip code)
SELECT 
    zipcode,
    area_deprivation_index_percent,
    description
FROM `bigquery-public-data.broadstreet_adi.area_deprivation_index_by_zipcode`
WHERE year = (SELECT MAX(year) FROM `bigquery-public-data.broadstreet_adi.area_deprivation_index_by_zipcode`)
ORDER BY area_deprivation_index_percent DESC
LIMIT 5;

-- Or Census ACS for poverty data
SELECT 
    geo_id,
    poverty,
    median_income,
    total_pop
FROM `bigquery-public-data.census_bureau_acs.zip_codes_2018_5yr`
ORDER BY poverty DESC
LIMIT 5;
```

---

## 🌫️ **Use Case 2: Air Quality Trends**
**Question:** "How's the air quality today compared to last week?"

**Datasets to Use:**
```sql
-- PM2.5 Daily Summary (most relevant for health)
SELECT 
    state_name,
    county_name,
    date_local,
    arithmetic_mean as pm25_level,
    parameter_name
FROM `bigquery-public-data.epa_historical_air_quality.pm25_frm_daily_summary`
WHERE state_name = 'California'
    AND county_name = 'Los Angeles'
    AND date_local >= DATE_SUB(CURRENT_DATE(), INTERVAL 14 DAY)
ORDER BY date_local DESC;

-- Ozone (O3) Levels
SELECT 
    state_name,
    county_name,
    date_local,
    arithmetic_mean as ozone_level
FROM `bigquery-public-data.epa_historical_air_quality.o3_daily_summary`
WHERE state_name = 'California'
    AND date_local >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
ORDER BY date_local DESC;
```

---

## 🏥 **Use Case 3: Healthcare Access & Uninsured Populations** ⭐
**Question:** "Show me free or low-cost dental clinics in close proximity to the highest uninsured populations"

**🎯 PROJECT DATASET - PERFECT FIT!**
```sql
-- Find free/low-cost dental clinics in high-uninsured areas
SELECT 
    county,
    state,
    clinic_name,
    clinic_address,
    clinic_phone,
    clinic_services,
    accepts_uninsured,
    free_services,
    sliding_scale,
    uninsured_rate,
    uninsured_count,
    total_population,
    distance_miles
FROM `qwiklabs-gcp-04-91797af16116.dental.dental_data`
WHERE (free_services = TRUE OR sliding_scale = TRUE)
    AND state = 'CA'
ORDER BY uninsured_rate DESC, distance_miles ASC
LIMIT 10;

-- Find clinics in specific high-need counties
SELECT 
    county,
    clinic_name,
    clinic_address,
    clinic_phone,
    clinic_services,
    free_services,
    sliding_scale,
    uninsured_rate
FROM `qwiklabs-gcp-04-91797af16116.dental.dental_data`
WHERE county IN ('Los Angeles County', 'Fresno County', 'Kern County')
    AND (free_services = TRUE OR sliding_scale = TRUE OR accepts_uninsured = TRUE)
ORDER BY uninsured_rate DESC;
```

**Also useful - Census ACS:**
```sql
-- Find areas with highest uninsured populations
SELECT 
    geo_id,
    total_pop,
    median_income,
    poverty
FROM `bigquery-public-data.census_bureau_acs.zip_codes_2018_5yr`
WHERE poverty > 15.0
ORDER BY total_pop DESC, poverty DESC
LIMIT 20;
```

---

## 🏆 **Use Case 4: State Health Rankings**
**Question:** "Compare health outcomes across states"

**Datasets to Use:**
```sql
-- America Health Rankings
SELECT 
    state,
    year,
    edition,
    measure_name,
    value,
    source
FROM `bigquery-public-data.america_health_rankings.ahr`
WHERE measure_name LIKE '%Infant Mortality%'
    OR measure_name LIKE '%Diabetes%'
    OR measure_name LIKE '%Asthma%'
ORDER BY state, year DESC, measure_name;
```

---

## 🦠 **Use Case 5: Pandemic Impact Analysis**
**Question:** "COVID-19 cases and health equity"

**Datasets to Use:**
```sql
-- COVID-19 Open Data
SELECT 
    location_key,
    date,
    new_confirmed,
    new_deceased,
    cumulative_confirmed,
    cumulative_deceased,
    population
FROM `bigquery-public-data.covid19_open_data.covid19_open_data`
WHERE country_name = 'United States'
    AND subregion1_name = 'California'
    AND date >= '2020-01-01'
ORDER BY date DESC
LIMIT 100;
```

---

## 📍 **Key Dataset Details**

### **Census Bureau ACS (American Community Survey)**
**Tables:** `census_bureau_acs.zip_codes_2018_5yr`, `census_bureau_acs.county_2018_5yr`

**Key Fields:**
- `total_pop` - Total population
- `median_income` - Median household income
- `income_per_capita` - Per capita income
- `poverty` - Poverty rate
- `pop_determined_poverty_status` - Population for whom poverty status determined
- Income brackets (income_less_10000, income_10000_14999, etc.)
- Employment by sector

**Use For:** Finding underserved areas, income disparities, poverty rates

---

### **Broadstreet Area Deprivation Index (ADI)**
**Tables:** 
- `broadstreet_adi.area_deprivation_index_by_zipcode`
- `broadstreet_adi.area_deprivation_index_by_county`

**Key Fields:**
- `zipcode` / `county_fips` - Geographic identifier
- `area_deprivation_index_percent` - Percentile rank (0-100, higher = more deprived)
- `year` - Data year

**Use For:** Identifying socioeconomically disadvantaged areas for targeted interventions

---

### **EPA Air Quality**
**Tables:** Multiple daily/hourly summaries for different pollutants

**Key Fields:**
- `state_name`, `county_name`, `city_name` - Location
- `arithmetic_mean` - Average pollutant level
- `parameter_name` - Type of pollutant
- `date_local` - Date of measurement
- `aqi` - Air Quality Index (if available)

**Common Pollutants:**
- **PM2.5** - Fine particulate matter (most health-relevant)
- **O3** - Ozone
- **NO2** - Nitrogen dioxide
- **SO2** - Sulfur dioxide
- **CO** - Carbon monoxide

**Use For:** Air quality monitoring, environmental health hazards

---

### **America Health Rankings**
**Table:** `america_health_rankings.ahr`

**Key Fields:**
- `state` - State name
- `measure_name` - Health metric (e.g., "Diabetes", "Infant Mortality")
- `value` - Metric value
- `year` - Data year
- `edition` - Annual or Health of Women report

**Use For:** State-level health comparisons, population health trends

---

## 💡 **Pro Tips for Your Agent**

1. **Always use the latest year available:**
   ```sql
   WHERE year = (SELECT MAX(year) FROM table)
   ```

2. **Join datasets for richer insights:**
   - ADI + Census ACS = Socioeconomic picture
   - Air Quality + Census = Environmental justice analysis
   - Health Rankings + Demographics = Health equity assessment

3. **Use geographic joins:**
   ```sql
   -- Join by zip code
   JOIN ON zipcode = geo_id
   
   -- Join by state
   JOIN ON state_name = state
   ```

4. **Filter for recent data:**
   ```sql
   WHERE date_local >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
   ```

5. **Aggregate for trends:**
   ```sql
   GROUP BY state_name, EXTRACT(YEAR FROM date_local)
   ORDER BY year DESC
   ```

---

---

## 🎯 **PROJECT-SPECIFIC DATASETS** (Your Secret Weapons!)

### **1. Dental Clinics Data** ⭐⭐⭐
**Table:** `qwiklabs-gcp-04-91797af16116.dental.dental_data`

**Key Fields:**
- `clinic_name`, `clinic_address`, `clinic_phone` - Contact info
- `clinic_services` - What services they offer
- `accepts_uninsured` (BOOLEAN) - Takes uninsured patients
- `free_services` (BOOLEAN) - Offers free care
- `sliding_scale` (BOOLEAN) - Sliding scale pricing
- `county`, `state` - Location
- `uninsured_rate` (FLOAT) - % uninsured in area
- `uninsured_count` (INTEGER) - # of uninsured
- `total_population` (INTEGER) - Population
- `distance_miles` (FLOAT) - Distance metric

**Perfect For:**
- ✅ "Show me free dental clinics near uninsured populations"
- ✅ "Find sliding scale clinics in Los Angeles"
- ✅ Finding healthcare access solutions

---

### **2. California Hospital Ratings**
**Table:** `qwiklabs-gcp-04-91797af16116.cal_hosp_ratings.cal-hosp-ratings-2011-2018_copy`

**Key Fields:**
- `Hospital`, `County`, `OSHPD_ID` - Hospital identification
- `Performance_Measure` - What's being measured
- `Performance_Rating` - Rating (Excellent, Good, Fair, Poor)
- `Latitude`, `Longitude` - Location coordinates
- `Year` - Data year
- `Number_of_Cases`, `Number_of_Adverse_Events` - Outcomes
- `Risk_adjusted_Rate` - Adjusted performance

**Perfect For:**
- Finding hospitals by location
- Hospital quality comparisons
- Healthcare facility planning

---

### **3. Chronic Disease Indicators**
**Table:** `qwiklabs-gcp-04-91797af16116.chronic_disease_indicators.chronic_disease_indicators_table`

**Key Fields:**
- `LocationAbbr`, `LocationDesc` - State/location
- `Topic` - Health topic (Diabetes, Cardiovascular, etc.)
- `Question` - Specific indicator
- `DataValue` - Prevalence/rate
- `YearStart`, `YearEnd` - Time period
- `LowConfidenceLimit`, (continues with confidence intervals)

**Perfect For:**
- Disease prevalence by state
- Health outcome trends
- Identifying high-burden areas

**Example Query:**
```sql
SELECT 
    LocationDesc,
    Topic,
    Question,
    DataValue,
    YearStart
FROM `qwiklabs-gcp-04-91797af16116.chronic_disease_indicators.chronic_disease_indicators_table`
WHERE Topic = 'Diabetes'
    AND LocationDesc = 'California'
ORDER BY YearStart DESC, DataValue DESC
LIMIT 10;
```

---

### **4. Global Air Quality Data**
**Table:** `qwiklabs-gcp-04-91797af16116.global_aq.global_aq_data`

**Key Fields:**
- `city`, `country`, `location` - Geographic identifiers
- `pollutant` - Type (PM2.5, PM10, O3, NO2, etc.)
- `value` - Measurement value
- `unit` - Measurement unit
- `timestamp` - When measured
- `latitude`, `longitude` - Coordinates
- `location_geom` (GEOGRAPHY) - Geographic data type
- `source_name` - Data source

**Perfect For:**
- Real-time air quality by city
- Geographic air quality analysis
- Tracking pollution trends

**Example Query:**
```sql
SELECT 
    city,
    pollutant,
    AVG(value) as avg_value,
    unit,
    DATE(timestamp) as date
FROM `qwiklabs-gcp-04-91797af16116.global_aq.global_aq_data`
WHERE city LIKE '%Los Angeles%'
    AND pollutant = 'pm25'
    AND timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
GROUP BY city, pollutant, unit, date
ORDER BY date DESC;
```

---

## 🚀 **Next Steps**

To test these queries:
1. Restart ADK web: `adk web`
2. Select `data_agent`
3. Ask natural language questions like:
   - **"Show me free dental clinics in California counties with high uninsured rates"** ⭐
   - **"Find sliding scale dental clinics in Los Angeles"** ⭐
   - **"What are the chronic disease rates in California?"** ⭐
   - "What zip codes in California have the highest area deprivation index?"
   - "Show me PM2.5 air quality trends for Los Angeles in the last month"
   - "Which California hospitals have the best performance ratings?"

Your agent will automatically translate these to SQL using the datasets above!

