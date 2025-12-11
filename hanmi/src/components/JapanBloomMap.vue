<template>
    <div class="py-8 px-4 min-h-screen bg-fuchsia-5 ">
        <div class="max-w-6xl mx-auto bg-fuchsia-50 rounded-2xl p-6 border border-fuchsia-300 shadow-outside mb-[100px]">
            <div class="flex justify-between mb-4">
                <h2 class="text-3xl font-bold text-gray-800">
                花見 <i class="font-normal"> hanami </i> - Japan Cherry Blossom Bloom Map
                </h2>
                <div class="flex justify-end mb-2">
                    <button
                        @click="activeView = activeView === 'map' ? 'scatter' : 'map'"
                        class="px-4 py-2 text-sm font-semibold rounded-lg transition duration-200"
                        :class="activeView === 'map' ? 'bg-fuchsia-100 text-fuchsia-700 hover:bg-fuchsia-200' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'"
                        >
                    Switch to {{ activeView === 'map' ? 'Scatter Plot' : 'Map View' }}
                    </button>
                </div>
            </div>
                <a class="text-sm text-gray-400" href="https://github.com/Kanahe1800/hanami-bloom-prediction" target="_blank">Data Source: https://github.com/Kanahe1800/hanami-bloom-prediction</a>

            <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">

                <div class="col-span-3 min-h-[600px] border border-fuchsia-300 bg-fuchsia-5 rounded-xl overflow-hidden relative inset-shadow">

                    <div v-if="isLoading" class="absolute inset-0 .bg-fuchsia-5 flex items-center justify-center z-10">
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

                <div class="bg-fuchsia-5 border border-fuchsia-300 rounded-xl p-4 space-y-4 inset-shadow">

                    <div v-if="selectedCityStats" class="space-y-4">
                        <div 
                            :class="[
                            'p-3 rounded-lg border-l-4 border shadow-outside-small',
                            selectedCityStats.isCity ? 'bg-fuchsia-5 border-fuchsia-300' : 'bg-fuchsia-50 border-gray-500'
                            ]"
                        >
                            <p class="text-sm font-semibold" :class="selectedCityStats.isCity ? 'text-fuchsia-300' : 'text-gray-700'">
                                {{ selectedCityStats.isCity ? 'Selected City' : 'Selected Prefecture' }}
                            </p>
                            <span class="text-2xl font-extrabold text-gray-900">{{ selectedCityStats.name }}</span>
                        </div>

                        <template v-if="selectedCityStats.isCity">
                            <div class="bg-fuchsia-5 p-3 rounded border border-fuchsia-200 inset-shadow-small">
                                <p class="text-sm font-semibold text-gray-700">Year</p>
                                <span class="text-xl font-extrabold text-gray-900">{{ selectedCityStats.year }}</span>
                            </div>

                            <div class="bg-fuchsia-5 p-3 rounded border border-fuchsia-200 inset-shadow-small">
                                <p class="text-sm font-semibold text-gray-700">Bloom Date</p>
                                <span class="text-xl font-extrabold text-gray-900">{{ selectedCityStats.date }}</span>
                            </div>

                            <div class="bg-fuchsia-5 p-3 rounded border border-fuchsia-200 inset-shadow-small">
                                <p class="text-sm font-semibold text-gray-700">Day of Year</p>
                                <span class="text-xl font-extrabold text-gray-900">{{ selectedCityStats.day }}</span>
                            </div>
                        </template>

                    </div>

                    <div v-else>
                        <p class="text-sm text-gray-500 py-4">
                            Hover over a city to view its information here.
                        </p>
                    </div>

                    <div class="space-y-4">
                        <div v-if="activeView === 'map'" class="space-y-4">
                            <div class="flex justify-between items-end">

                                <p class="text-lg font-bold text-gray-800">Map Controls</p>
                                
                                <p v-if="showMapControls" class="text-sm text-gray-600 cursor-pointer" @click="showMapControls = !showMapControls" >hide</p>
                                <p v-else class="text-sm text-gray-600 cursor-pointer" @click="showMapControls = !showMapControls">show</p>
                            </div>
                            
                            <div v-if="showMapControls" class="flex items-center gap-3 p-4 rounded-lg bg-fuchsia-5 border border-gray-200 inset-shadow-small">
                                <label for="pointSizeSlider" class="text-sm font-semibold text-gray-700 shrink-0 w-16">
                                    Dot Size:
                                </label>
                                <input 
                                    type="range" 
                                    id="pointSizeSlider" 
                                    min="4" 
                                    max="80" 
                                    step="1" 
                                    v-model.number="cityPointSize"
                                    class="w-full h-2 bg-gray-400 rounded-lg appearance-none cursor-pointer"
                                >
                                <span class="text-sm font-bold text-gray-800 w-8 text-right shrink-0">
                                    {{ cityPointSize }}
                                </span>
                            </div>

                            <div v-if="showMapControls" class="flex items-center gap-3 p-4 rounded-lg bg-fuchsia-5 border border-gray-200 inset-shadow-small">
                                <label for="zoomSlider" class="text-sm font-semibold text-gray-700 shrink-0 w-16">
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

                            <div v-if="showMapControls" class="flex items-center gap-3 p-4 rounded-lg bg-fuchsia-5 border border-gray-200 inset-shadow-small">
                                <label for="speedSlider" class="text-sm font-semibold text-gray-700 shrink-0 w-16">
                                    Animation Speed:
                                </label>
                                <input 
                                    type="range" 
                                    id="speedSlider" 
                                    min="0.5" 
                                    max="4" 
                                    step="0.1" 
                                    v-model.number="timeInterval"
                                    class="w-full h-2 bg-gray-400 rounded-lg appearance-none cursor-pointer"
                                >
                                <span class="text-sm font-bold text-gray-800 w-8 text-right shrink-0">
                                    {{ timeInterval.toFixed(1) }}
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
                                    class="w-full  bg-gray-50 border border-gray-300 rounded-lg p-4 text-gray-800 text-sm focus:ring-fuchsia-500 focus:border-fuchsia-500 inset-shadow-small">
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
                                    class="w-full bg-gray-50 border border-gray-300 rounded-lg p-4 text-gray-800 text-sm focus:ring-fuchsia-500 focus:border-fuchsia-500 inset-shadow-small">
                                    <option v-for="option in axisOptions" :key="option.value" :value="option.value">
                                        {{ option.label }}
                                    </option>
                                </select>
                            </div>

                            <div class="flex items-center gap-3 p-4 rounded-lg bg-fuchsia-5 border border-gray-200 inset-shadow-small">
                                <label for="pointSizeSlider" class="text-sm font-semibold text-gray-700 shrink-0 w-8">
                                    Dot Size:
                                </label>
                                <input 
                                    type="range" 
                                    id="pointSizeSlider" 
                                    min="4" 
                                    max="80" 
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
        </div>
        <div class="mt-8 space-y-6 w-6xl mx-auto bg-fuchsia-50 rounded-2xl p-6 border border-fuchsia-300 fixed left-0 right-0 bottom-8 shadow-outside">
            <div class="flex items-center justify-between gap-4 p-4 rounded-lg bg-fuchsia-5 border border-fuchsia-300 inset-shadow">
                <label for="yearSlider" class="text-lg w-12  font-bold shrink-0">
                    {{ selectedYear }}
                </label>
                
                <button 
                    @click="toggleAnimation"
                    :disabled="isLoading"
                    class="grid place-content-center aspect-square w-10 text-lg font-semibold rounded-full border-grey-500 hover:border transition duration-200 shrink-0 hover:scale-125"
                    :class="[
                        isLoading ? 'opacity-50 cursor-not-allowed' : '',
                        isAnimating ? 'border-gray-300 border bg-gray-100' : '',
                    ]"
                >
                    <span v-if="!isAnimating" class="text-black">▶</span>
                    <span v-else class="text-black">■</span>
                </button>
                
                <input 
                    type="range" 
                    id="yearSlider" 
                    :min="minYear" 
                    :max="maxYear" 
                    step="1" 
                    v-model.number="selectedYear"
                    :disabled="isAnimating || isLoading"
                    class="w-full h-2 rounded-lg appearance-none cursor-pointer"
                    :class="isAnimating ? 'bg-gray-300' : 'bg-gray-600'"
                >
            </div>
        </div>
    </div>
</template>

<script setup>
    import { ref, watch, computed, onMounted, onUnmounted } from 'vue'
    import VChart from 'vue-echarts'
    import * as echarts from 'echarts'
    import * as Papa from 'papaparse'


    import japanGeoJson from '@/assets/japan.geo.json'
    const csvFile = ref('/all_cities_cat.csv')

    const selectedYear = ref(2025)
    const fullData = ref([])
    const minYear = ref(1981)
    const maxYear = ref(2025)
    const isLoading = ref(true)

    const cityPointSize = ref(20)
    const mapZoomLevel = ref(1.5)
    const selectedCityStats = ref(null)
    const activeView = ref('map')
    const showMapControls = ref('true')
    const xAxisKey = ref('day')
    const yAxisKey = ref('lat')

    const isAnimating = ref(false)
    const timeInterval = ref(1)
    let animationTimer = null


    const axisOptions = [
        { value: 'day', label: 'Day of Year (Bloom Day)' },
        { value: 'lat', label: 'Latitude' },
        { value: 'lon', label: 'Longitude' },
        { value: 'elevation', label: 'Elevation (m)' }
    ]

    const processedJapanGeoJson = JSON.parse(JSON.stringify(japanGeoJson))

    processedJapanGeoJson.features.forEach(feature => {
        if (feature.properties && feature.properties.nam_ja) {
            feature.name = feature.properties.nam_ja; 
        }
    })
    
    const dayOfYearToDate = (dayOfYear, year) => {
        const date = new Date(year, 0, 1);
        date.setDate(date.getDate() + dayOfYear - 1);
        return date.toLocaleDateString('en-US', { month: 'long', day: 'numeric' });
    }

    const loadCsvData = async () => {
        isLoading.value = true;

        const response = await fetch(csvFile.value);
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
                    row.elevation &&
                    row.bloom_day_of_year
                );

                const years = [...new Set(fullData.value.map(d => d.seasonal_year))].filter(y => typeof y === 'number');
                minYear.value = Math.min(...years);
                maxYear.value = Math.max(...years);
                selectedYear.value = maxYear.value;

                isLoading.value = false;
            }
        });
    };

    const scatterData = computed(() => {
        if (isLoading.value) return [];

        return fullData.value
            .filter(d => d.seasonal_year === selectedYear.value)
            .map(d => ({
                name: d.city_name,
                value: [d.longitude, d.latitude, d.elevation, d.bloom_day_of_year], 
                city_name: d.city_name
            }));
    });

    const handleChartHover = params => {
        if (!params || (params.seriesType !== 'scatter' && params.componentType !== 'geo')) {
            selectedCityStats.value = null;
            return;
        }

        if (activeView.value === 'scatter') {
            const cityData = scatterData.value.find(d => d.name === params.name);
            if (!cityData) return;

            const day = cityData.value[3]; 
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
        
        if (activeView.value === 'map') {
            if (params.seriesType === 'scatter') {
                const year = selectedYear.value;
                const [lon, lat, elevation ,day] = params.value; 
                const bloomDate = dayOfYearToDate(day, year);

                selectedCityStats.value = {
                    name: params.name,
                    year: year,
                    date: bloomDate,
                    day: day,
                    elevation: elevation,
                    isCity: true
                };
                return; 
            }
            if (params.componentType === 'geo' && params.name) {
                selectedCityStats.value = {
                    name: params.name,
                    isCity: false
                };
                return;
            }
        }
        selectedCityStats.value = null;
    };

    const startAnimation = () => {
        if (isLoading.value) return;

        isAnimating.value = true;
        if (selectedYear.value >= maxYear.value) {
            selectedYear.value = minYear.value;
        }

        animationTimer = setInterval(() => {
            if (selectedYear.value < maxYear.value) {
                selectedYear.value++;
            } else {
                stopAnimation();
            }
        }, 500 / timeInterval.value);
        console.log(timeInterval.value)
    };

    const stopAnimation = () => {
        if (animationTimer) {
            clearInterval(animationTimer);
            animationTimer = null;
        }
        isAnimating.value = false;
    };

    const toggleAnimation = () => {
        if (isAnimating.value) {
            stopAnimation();
        } else {
            startAnimation();
        }
    };

    onUnmounted(() => {
        stopAnimation(); 
    });

    onMounted(() => {
        echarts.registerMap("japan", processedJapanGeoJson);
        loadCsvData();
    });

    const chartOption = computed(() => ({
        backgroundColor: '#fff0', 

        title: {
            text: `Cherry Blossom Bloom Day in ${selectedYear.value}`,
            subtext: 'Days since January 1 (Lighter = Earlier Bloom)',
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
            bottom: 0
        },

        geo: {
            map: "japan",
            roam: true,
            aspectScale: 1,
            zoom: mapZoomLevel.value,
            center: [137.5, 38.0], 
            
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
                
                if (params.seriesType === 'scatter') {
                    const [lon, lat, elevation, day] = params.value; 
                    const bloomDate = dayOfYearToDate(day, year);
                    
                    return `<strong>${params.name}</strong><br>
                            Date: <strong>${bloomDate}</strong><br>
                            Day of Year: ${day}`;
                }

                // Show only prefecture name on map hover
                if (params.componentType === 'geo') {
                    return `<strong>${params.name} Prefecture</strong>`;
                }

                return "No Data";
            }
        },
        series: [
            {
                type: "scatter",
                coordinateSystem: "geo",
                symbolSize: cityPointSize.value,
                emphasis: { label: { show: false, formatter: '{b}', position: 'right' } },
                // data: [lon, lat, elevation, day]
                data: scatterData.value
            }
        ]
    }));


    //SCATTER PLOT
    const scatterChartOption = computed(() => {
        const dataKeyMap = {
            'lon': 0, 
            'lat': 1, 
            'elevation': 2, 
            'day': 3
        };

        const xAxisLabel = axisOptions.find(o => o.value === xAxisKey.value).label;
        const yAxisLabel = axisOptions.find(o => o.value === yAxisKey.value).label;
        
        const extractValue = (dataPoint, key) => dataPoint.value[dataKeyMap[key]];

        return {
            backgroundColor: '#fff0',

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
                bottom: 0
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
                        const cityData = scatterData.value.find(d => d.name === params.name);
                        if (!cityData) return;
                        const day = cityData.value[3]; 
                        const bloomDate = dayOfYearToDate(day, selectedYear.value);

                        return `<strong>${params.name}</strong><br>
                                Date: <strong>${bloomDate}</strong><br>
                                Day of Year: ${day}`; 
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

<style scoped>
    .inset-shadow {
        box-shadow: 8px 8px 12px rgba(0, 0, 0, 0.081) inset,
                     -12px -12px 12px rgb(255, 255, 255) inset;
    }

    .inset-shadow-small {
        box-shadow: 4px 4px 6px rgba(0, 0, 0, 0.041) inset,
                     -6px -6px 6px rgb(255, 255, 255) inset;
    }

    .shadow-outside {
        box-shadow: 8px 8px 12px rgba(0, 0, 0, 0.081),
                     -12px -12px 12px rgb(255, 255, 255);
    } 
    
    .shadow-outside-small {
        box-shadow: 4px 4px 6px rgba(0, 0, 0, 0.081),
                     -6px -6px 6px rgb(255, 255, 255);
    }

    .bg-fuchsia-5 {
        background-color: oklch(99% 0.005 340.058);
    }
</style>