<template>
  <div class="py-8 px-4 min-h-screen bg-fuchsia-5 transition-all duration-200">
    <div class="max-w-6xl mx-auto bg-fuchsia-50 rounded-2xl p-6 border border-fuchsia-300 shadow-outside mb-16 transition-all duration-200" v-if="mapView">
      <div class="flex justify-between mb-4">
        <h2 class="text-3xl font-bold text-gray-800">
          花見 <i class="font-normal"> hanami </i> - Japan Cherry Blossom Bloom Map
        </h2>
        <div class="flex gap-8">
          <button
            @click="activeView = activeView === 'map' ? 'scatter' : 'map'; mapView = true"
            class="p-4 text-sm font-semibold rounded-lg transition duration-200 border border-fuchsia-300"
            :class="activeView === 'map' ? 'bg-fuchsia-100 text-fuchsia-700 hover:bg-fuchsia-200' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'"
          >
            Switch to {{ activeView === 'map' ? 'Graph' : 'Map' }} View
          </button>
          <button
            @click="mapView = !mapView"
            class="p-4 text-sm font-semibold rounded-lg transition duration-200 border border-fuchsia-300"
            :class="mapView ? 'bg-fuchsia-100 text-fuchsia-700 hover:bg-fuchsia-200' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'"
          >
            Show {{ mapView ? 'Stats' : 'Visuals' }}
          </button>
        </div>
      </div>
      <a class="text-sm text-gray-400" href="https://github.com/Kanahe1800/hanami-bloom-prediction" target="_blank">Data Source: https://github.com/Kanahe1800/hanami-bloom-prediction</a>

      <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <div class="col-span-3 min-h-[600px] border border-fuchsia-300 bg-fuchsia-5 rounded-xl overflow-hidden relative inset-shadow">
          <div v-if="isLoading" class="absolute inset-0 flex items-center justify-center z-10">
            <p class="text-xl font-medium text-gray-600">Loading data...</p>
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
            <div :class="['p-3 rounded-lg border-l-4 border shadow-outside-small', selectedCityStats.isCity ? 'bg-fuchsia-5 border-fuchsia-300' : 'bg-fuchsia-50 border-gray-500']">
              <p class="text-sm font-semibold" :class="selectedCityStats.isCity ? 'text-fuchsia-300' : 'text-gray-700'">
                {{ selectedCityStats.isCity ? 'Selected City' : 'Hover over a city' }}
              </p>
              <span class="text-2xl font-extrabold text-gray-900">{{ selectedCityStats.name }}</span>
            </div>

            <template v-if="selectedCityStats">
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
            <p class="text-sm text-gray-500 py-4">Hover over a city to view its information here.</p>
          </div>

          <div class="space-y-4">
            <div v-if="activeView === 'map'" class="space-y-4">
              <div class="flex justify-between items-end">
                <p class="text-lg font-bold text-gray-800">Map Controls</p>
                <p class="text-sm text-gray-600 cursor-pointer" @click="showMapControls = !showMapControls">
                  {{ showMapControls ? 'hide' : 'show' }}
                </p>
              </div>
              
              <div v-if="showMapControls" class="space-y-3">
                <div class="flex items-center gap-3 p-4 rounded-lg bg-fuchsia-5 border border-gray-200 inset-shadow-small">
                  <label class="text-sm font-semibold text-gray-700 shrink-0 w-16">Dot Size:</label>
                  <input type="range" min="4" max="80" v-model.number="cityPointSize" class="w-full h-2 bg-gray-400 rounded-lg appearance-none cursor-pointer">
                  <span class="text-sm font-bold text-gray-800 w-8 text-right">{{ cityPointSize }}</span>
                </div>
                <div class="flex items-center gap-3 p-4 rounded-lg bg-fuchsia-5 border border-gray-200 inset-shadow-small">
                  <label class="text-sm font-semibold text-gray-700 shrink-0 w-16">Zoom:</label>
                  <input type="range" min="1" max="4" step="0.1" v-model.number="mapZoomLevel" class="w-full h-2 bg-gray-400 rounded-lg appearance-none cursor-pointer">
                  <span class="text-sm font-bold text-gray-800 w-8 text-right">{{ mapZoomLevel.toFixed(1) }}</span>
                </div>
              </div>
            </div>

            <div v-else-if="activeView === 'scatter'" class="space-y-4">
              <p class="text-lg font-bold text-gray-800">Graph Controls</p>
              <div class="space-y-2">
                <label class="text-sm font-semibold text-gray-700">X-Axis:</label>
                <select v-model="xAxisKey" class="w-full bg-gray-50 border border-gray-300 rounded-lg p-3 text-sm inset-shadow-small">
                  <option v-for="option in axisOptions" :key="option.value" :value="option.value">{{ option.label }}</option>
                </select>
                <label class="text-sm font-semibold text-gray-700">Y-Axis:</label>
                <select v-model="yAxisKey" class="w-full bg-gray-50 border border-gray-300 rounded-lg p-3 text-sm inset-shadow-small">
                  <option v-for="option in axisOptions" :key="option.value" :value="option.value">{{ option.label }}</option>
                </select>
              </div>
            </div>
          </div>
        </div>
      </div> 
    </div>

    <div class="max-w-6xl mx-auto bg-fuchsia-50 rounded-2xl p-6 border border-fuchsia-300 shadow-outside mb-32" v-else>
      <div class="flex justify-between items-center mb-8">
        <h2 class="text-3xl font-bold text-gray-800">Bloom Statistics & Trends</h2>
        <button @click="mapView = true" class="p-4 text-sm font-semibold rounded-lg transition duration-200 border border-fuchsia-300 bg-fuchsia-100 text-fuchsia-700 hover:bg-fuchsia-200">
            Return to Visualizer
        </button>
      </div>

      <div class="flex items-center justify-between mb-4">
        <p class="text-gray-900 font-bold text-2xl mx-2">City Specific Data & Trends</p>
        
        <div class="relative w-64 group">
          <input 
            type="text" 
            v-model="citySearchQuery"
            placeholder="Search city..."
            class="w-full bg-white border border-fuchsia-300 rounded-lg px-4 py-2 text-sm shadow-outside-small focus:ring-2 focus:ring-fuchsia-400 outline-none"
            @focus="showDropdown = true"
          />
          <div v-if="showDropdown && filteredCities.length" class="absolute z-60 mt-1 w-full max-h-60 overflow-auto bg-white border border-fuchsia-200 rounded-lg shadow-xl">
            <div 
              v-for="city in filteredCities" 
              :key="city" 
              @click="selectCity(city)"
              class="px-4 py-2 hover:bg-fuchsia-100 cursor-pointer text-sm"
            >
              {{ city }}
            </div>
          </div>
        </div>
      </div>

      <div class="bg-fuchsia-5 p-8 rounded-2xl border border-fuchsia-300 inset-shadow grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8" v-if="selectedCityName">
        <div class="space-y-6">
          <h4 class="text-2xl font-bold text-gray-900 border-b border-fuchsia-200 pb-2">{{ selectedCityName }}</h4>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <p class="text-xs text-gray-500 uppercase font-bold">Current Bloom</p>
              <p class="text-lg font-extrabold text-gray-900">{{ citySpecificStats?.currentYearDate || 'N/A' }}</p>
            </div>
            <div>
              <p class="text-xs text-gray-500 uppercase font-bold">Hist. Average</p>
              <p class="text-lg font-extrabold text-gray-900">{{ citySpecificStats?.avgDate }}</p>
            </div>
            <div>
              <p class="text-xs text-gray-500 uppercase font-bold">Record Earliest</p>
              <p class="text-lg font-extrabold text-gray-900">{{ citySpecificStats?.earliestDate }}</p>
            </div>
            <div>
              <p class="text-xs text-gray-500 uppercase font-bold">Record Latest</p>
              <p class="text-lg font-extrabold text-gray-900">{{ citySpecificStats?.latestDate }}</p>
            </div>
          </div>
          <div class="p-4 rounded-lg border border-fuchsia-300 shadow-sm">
             <p class="text-sm font-medium text-gray-700">Trend vs National Average</p>
             <p class="text-2xl font-gray-900 font-bold">
              {{ Math.abs(citySpecificStats?.trendDiff || 0) }} Days {{ citySpecificStats?.trendStatus }}
            </p>
          </div>
        </div>

        <div class="lg:col-span-2 h-[270px] rounded-xl p-2 border border-fuchsia-300 relative overflow-hidden">
          <v-chart class="chart" :option="cityHistoryChartOption" autoresize />
        </div>
      </div>
      <div class="bg-fuchsia-5 p-8 rounded-2xl border border-fuchsia-300 text-center mb-8 inset-shadow" v-else>
        <p class="text-gray-500 italic">Search and select a city to visualize local historical trends.</p>
      </div>

      <p class="text-gray-900 py-1 rounded-full font-bold text-2xl mb-4 mx-2">National Historical Data</p>
      <div class="bg-fuchsia-5 p-8 rounded-2xl border border-fuchsia-300 inset-shadow mb-8">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div>
                <p class="text-gray-700 font-medium">Earliest Bloom Ever</p>
                <p class="text-2xl font-extrabold text-gray-900">{{ globalStats?.earliest.date }}</p>
                <p class="text-gray-600 mt-1">{{ globalStats?.earliest.city }} ({{ globalStats?.earliest.year }})</p>
            </div>
            <div>
                <p class="text-gray-700 font-medium">Latest Bloom Ever</p>
                <p class="text-2xl font-extrabold text-gray-900">{{ globalStats?.latest.date }}</p>
                <p class="text-gray-600 mt-1">{{ globalStats?.latest.city }} ({{ globalStats?.latest.year }})</p>
            </div>
            <div>
                <p class="text-gray-700 font-medium">National Shift (since 1981)</p>
                <p class="text-2xl font-extrabold text-gray-900">{{ Math.abs(historicalTrend?.diff) }} Days {{ historicalTrend?.status }}</p>
            </div>
        </div>
      </div>

      <p class="text-gray-900 py-1 rounded-full font-bold text-2xl mb-4 mx-2">Statistics for {{ selectedYear }}</p>
      <div class="bg-fuchsia-5 p-8 rounded-2xl border border-fuchsia-300 inset-shadow mb-8">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <p class="text-gray-700 font-medium">Average Bloom Date</p>
            <p class="text-2xl font-extrabold text-gray-900">{{ yearlyStats?.avgDate }}</p>
            <p class="text-xs text-gray-400">Day {{ yearlyStats?.avgDay }} of year</p>
          </div>
          <div>
            <p class="text-gray-700 font-medium">{{ selectedYear }} Earliest</p>
            <p class="text-2xl font-extrabold text-gray-900">{{ dayOfYearToDate(yearlyStats?.earliest, selectedYear) }}</p>
          </div>
          <div>
            <p class="text-gray-700 font-medium">{{ selectedYear }} Latest</p>
            <p class="text-2xl font-extrabold text-gray-900">{{ dayOfYearToDate(yearlyStats?.latest, selectedYear) }}</p>
          </div>
        </div>
      </div>
    </div>

    <div class="mt-8 space-y-6 max-w-6xl mx-auto bg-fuchsia-50 rounded-2xl p-6 border border-fuchsia-300 fixed left-0 right-0 bottom-8 shadow-outside z-50">
      <div class="flex items-center justify-between gap-4 p-4 rounded-lg bg-fuchsia-5 border border-fuchsia-300 inset-shadow">
        <label for="yearSlider" class="text-lg w-12 font-bold shrink-0">{{ selectedYear }}</label>
        
        <button 
          @click="toggleAnimation"
          :disabled="isLoading"
          class="grid place-content-center aspect-square w-10 text-lg font-semibold rounded-full border-gray-500 hover:border transition duration-200 shrink-0 hover:scale-125"
          :class="[isLoading ? 'opacity-50 cursor-not-allowed' : '', isAnimating ? 'border-gray-300 border bg-gray-100' : '']"
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
    const mapView = ref(true)

    const selectedCityName = ref('')
    const citySearchQuery = ref('')
    const showDropdown = ref(false)
    
    const cityPointSize = ref(20)
    const mapZoomLevel = ref(1.5)
    const selectedCityStats = ref(null)
    const activeView = ref('map')
    const showMapControls = ref(true)
    const xAxisKey = ref('day')
    const yAxisKey = ref('lat')

    const isAnimating = ref(false)
    let animationTimer = null

    const axisOptions = [
      { value: 'day', label: 'Day of Year (Bloom Day)' },
      { value: 'lat', label: 'Latitude' },
      { value: 'lon', label: 'Longitude' },
      { value: 'elevation', label: 'Elevation (m)' }
    ]

    const dayOfYearToDate = (dayOfYear, year) => {
      if (!dayOfYear) return 'N/A';
      const date = new Date(year, 0, 1);
      date.setDate(date.getDate() + Math.floor(dayOfYear) - 1);
      return date.toLocaleDateString('en-US', { month: 'long', day: 'numeric' });
    }

    const uniqueCities = computed(() => {
      const cities = [...new Set(fullData.value.map(d => d.city_name))];
      return cities.sort();
    });

    const filteredCities = computed(() => {
      if (!citySearchQuery.value) return uniqueCities.value;
      return uniqueCities.value.filter(c => 
        c.toLowerCase().includes(citySearchQuery.value.toLowerCase())
      );
    });

    const selectCity = (city) => {
      selectedCityName.value = city;
      citySearchQuery.value = city;
      showDropdown.value = false;
    };

    const globalStats = computed(() => {
      if (!fullData.value.length) return null;
      const valid = fullData.value.filter(d => d.bloom_day_of_year);
      const earliest = valid.reduce((prev, curr) => prev.bloom_day_of_year < curr.bloom_day_of_year ? prev : curr);
      const latest = valid.reduce((prev, curr) => prev.bloom_day_of_year > curr.bloom_day_of_year ? prev : curr);
      return {
          earliest: { date: dayOfYearToDate(earliest.bloom_day_of_year, earliest.seasonal_year), city: earliest.city_name, year: earliest.seasonal_year },
          latest: { date: dayOfYearToDate(latest.bloom_day_of_year, latest.seasonal_year), city: latest.city_name, year: latest.seasonal_year }
      };
    });

    const yearlyStats = computed(() => {
      const yearData = fullData.value.filter(d => d.seasonal_year === selectedYear.value);
      if (!yearData.length) return null;
      const days = yearData.map(d => d.bloom_day_of_year);
      const avg = Math.round(days.reduce((a, b) => a + b, 0) / days.length);
      return { avgDay: avg, avgDate: dayOfYearToDate(avg, selectedYear.value), earliest: Math.min(...days), latest: Math.max(...days) };
    });

    const citySpecificStats = computed(() => {
      if (!selectedCityName.value || !fullData.value.length) return null;
      const cityData = fullData.value.filter(d => d.city_name === selectedCityName.value);
      const currentYearData = cityData.find(d => d.seasonal_year === selectedYear.value);
      const days = cityData.map(d => d.bloom_day_of_year).filter(Boolean);
      const avgDay = days.reduce((a, b) => a + b, 0) / days.length;
      const diff = (currentYearData?.bloom_day_of_year || avgDay) - (yearlyStats.value?.avgDay || 100);
      return {
        currentYearDate: currentYearData ? dayOfYearToDate(currentYearData.bloom_day_of_year, selectedYear.value) : null,
        avgDate: dayOfYearToDate(avgDay, 2024),
        earliestDate: dayOfYearToDate(Math.min(...days), 2024),
        latestDate: dayOfYearToDate(Math.max(...days), 2024),
        trendDiff: diff.toFixed(1),
        trendStatus: diff < 0 ? 'Earlier' : 'Later'
      };
    });

    const cityHistoryChartOption = computed(() => {
      if (!selectedCityName.value) return {};
      const cityData = fullData.value
        .filter(d => d.city_name === selectedCityName.value)
        .sort((a, b) => a.seasonal_year - b.seasonal_year);

      return {
        tooltip: { trigger: 'axis' },
        grid: { left: '3%', right: '4%', bottom: '3%', containLabel: false },
        xAxis: { type: 'category', data: cityData.map(d => d.seasonal_year) },
        yAxis: { type: 'value', inverse: true, name: 'Day of Year', splitLine: { show: false } },
        series: [{
          name: 'Bloom Day',
          type: 'line',
          smooth: true,
          data: cityData.map(d => d.bloom_day_of_year),
          itemStyle: { color: '#db2777' },
          areaStyle: { color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{ offset: 0, color: '#fbcfe8' }, { offset: 1, color: '#fff' }]) }
        }]
      };
    });

    const historicalTrend = computed(() => {
      if (!fullData.value.length) return null;
      const years = [...new Set(fullData.value.map(d => d.seasonal_year))].sort();
      const getAvg = (yrs) => {
          const data = fullData.value.filter(d => yrs.includes(d.seasonal_year));
          return data.reduce((a, b) => a + b.bloom_day_of_year, 0) / data.length;
      };
      const diff = getAvg(years.slice(-5)) - getAvg(years.slice(0, 5));
      return { diff: diff.toFixed(1), status: diff < 0 ? 'Earlier' : 'Later' };
    });

    const loadCsvData = async () => {
      isLoading.value = true;
      const response = await fetch(csvFile.value);
      const csvText = await response.text();
      Papa.parse(csvText, {
          header: true,
          dynamicTyping: true,
          complete: results => {
          fullData.value = results.data.filter(row => row.seasonal_year && row.latitude);
          const years = [...new Set(fullData.value.map(d => d.seasonal_year))].filter(y => typeof y === 'number');
          minYear.value = Math.min(...years);
          maxYear.value = Math.max(...years);
          selectedYear.value = maxYear.value;
          isLoading.value = false;
          }
      });
    };

    const scatterData = computed(() => {
      return fullData.value
          .filter(d => d.seasonal_year === selectedYear.value)
          .map(d => ({
          name: d.city_name,
          value: [d.longitude, d.latitude, d.elevation, d.bloom_day_of_year]
          }));
    });

    const handleChartHover = params => {
      if (!params) { selectedCityStats.value = null; return; }
      const d = params.seriesType === 'scatter' ? params.value : null;
      if (d) {
        selectedCityStats.value = { name: params.name, year: selectedYear.value, date: dayOfYearToDate(d[3], selectedYear.value), day: d[3], isCity: true };
      }
    };

    const toggleAnimation = () => {
      if (isAnimating.value) { clearInterval(animationTimer); isAnimating.value = false; }
      else {
          isAnimating.value = true;
          if (selectedYear.value >= maxYear.value) selectedYear.value = minYear.value;
          animationTimer = setInterval(() => {
            if (selectedYear.value < maxYear.value) selectedYear.value++;
            else { clearInterval(animationTimer); isAnimating.value = false; }
          }, 600);
      }
    };

    onMounted(() => {
      echarts.registerMap("japan", japanGeoJson);
      loadCsvData();
      window.addEventListener('click', (e) => {
        if (!e.target.closest('.relative')) showDropdown.value = false;
      });
    });

    const chartOption = computed(() => ({
      backgroundColor: '#fff0',
      title: { text: `Bloom Map ${selectedYear.value}`, left: 'center' },
      visualMap: { min: 30, max: 150, calculable: true, inRange: { color: ['#FF4500', '#FFFF00', '#00BFFF'] }, left: 'center', orient: 'horizontal', bottom: 10 },
      geo: { map: "japan", roam: true, zoom: mapZoomLevel.value, center: [137.5, 38.0], itemStyle: { areaColor: '#fff', borderColor: '#444' } },
      series: [{ type: "scatter", coordinateSystem: "geo", symbolSize: cityPointSize.value, data: scatterData.value }]
    }));

    const scatterChartOption = computed(() => {
        const dataKeyMap = { 'lon': 0, 'lat': 1, 'elevation': 2, 'day': 3 };
        return {
            title: { text: `Bloom Analysis ${selectedYear.value}`, left: 'center' },
            xAxis: { type: 'value', name: xAxisKey.value },
            yAxis: { type: 'value', name: yAxisKey.value },
            visualMap: { min: 30, max: 150, inRange: { color: ['#FF4500', '#FFFF00', '#00BFFF'] }, show: true },
            series: [{ type: 'scatter', symbolSize: cityPointSize.value, data: scatterData.value.map(d => ({ name: d.name, value: [d.value[dataKeyMap[xAxisKey.value]], d.value[dataKeyMap[yAxisKey.value]], d.value[3]] })) }]
        };
    });

    onUnmounted(() => clearInterval(animationTimer));
</script>

<style scoped>
    .inset-shadow { box-shadow: 8px 8px 12px rgba(0, 0, 0, 0.081) inset, -12px -12px 12px rgb(255, 255, 255) inset; }
    .inset-shadow-small { box-shadow: 4px 4px 6px rgba(0, 0, 0, 0.041) inset, -6px -6px 6px rgb(255, 255, 255) inset; }
    .shadow-outside { box-shadow: 8px 8px 12px rgba(0, 0, 0, 0.081), -12px -12px 12px rgb(255, 255, 255); } 
    .shadow-outside-small { box-shadow: 4px 4px 6px rgba(0, 0, 0, 0.081), -6px -6px 6px rgb(255, 255, 255); }
    .bg-fuchsia-5 { background-color: oklch(99% 0.005 340.058); }
</style>