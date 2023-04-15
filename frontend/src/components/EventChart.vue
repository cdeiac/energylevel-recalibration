<template>
  <v-card v-if="targetActivities.length > 0 || targetSleeps.length > 0">
    <highcharts ref="event-chart"  :options="chartOptions"></highcharts>
  </v-card>
  <v-card v-else>
    <v-card-title>Select some activities...</v-card-title>
  </v-card>

</template>

<script>

import {Chart} from "highcharts-vue";
import Xrange from "highcharts/modules/xrange";
import Highcharts from "highcharts";

Xrange(Highcharts)

export default {
  components: {
    highcharts: Chart,
  },
  props: {
    targetActivities: {type: Array, required: true},
    comparisonActivities: {type: Array, required: true}
  },
  data() {
    return {
    }
  },
  computed: {
    chartOptions() {
      const vm = this;
      return {
        chart: {
          type: 'xrange',
          //styledMode: true,
        },
        title: {
          text: 'Events'
        },
        xAxis: {
          type: 'datetime',
          min: new Date(new Date(this.targetActivities[0].startTimeOffsetInSeconds * 1000).setHours(0, 0, 0, 0)).getTime(),
          max: new Date(new Date(this.targetActivities[0].startTimeOffsetInSeconds * 1000).setHours(24, 0, 0, 0)).getTime(),
          labels: {
            formatter: function(p) {
              return Highcharts.dateFormat('%H:%M', p.value)
            }
          },
          tickInterval: 1000 * 60 * 60,
        },
        yAxis: {
          title: {
            text: ''
          },
          labels: {
            enabled: false
          },
          categories: ['Suggestion', 'Reference'],
          reversed: false
        },
        legend: {
          enabled: false
        },
        credits: {
          enabled: false
        },
        /*
        tooltip: {
          xDateFormat: '%H:%M',
        },*/
        tooltip: {
          formatter: function() {
            return  Highcharts.dateFormat('%H:%M', this.x)
              + " - "
              + Highcharts.dateFormat('%H:%M', this.x2);
          }
        },
        plotOptions: {
          series: {
            allowPointSelect: true,
            marker: {
              states: {
                select: {
                  fillColor: 'red',
                  lineWidth: 1
                }
              }
            },
            cursor: 'pointer',
            events: {
              click: function (event) {
                console.log("point clicked", event.point);
                vm.onClick(event.point);
              }
            }
          }
        },
        series: [{
          colorByPoint: true,
          // pointPadding: 0,
          // groupPadding: 0,
          //pointWidth: 20,
          data: this.mapSeriesData(),
          dataLabels: {
            enabled: true,
            useHTML: true,
            formatter: function () {
              return vm.formatActivityIcon(this)
            },
          }
        }]
      }
    },
  },
  methods: {
    formatSeriesName(activity) {
      return `${activity.activityName} (${new Date(activity.startTimeOffsetInSeconds * 1000).toDateString()})`
    },
    formatTitle() {
      if (!this.comparisonActivity.activityName) {
        return this.targetActivity.activityName;
      }
      else {
        return `Comparing ${this.targetActivity.activityName} (${new Date(this.targetActivity.startTimeOffsetInSeconds * 1000).toDateString()})
        with ${this.comparisonActivity.activityName} (${new Date(this.comparisonActivity.startTimeOffsetInSeconds * 1000).toDateString()})`
      }
    },
    formatActivityIcon(e) {
      // icons
      const runIcon = `<span class="mdi mdi-run"></span>`
      return runIcon;
    },
    onClick(point) {
      let clickedActivity = null
      console.log("onClick", point);
      console.log("filter comp activities", this.comparisonActivities);
      if (point.y === 0) {
        // target series
        clickedActivity = this.targetActivities.filter(a => (a.startTimeOffsetInSeconds * 1000) === point.x)

      }
      else {
        clickedActivity = this.comparisonActivities.filter(a => (a.startTimeOffsetInSeconds * 1000) === point.x)[0]
      }
      this.$emit("selectActivity", clickedActivity[0]);
    },
    mapSeriesData() {
      // map activities
      let data = this.mapActivityData(this.targetActivities, 0, false);
      if (this.comparisonActivities.length > 0) {
        data.push(...this.mapActivityData(this.comparisonActivities, 1, true))
      }
      return data;
    },
    mapActivityData(activities, series, multipleSeries) {

      if (!multipleSeries) {
        // map data normally
        let act_arr = []
        activities.map(a => {
          act_arr.push({
            x: a.startTimeOffsetInSeconds * 1000,
            x2: a.endTimeOffsetInSeconds * 1000,
            y: series,
            colorIndex: 0,
          })
        })
        return act_arr;
      }
      else {
        // synchronize dates
        let act_arr = []
        activities.map(a => {
          const targetStartTime = new Date(this.targetActivities[0].startTimeOffsetInSeconds * 1000)
          const targetEndTime = new Date(this.targetActivities[0].endTimeOffsetInSeconds * 1000)
          const startTime = new Date(a.startTimeOffsetInSeconds * 1000)
          const endTime = new Date(a.endTimeOffsetInSeconds * 1000)
          targetStartTime.setHours(startTime.getHours(), startTime.getMinutes())
          targetEndTime.setHours(endTime.getHours(), endTime.getMinutes())

          act_arr.push({
            x: targetStartTime.getTime(),
            x2: targetEndTime.getTime(),
            y: series,
            colorIndex: 0,
          })
        })
        console.log("activity array", act_arr);
        return act_arr;
      }
    },
    mapColorIndex(activity) {
      if (activity.activityName === "Walking") {
        return 0;
      }
      // TODO: map sleep and activities
    }
  }
}





</script>

<style scoped>
highcharts {
  height: 100px;
}
</style>
