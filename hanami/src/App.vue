<script setup lang="ts">
    import PrefectureChart from './components/prefectureChart.vue';
    import japanGeo from "./assets/japan-prefectures.geo.json";
    const prefectureValues = {
        Tokyo: 95,
        Osaka: 80,
        Hokkaido: 60,
        Aichi: 75,
        Fukuoka: 55
    };
</script>

<template>
    <div>
        <PrefectureChart />
    </div>
</template>