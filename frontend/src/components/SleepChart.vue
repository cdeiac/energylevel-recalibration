<template>
  <v-card>
    <!--v-card-title> Sleep Overview </v-card-title-->
    <highcharts ref="sleep-chart" :options="chartOptions"></highcharts>
  </v-card>
</template>

<script>

import {Chart} from "highcharts-vue";
import More from "highcharts/highcharts-more";
import ParallelCoordinates from "highcharts/modules/parallel-coordinates";
import Highcharts from "highcharts";

More(Highcharts)
ParallelCoordinates(Highcharts)

export default {
  components: {
    highcharts: Chart
  },
  props: {
    targetSleep: {type: Object, required: true},
    comparisonSleep: {type: Object, required: false},
  },
  data() {
    return {

    }
  },
  computed: {
    chartOptions() {
      console.log("sleepChart target", this.targetSleep);
      console.log("sleepChart comparison", this.comparisonSleep);
      return {
        chart: {
          type: 'column',
          animation: false
        },
        title: {
          text: 'Sleep',
        },
        xAxis: {
          categories: this.comparisonSleep.summaryId ? ['Suggestion', 'Reference'] : ['Suggestion']
        },
        yAxis: {
          min: 0,
          title: {
            text: 'Minutes'
          },
          stackLabels: {
            enabled: true,
          }
        },
        credits: {
          enabled: false
        },
        legend: {
          enabled: false
        },
        tooltip: {
          headerFormat: '<b>{point.x}</b><br/>',
          pointFormat: '{series.name}: {point.y} min'
        },
        plotOptions: {
          column: {
            stacking: 'normal',
            dataLabels: {
              enabled: true
            }
          }
        },
        series: this.mapSleepData()
      }
    }
  },
  methods: {
    mapSleepData() {
      let dataArr = []
      let deep = {
        name: "Deep Sleep",
        data: [],
        color: "#004D40"
      };
      let light = {
        name: "Light Sleep",
        data: [],
        color: "#00695C"
      };
      let rem = {
        name: "REM Sleep",
        data: [],
        color: "#009688"
      };
      let awake = {
        name: "Awake Time",
        data: [],
        color: "#4DB6AC"
      };

      deep.data.push(this.targetSleep.deepSleepDurationInSeconds / 60)
      light.data.push(this.targetSleep.lightSleepDurationInSeconds / 60)
      rem.data.push(this.targetSleep.remSleepInSeconds / 60)
      awake.data.push(this.targetSleep.awakeDurationInSeconds / 60)

      if (this.comparisonSleep.summaryId) {
        deep.data.push(this.comparisonSleep.deepSleepDurationInSeconds / 60)
        light.data.push(this.comparisonSleep.lightSleepDurationInSeconds / 60)
        rem.data.push(this.comparisonSleep.remSleepInSeconds / 60)
        awake.data.push(this.comparisonSleep.awakeDurationInSeconds / 60)
      }
      dataArr.push(deep, light, rem, awake)
      return dataArr;
    }
  }
}





</script>

<style scoped>

</style>
