<template>
  <div class="py-8 px-4">
    <div class="max-w-6xl mx-auto bg-white rounded-2xl p-6 border border-fuchsia-300">
      
      <h2 class="text-3xl font-extrabold text-gray-800 mb-2">
        花見 <i class="font-normal"> hanami </i> - Japan Cherry Blossom Bloom Map
      </h2>
      <p class="text-sm text-gray-500 mb-8">
        Shows the number of days passed from January 1st until the first bloom.
      </p>

      <div class="flex justify-end mb-4">
          <button
              @click="activeView = activeView === 'map' ? 'scatter' : 'map'"
              class="px-4 py-2 text-sm font-semibold rounded-lg transition duration-200"
              :class="activeView === 'map' ? 'bg-fuchsia-100 text-fuchsia-700 hover:bg-fuchsia-200' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'"
          >
              Switch to {{ activeView === 'map' ? 'Scatter Plot' : 'Map View' }}
          </button>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
        
        <div class="lg:col-span-3 min-h-[600px] border border-fuchsia-300 bg-white rounded-xl overflow-hidden relative">
          
          <div v-if="isLoading" class="absolute inset-0 bg-white/70 flex items-center justify-center z-10">
            <p class="text-xl font-medium text-gray-600">Loading map data...</p>
          </div>
          
          <v-chart 
              v-if="activeView === 'map' && !isLoading"
              class="chart" 
              :option="chartOption" 
              autoresize 
              style="height: 600px; width: 100%;"
              ref="chartRef"          
              @mousemove="handleChartHover" />
          
          <v-chart 
              v-else-if="activeView === 'scatter' && !isLoading"
              class="chart" 
              :option="scatterChartOption" 
              autoresize 
              style="height: 600px; width: 100%;"
              ref="chartRef"          
              @mousemove="handleChartHover" />

        </div>

        <div class="lg:col-span-1 bg-white border border-fuchsia-300 rounded-xl p-4 space-y-4">
          
          <div v-if="selectedCityStats" class="space-y-4">
            
            <div 
              :class="[
                'p-3 rounded-lg border-l-4 border',
                selectedCityStats.isCity ? 'bg-white border-fuchsia-300' : 'bg-fuchsia-50 border-gray-500'
              ]"
            >
              <p class="text-sm font-semibold" :class="selectedCityStats.isCity ? 'text-fuchsia-300' : 'text-gray-700'">
                {{ selectedCityStats.isCity ? 'Selected City' : 'Selected Prefecture' }}
              </p>
              <span class="text-2xl font-extrabold text-gray-900">{{ selectedCityStats.name }}</span>
            </div>
            
            <template v-if="selectedCityStats.isCity">
                <div class="bg-gray-50 p-3 rounded border border-gray-300">
                    <p class="text-sm font-semibold text-gray-700">Year</p>
                    <span class="text-xl font-extrabold text-gray-900">{{ selectedCityStats.year }}</span>
                </div>
                
                <div class="bg-gray-50 p-3 rounded border border-gray-300">
                    <p class="text-sm font-semibold text-gray-700">Bloom Date</p>
                    <span class="text-xl font-extrabold text-gray-900">{{ selectedCityStats.date }}</span>
                </div>
                
                <div class="bg-gray-50 p-3 rounded border border-gray-300">
                    <p class="text-sm font-semibold text-gray-700">Day of Year</p>
                    <span class="text-xl font-extrabold text-gray-900">{{ selectedCityStats.day }}</span>
                </div>
            </template>
            
          </div>
          
          <div v-else>
            <p class="text-sm text-gray-500 py-4">
              Hover over a city or a prefecture to view its information here.
            </p>
          </div>
          
          <hr class="border-fuchsia-100" />
          
          <div class="space-y-4">
              
              <div v-if="activeView === 'map'" class="space-y-4">
                  <h3 class="text-lg font-bold text-gray-800">Map Controls</h3>
                  <div class="flex items-center gap-3 p-1 rounded-lg bg-white border border-gray-200">
                      <label for="pointSizeSlider" class="text-sm font-semibold text-gray-700 shrink-0 w-24">
                          City Size:
                      </label>
                      <input 
                          type="range" 
                          id="pointSizeSlider" 
                          min="4" 
                          max="40" 
                          step="1" 
                          v-model.number="cityPointSize"
                          class="w-full h-2 bg-gray-400 rounded-lg appearance-none cursor-pointer"
                      >
                      <span class="text-sm font-bold text-gray-800 w-8 text-right shrink-0">
                          {{ cityPointSize }}
                      </span>
                  </div>
                  <div class="flex items-center gap-3 p-1 rounded-lg bg-white border border-gray-200">
                      <label for="zoomSlider" class="text-sm font-semibold text-gray-700 shrink-0 w-24">
                          Zoom:
                      </label>
                      <input 
                          type="range" 
                          id="zoomSlider" 
                          min="1" 
                          max="4" 
                          step="0.1" 
                          v-model.number="mapZoomLevel"
                          class="w-full h-2 bg-gray-400 rounded-lg appearance-none cursor-pointer"
                      >
                      <span class="text-sm font-bold text-gray-800 w-8 text-right shrink-0">
                          {{ mapZoomLevel.toFixed(1) }}
                      </span>
                  </div>
              </div>

              <div v-else-if="activeView === 'scatter'" class="space-y-4">
                  <h3 class="text-lg font-bold text-gray-800">Scatter Controls</h3>
                  
                  <div class="space-y-1">
                      <label for="xAxisSelect" class="text-sm font-semibold text-gray-700">
                          X-Axis:
                      </label>
                      <select id="xAxisSelect" v-model="xAxisKey" 
                          class="w-full h-10 bg-gray-50 border border-gray-300 rounded-lg p-2 text-gray-800 text-sm focus:ring-fuchsia-500 focus:border-fuchsia-500">
                          <option v-for="option in axisOptions" :key="option.value" :value="option.value">
                              {{ option.label }}
                          </option>
                      </select>
                  </div>
                  
                  <div class="space-y-1">
                      <label for="yAxisSelect" class="text-sm font-semibold text-gray-700">
                          Y-Axis:
                      </label>
                      <select id="yAxisSelect" v-model="yAxisKey"
                          class="w-full h-10 bg-gray-50 border border-gray-300 rounded-lg p-2 text-gray-800 text-sm focus:ring-fuchsia-500 focus:border-fuchsia-500">
                          <option v-for="option in axisOptions" :key="option.value" :value="option.value">
                              {{ option.label }}
                          </option>
                      </select>
                  </div>

                  <div class="flex items-center gap-3 p-1 rounded-lg bg-white border border-gray-200">
                      <label for="pointSizeSlider" class="text-sm font-semibold text-gray-700 shrink-0 w-24">
                          Point Size:
                      </label>
                      <input 
                          type="range" 
                          id="pointSizeSlider" 
                          min="4" 
                          max="40" 
                          step="1" 
                          v-model.number="cityPointSize"
                          class="w-full h-2 bg-gray-400 rounded-lg appearance-none cursor-pointer"
                      >
                      <span class="text-sm font-bold text-gray-800 w-8 text-right shrink-0">
                          {{ cityPointSize }}
                      </span>
                  </div>
              </div>
          </div>
          
        </div>
      </div> 
      
      <div class="mt-8 space-y-6">
        <div class="flex items-center gap-4 p-4 rounded-lg bg-white border border-fuchsia-300">
          <label for="yearSlider" class="text-lg font-bold shrink-0 w-24">
            Year:
          </label>
          <input 
            type="range" 
            id="yearSlider" 
            :min="minYear" 
            :max="maxYear" 
            step="1" 
            v-model.number="selectedYear"
            class="w-full h-2 bg-gray-400 rounded-lg appearance-none cursor-pointer"
          >
          <span class="text-2xl font-bold w-12 text-right flex-shrink-0">
            {{ selectedYear }}
          </span>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed, onMounted } from 'vue';
import VChart from 'vue-echarts';
import * as echarts from 'echarts';
import * as Papa from 'papaparse';

import japanGeoJson from '@/assets/japan.geo.json'; 

// --- Component State ---
const selectedYear = ref(2025);
const fullData = ref([]);
const minYear = ref(1981);
const maxYear = ref(2025);
const isLoading = ref(true);

// --- UI State ---
const cityPointSize = ref(12);
const mapZoomLevel = ref(1.5);
const selectedCityStats = ref(null);
const chartRef = ref(null);
const activeView = ref('map'); // State for view switching ('map' or 'scatter')
const xAxisKey = ref('day'); // Scatter plot X-axis choice
const yAxisKey = ref('lat'); // Scatter plot Y-axis choice

// --- Axis Options for the dropdowns ---
const axisOptions = [
    { value: 'day', label: 'Day of Year (Bloom Day)' },
    { value: 'lat', label: 'Latitude' },
    { value: 'lon', label: 'Longitude' },
    { value: 'elevation', label: 'Elevation (m)' }
];

// --- DATA PROCESSING FOR NAME BINDING ---
const processedJapanGeoJson = JSON.parse(JSON.stringify(japanGeoJson));

processedJapanGeoJson.features.forEach(feature => {
    if (feature.properties && feature.properties.nam_ja) {
        feature.name = feature.properties.nam_ja; 
    }
});
// --- END DATA PROCESSING ---


// Convert day-of-year into a real date
const dayOfYearToDate = (dayOfYear, year) => {
    const date = new Date(year, 0, 1);
    date.setDate(date.getDate() + dayOfYear - 1);
    return date.toLocaleDateString('en-US', { month: 'long', day: 'numeric' });
};

// --- CSV Loader ---
const loadCsvData = async () => {
    isLoading.value = true;

    const response = await fetch('/all_cities_cat.csv');
    if (!response.ok) {
        console.error("CSV fetch failed.");
        isLoading.value = false;
        return;
    }

    const csvText = await response.text();

    Papa.parse(csvText, {
        header: true,
        dynamicTyping: true,
        complete: results => {
            fullData.value = results.data.filter(row =>
                row.seasonal_year &&
                row.latitude &&
                row.longitude &&
                row.bloom_day_of_year &&
                row.elevation 
            );

            const years = [...new Set(fullData.value.map(d => d.seasonal_year))].filter(y => typeof y === 'number');
            minYear.value = Math.min(...years);
            maxYear.value = Math.max(...years);
            selectedYear.value = maxYear.value;

            isLoading.value = false;
        }
    });
};

// --- Filter data per year ---
const scatterData = computed(() => {
    if (isLoading.value) return [];

    return fullData.value
        .filter(d => d.seasonal_year === selectedYear.value)
        .map(d => ({
            name: d.city_name,
            // UPDATED DATA ARRAY STRUCTURE: 
            // [0:longitude, 1:latitude, 2:bloom_day_of_year (Color Value), 3:elevation]
            value: [d.longitude, d.latitude, d.bloom_day_of_year, d.elevation],
            city_name: d.city_name
        }));
});

// --- HOVER HANDLER (Prioritizes City Data for both views) ---
const handleChartHover = params => {
    // 1. Check if the event came from the new scatter plot
    if (activeView.value === 'scatter' && params.seriesType === 'scatter' && params.name) {
        
        const cityData = scatterData.value.find(d => d.name === params.name);
        if (!cityData) return;

        // Day is still index 2: [lon, lat, DAY, elevation]
        const day = cityData.value[2]; 
        const bloomDate = dayOfYearToDate(day, selectedYear.value);

        selectedCityStats.value = {
            name: params.name,
            year: selectedYear.value,
            date: bloomDate,
            day: day,
            isCity: true
        };
        return; 
    }
    
    // 2. Check if the event came from the MAP VIEW (original logic)
    if (activeView.value === 'map') {
        
        // 2a. Map View: City Point (Scatter Series) - HIGH PRIORITY
        if (params.seriesType === 'scatter' && params.value?.length >= 3) {
            const year = selectedYear.value;
            // Data format is: [lon, lat, DAY, elevation]
            const [lon, lat, day] = params.value; 
            const bloomDate = dayOfYearToDate(day, year);

            selectedCityStats.value = {
                name: params.name,
                year: year,
                date: bloomDate,
                day: day,
                isCity: true
            };
            return; 
        }

        // 2b. Map View: Prefecture Area (geo region) - SECONDARY PRIORITY
        if (params.componentType === 'geo' && params.name) {
            selectedCityStats.value = {
                name: params.name,
                isCity: false
            };
            return;
        }
    }

    // Nothing hovered
    selectedCityStats.value = null;
};

// --- Register Map ---
onMounted(() => {
    echarts.registerMap("japan", processedJapanGeoJson);
    loadCsvData();
});

// --- CHART OPTION: MAP VIEW ---
const chartOption = computed(() => ({
    backgroundColor: '#F7F7F7', 

    title: {
        text: `Cherry Blossom Bloom Day in ${selectedYear.value}`,
        subtext: 'Days since January 1 (Lighter = Earlier Bloom)',
        left: 'center'
    },

    visualMap: {
        min: 30,
        max: 150,
        calculable: true,
        // The visual map colors based on the data item's 3rd index (which is now bloom_day_of_year)
        inRange: { color: ['#00BFFF', '#FFFF00', '#FF4500'] },
        text: ['Late Bloom', 'Early Bloom'],
        orient: 'horizontal',
        left: 'center',
        bottom: 20
    },

    geo: {
        map: "japan",
        roam: true,
        aspectScale: 1,
        zoom: mapZoomLevel.value,
        center: [137.5, 34.0], 
        
        itemStyle: {
            areaColor: '#fff', 
            borderColor: '#444',
            borderWidth: 1.2,
        },

        label: { show: false, color: '#111', fontSize: 9 },

        emphasis: {
            itemStyle: { areaColor: '#FFD7EB' }, 
            label: { show: true, fontSize: 12 }
        }
    },

    tooltip: {
        trigger: 'item',
        padding: [12, 18], 
        textStyle: { fontSize: 14, lineHeight: 20 }, 
        extraCssText: 'box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2); border-radius: 8px;', 
        
        formatter: params => {
            const year = selectedYear.value;
            
            if (params.seriesType === 'scatter' && params.value?.length >= 3) {
                // Data format is: [lon, lat, DAY, elevation]
                const [lon, lat, day] = params.value; 
                const bloomDate = dayOfYearToDate(day, year);
                
                return `<strong>${params.name}</strong><br>
                        Date: <strong>${bloomDate}</strong><br>
                        Day of Year: ${day}`;
            }

            return "No Data";
        }
    },

    series: [
        {
            type: "scatter",
            coordinateSystem: "geo",
            symbolSize: cityPointSize.value,
            emphasis: { label: { show: true, formatter: '{b}', position: 'right' } },
            data: scatterData.value
        }
    ]
}));


// --- CHART OPTION: SCATTER PLOT VIEW ---
const scatterChartOption = computed(() => {
    // Data array structure: [0:longitude, 1:latitude, 2:bloom_day_of_year (Color Value), 3:elevation]
    const dataKeyMap = {
        'lon': 0, 
        'lat': 1, 
        'day': 2, 
        'elevation': 3 
    };

    const xAxisLabel = axisOptions.find(o => o.value === xAxisKey.value).label;
    const yAxisLabel = axisOptions.find(o => o.value === yAxisKey.value).label;
    
    const extractValue = (dataPoint, key) => dataPoint.value[dataKeyMap[key]];

    return {
        backgroundColor: '#F7F7F7',

        title: {
            text: `City Data Scatter Plot in ${selectedYear.value}`,
            subtext: `X-Axis: ${xAxisLabel} | Y-Axis: ${yAxisLabel} (Color = Bloom Day)`,
            left: 'center'
        },
        visualMap: {
            min: 30,
            max: 150,
            calculable: true,
            inRange: { color: ['#00BFFF', '#FFFF00', '#FF4500'] },
            text: ['Late Bloom', 'Early Bloom'],
            orient: 'horizontal',
            left: 'center',
            bottom: 20
        },
        grid: {
            left: '10%',
            right: '5%',
            bottom: '15%',
            top: '10%',
            containLabel: true
        },
        xAxis: {
            name: xAxisLabel, 
            nameLocation: 'middle',
            nameGap: 30,
            min: xAxisKey.value === 'day' ? 30 : null, 
            max: xAxisKey.value === 'day' ? 150 : null,
            type: 'value'
        },
        yAxis: {
            name: yAxisLabel, 
            nameLocation: 'middle',
            nameGap: 30,
            type: 'value'
        },
        tooltip: {
            trigger: 'item',
            padding: 8,
            textStyle: { fontSize: 14 },
            formatter: params => {
                if (params.seriesType === 'scatter' && params.name) {
                    return `<strong>${params.name}</strong>`; 
                }
                return null;
            }
        },
        series: [
            {
                name: 'Data Point',
                type: 'scatter',
                symbolSize: cityPointSize.value,
                // Scatter series: [X-value, Y-value, Value for VisualMap (Day)]
                data: scatterData.value.map(d => ({
                    name: d.name, 
                    value: [
                        extractValue(d, xAxisKey.value),
                        extractValue(d, yAxisKey.value),
                        extractValue(d, 'day') // The coloring value must always be the third element (index 2)
                    ]
                })),
                emphasis: {
                    label: { show: false } 
                }
            }
        ]
    };
});
</script>