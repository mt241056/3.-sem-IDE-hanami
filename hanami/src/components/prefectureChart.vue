<template>
    <div class="grid place-items-center w-full">
        <div class="w-1/2 aspect-square">

            <canvas ref="mapCanvas" class=" "></canvas>
        </div>
    </div>
</template>

<script setup>
    import { ref, onMounted, nextTick } from 'vue';
    import { Chart } from 'chart.js';
    import {
        ChoroplethController,
        ProjectionScale,
        ColorScale,
        GeoFeature,
    } from 'chartjs-chart-geo';

    Chart.register(
        ChoroplethController,
        ProjectionScale,
        ColorScale,
        GeoFeature
    );


    import * as topojson from 'topojson-client';
    import japanTopo from '../assets/japan-prefectures.geo.json';

    const mapCanvas = ref(null);
    let mapChart = null;

    const initializeMap = () => {
        const features = japanTopo.features;

        const dataMap = new Map([
            ['Tokyo', 50],
            ['Osaka', 35],
            ['Hokkaido', 20],
            ['Fukuoka', 30],
        ]);

        features.forEach((feature) => {
            feature.value = dataMap.get(feature.properties.name) || 0;
        });

        mapChart = new Chart(mapCanvas.value.getContext('2d'), {
            type: 'choropleth',
            data: {
                labels: features.map((feature) => feature.properties.name),
                datasets: [
                    {
                        label: 'Prefecture Data',

                        data: features.map((feature) => ({
                            feature: feature,
                            value: feature.value
                        })),
                    },
                ],
            },
            options: {
                maintainAspectRatio: false,
                aspectRatio: 1,
                scales: {
                    projection: {
                        axis: 'x',
                        projection: 'mercator',
                        projectionScale: 1,
                        fit: true,
                    },
                    color: {
                        axis: 'x',
                        quantize: 5,
                        legend: {
                            display: false
                        },
                    },
                },
                plugins: {
                    legend: {
                        display: false
                    }
                },
                tooltip: {
                    mode: 'nearest',
                    intersect: false,

                    // *** Define the text that appears in the tooltip ***
                    callbacks: {
                        title: function(context) {
                            return context[0].raw.feature.properties.name;
                        },
                        label: function(context) {
                            const value = context.raw.value;
                            return `Data Value: ${value}`;
                        }
                    }
                },
            },
        });
    };

    onMounted(() => {
        nextTick(() => {
            initializeMap();
        });
    });
</script>
