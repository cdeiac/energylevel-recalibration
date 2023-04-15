<template>
  <v-card v-if="targetActivity.activityName">
    <highcharts ref="activity-chart" :options="chartOptions"></highcharts>
  </v-card>
  <v-card v-else>
    <v-card-title> Select an activity...</v-card-title>
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
    targetActivity: {type: Object, required: true},
    comparisonActivity: {type: Object, required: false},
    activities: {type: Array, required: true}
  },
  data() {
    return {

    }
  },
  computed: {
    chartOptions() {
      let maxDuration = 0;
      let maxDistCov = 0;
      let maxActCal = 0;
      let maxAvgHR = 0;
      let maxAvgPace = 0;
      let maxAvgRunCad = 0;
      let maxAvgSp = 0;
      let maxMaxHR = 0;
      let maxMaxPac = 0;
      let maxMaxRunCad = 0;
      let maxMaxSpeed = 0;
      let maxSteps = 0;
      let maxTotElevGain = 0;
      let activities = this.activities;
      Object.keys(this.activities).forEach(function(idx) {
        const activity = activities[idx];
        if (activity.durationInSeconds > maxDuration) {
          maxDuration = activity.durationInSeconds;
        }
        if (activity.distanceInMeters > maxDistCov) {
          maxDistCov = activity.distanceInMeters;
        }
        if (activity.activeKilocalories > maxActCal) {
          maxActCal = activity.activeKilocalories;
        }
        if (activity.averageHeartRateInBeatsPerMinute > maxAvgHR) {
          maxAvgHR = activity.averageHeartRateInBeatsPerMinute;
        }
        if (activity.averagePaceInMinutesPerKilometer > maxAvgPace) {
          maxAvgPace = activity.averagePaceInMinutesPerKilometer;
        }
        if (activity.averageRunCadenceInStepsPerMinute > maxAvgRunCad) {
          maxAvgRunCad = activity.averageRunCadenceInStepsPerMinute;
        }
        if (activity.averageSpeedInMetersPerSecond > maxAvgSp) {
          maxAvgSp = activity.averageSpeedInMetersPerSecond;
        }
        if (activity.maxHeartRateInBeatsPerMinute > maxMaxHR) {
          maxMaxHR = activity.maxHeartRateInBeatsPerMinute;
        }
        if (activity.maxPaceInMinutesPerKilometer > maxMaxPac) {
          maxMaxPac = activity.maxPaceInMinutesPerKilometer;
        }
        if (activity.maxRunCadenceInStepsPerMinute > maxMaxRunCad) {
          maxMaxRunCad = activity.maxRunCadenceInStepsPerMinute;
        }
        if (activity.maxSpeedInMetersPerSecond > maxMaxSpeed) {
          maxMaxSpeed = activity.maxSpeedInMetersPerSecond;
        }
        if (activity.steps > maxSteps) {
          maxSteps = activity.steps;
        }
        if (activity.totalElevationGainInMeters > maxTotElevGain) {
          maxTotElevGain = activity.totalElevationGainInMeters;
        }
      });

      return {
        title: {
          text: this.formatTitle()
        },
        pane: {
          size: '75%'
        },
        credits: {
          enabled: false
        },
        chart: {
          parallelCoordinates: true,
          parallelAxes: {

          },
          polar: true
        },

        xAxis: {
          categories: [
            "Duration", "Distance covered", "Active calories", "Avg. heart rate", "Avg. pace",
            "Avg. run cadence", "Avg. speed", "Max. heart rate", "Max. pace", "Max. run cadence",
            "Max. speed", "Steps", "Tot. elevation gain"],
          labels: {
            style: {
              color: 'black'
            }
          }
        },

        legend: {
          enabled: false
        },

        yAxis: [
          {min: 0, max: maxDuration, showLastLabel: true},
          {min: 0, max: maxDistCov, showLastLabel: true},
          {min: 0, max: maxActCal, showLastLabel: true},
          {min: 0, max: maxAvgHR, showLastLabel: true},
          {min: 0, max: maxAvgPace, showLastLabel: true},
          {min: 0, max: maxAvgRunCad, showLastLabel: true},
          {min: 0, max: maxAvgSp, showLastLabel: true},
          {min: 0, max: maxMaxHR, showLastLabel: true},
          {min: 0, max: maxMaxPac, showLastLabel: true},
          {min: 0, max: maxMaxRunCad, showLastLabel: true},
          {min: 0, max: maxMaxSpeed, showLastLabel: true},
          {min: 0, max: maxSteps, showLastLabel: true},
          {min: 0, max: maxTotElevGain, showLastLabel: true}
        ],

        series: [{
          name: this.formatSeriesName(this.targetActivity),
          color: "#2f7ed8",
          data: [
            this.targetActivity.durationInSeconds, this.targetActivity.distanceInMeters,
            this.targetActivity.activeKilocalories, this.targetActivity.averageHeartRateInBeatsPerMinute,
            this.targetActivity.averagePaceInMinutesPerKilometer, this.targetActivity.averageRunCadenceInStepsPerMinute,
            this.targetActivity.averageSpeedInMetersPerSecond, this.targetActivity.maxHeartRateInBeatsPerMinute,
            this.targetActivity.maxPaceInMinutesPerKilometer, this.targetActivity.maxRunCadenceInStepsPerMinute,
            this.targetActivity.maxSpeedInMetersPerSecond, this.targetActivity.steps,
            this.targetActivity.totalElevationGainInMeters,
          ]
        },
          {
            name: this.formatSeriesName(this.comparisonActivity),
            color: "black",
            data: [
              this.comparisonActivity.durationInSeconds, this.comparisonActivity.distanceInMeters,
              this.comparisonActivity.activeKilocalories, this.comparisonActivity.averageHeartRateInBeatsPerMinute,
              this.comparisonActivity.averagePaceInMinutesPerKilometer, this.comparisonActivity.averageRunCadenceInStepsPerMinute,
              this.comparisonActivity.averageSpeedInMetersPerSecond, this.comparisonActivity.maxHeartRateInBeatsPerMinute,
              this.comparisonActivity.maxPaceInMinutesPerKilometer, this.comparisonActivity.maxRunCadenceInStepsPerMinute,
              this.comparisonActivity.maxSpeedInMetersPerSecond, this.comparisonActivity.steps,
              this.comparisonActivity.totalElevationGainInMeters,
            ]
          }
        ]
      }
    }
  },
  methods: {
    formatSeriesName(activity) {
      return `${activity.activityName} (${new Date(activity.startTimeOffsetInSeconds * 1000).toDateString()})`
    },
    formatTitle() {
      console.log("this", this);
      console.log("this.comparisonActivity", this.comparisonActivity);
      if (!this.comparisonActivity.activityName) {
        return this.targetActivity.activityName;
      }
      else {
        return `Comparing ${this.targetActivity.activityName} (${new Date(this.targetActivity.startTimeOffsetInSeconds * 1000).toDateString()})
        with ${this.comparisonActivity.activityName} (${new Date(this.comparisonActivity.startTimeOffsetInSeconds * 1000).toDateString()})`
      }
    }
  }
}





</script>

<style scoped>

</style>
