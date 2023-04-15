<template>
  <div>
    <highcharts ref="bb-chart" :options="chartOptions"></highcharts>
  </div>
</template>

<script>
import Highcharts from "highcharts";
import { Chart } from "highcharts-vue";
import draggablePoints from "highcharts/modules/draggable-points";
import { mdiRun } from "@mdi/js";

draggablePoints(Highcharts)

export default {
  components: {
    highcharts: Chart
  },
  props: {
    targetBodyBatteryData: { type: Array, required: true },
    comparisonBodyBatteryData: { type: Array, required: false },
    targetDate: { type: Date, required: true },
    targetActivities: { type: Array, required: true },
    comparisonActivities: { type: Array, required: false }
  },
  data() {
    return {
      loaded: false,
      //vm: this,
      selectedPoints: [],
      runPath: mdiRun
    }
  },
  computed: {
    chartOptions() {
      console.log("computing chartOptions. . .", this.targetBodyBatteryData);
      const vm = this;
      return {
        time: {
          useUTC: false,
          timezone: 'Europe/Berlin',
          //timezoneOffset: 3600
        },
        credits: {
          enabled: false
        },
        title: {
          text: this.formatTitle(this.targetDate)
        },
        yAxis: {
          title: '',
          min: 0,
          max: 100

        },
        chart: {
          zoomType: "",
          renderTo: "bb-chart",
          events: {
            render: function() {
              const chart = this;
              console.log("rendered!");
              //vm.renderActivities(chart);
            },
            load: function() {
              console.log("loaded!");
              //vm.renderActivities(this);
            },
          }
        },
        plotOptions: {
          series: {
            animation: false,
            dragDrop: {
              draggableX: false,
              draggableY: true,
              dragMinY: 0,
              dragMaxY: 100,
              dragPrecisionY: 1,
              states: {
                inactive: {
                  opacity: 1
                }
              }
            },
            point: {
              events: {
                redraw: function() {
                  console.log("redraw!")
                },
                render: ({point}) => {
                  this.renderActivities(point);
                },
                click: ({point}) => {
                  this.onClickPoint(point);
                },
                drag: function(e) {
                  // only allow interactions with reference series
                  if ((e.target.series.index === 0)) {
                    return false;
                  }
                },
                drop: function(e) {
                  // only allow interactions with reference series
                  if ((e.target.series.index === 0)) {
                    return false;
                  }
                  vm.onLabelSeries(e.target.category, e.newPoint.y)
                },
              }
            }
              //pointInterval: 3
          },
          line: {
            cursor: 'native'
          }
        },
        responsive: true,
        maintainAspectRatio: false,
        xAxis: {
          //offset: 23.5,
          categories: this.targetBodyBatteryData.map(d => d.timestamp * 1000),
          type: 'datetime',
          tickWidth: 1,
          labels: {
            formatter: function(p) {
              return Highcharts.dateFormat('%H:%M', p.value)
            }
          }
        },
        tooltip: {
          xDateFormat: '%Y-%m-%d %H:%M',
          shared: true,
          borderWidth: 0,
          shadow: false,
          style: {
            fontSize: "18px",
          },
          backgroundColor: "rgba(255,255,255,0)",
          formatter: function() {
            return this.y;
          },
          positioner: function () {
            return {
              // right aligned
              x: this.chart.chartWidth - this.label.width,
              y: 0 // align to title
            };
          },
        },
        series: [{
          name: 'Reference',
          data: this.comparisonBodyBatteryData.map(d => d.value),
          color: "#8E8E8E",
          enableMouseTracking: false,
          showInLegend: this.comparisonBodyBatteryData.length > 0,
          marker: {
            radius: 0.1,
            symbol: 'circle',
            states: {
              hover: {
                enabled: true,
                radius: 4
              },
              select: {
                enabled: false,
                radius: 5
              }
            }
          }
        },
          {
            name: 'Suggestion',
            data: this.targetBodyBatteryData.map(d => d.value),
            showInLegend: true,
            marker: {
              radius: 0.1,
              symbol: 'circle',
              states: {
                hover: {
                  enabled: true,
                  radius: 4
                },
                select: {
                  enabled: true,
                  radius: 5
                }
              }
            }
          }]
      };
    }
  },
  watch: {
    data: function(newData) {
      this.chartOptions.series[1].data = newData.map(d => d.value);
      this.chartOptions.xAxis.categories = newData.map(d => d.timestamp);
    },
    targetDate: function(newDate) {
      this.chartOptions.title.text = this.formatTitle(newDate);
    }
  },
  methods: {
    formatTitle(date) {
      return 'Energylevel on ' + date.toLocaleDateString();
    },
    onClickPoint(point) {
      // only allow interactions with target series
      if ((point.series.index === 0)) {
        return
      }
      // set clicked point to selected
      point.select(true, true)

      const prevSelectedPoints = this.selectedPoints;

      // check if selected point not within same series then unselect
      // on chart and remove from selected array
      if (
        prevSelectedPoints.length > 0 &&
        point.series.index !==
        prevSelectedPoints[prevSelectedPoints.length - 1].series_index
      ) {
        prevSelectedPoints.forEach((p, i) => {
          if (point.series.index !== p.series_index) {
            point.series.chart.series[p.series_index].points[p.index].select(false, true)
          }
        })
        // empty the selected array
        //selectedPoints.length = 0;
        this.selectedPoints = []
      }
      // add to array of selected points
      let p = {index: point.index, x: point.x, y: point.y, series_index: point.series.index}
      this.selectedPoints.push(p)
      // keep maximum selected points to 2, remove the first point
      // added and set select to false if selected points is > 2
      if (this.selectedPoints.length > 2) {
        point.series.data[this.selectedPoints[0].index].select(false, true)
        this.selectedPoints.shift()
      }
      //ref.activityStore.setSelectedPoints(selectedPoints)
    },
    renderActivities: function(chart) {

      if (!chart) {
        return;
      }
      // remove existing svgs
      if (chart.activitySvgs) {
        chart.activitySvgs.forEach(svg => svg.destroy());
      }
      chart.activitySvgs = [];
      this.renderActivityForSeries(chart, this.targetActivities, this.targetBodyBatteryData, "black");
      this.renderActivityForSeries(chart, this.comparisonActivities,this.targetBodyBatteryData, "blue");
    },
    renderActivityForSeries(chart, activities, bodyBatteryData, fillColor) {
      const runSvg = this.runPath;
      const instance = this;

      Object.keys(activities).forEach(function(idx) {
        // TODO: Fix position
        // draw SVG
        const activity = activities[idx];
        let xIdx = 0;
        Object.keys(bodyBatteryData).forEach(function(idx) {
          if(bodyBatteryData[idx].timestamp <= (activity.startTimeOffsetInSeconds)) {
            xIdx = idx;
          }
        })
        const yPos = chart.yAxis[0].toPixels(0);
        const xPos = chart.series[1].data[xIdx].plotX;
        const activitySvg = chart.renderer
          .path([runSvg])
          .attr({
            width: '3',
            height: '10',
            fill: fillColor,
            transform: 'translate(' + (xPos) + ',' + (yPos) + ')',
          })
          .on("click", function(e) {
            instance.$emit("selectActivity", activity);
          })
          .add()
        chart.activitySvgs.push(activitySvg)
      });
    },
    onLabelSeries(x, y) {
      console.log("onLabelSeries", this);
      const instance = this;
      instance.$emit("labelSeries", x, y);
      /*
    // keeps track of the new labels and updates the chart series
      const unixTimestamp = x / 1000
      let newData = this.labelledData;
      Object.keys(newData).forEach(function(idx) {
        if (newData[idx].timestamp === unixTimestamp) {
          newData[idx].value = y
        }
      })
      // HC requires data to be sorted
      //this.chartOptions.series[0] = this.labelledData.sort(d => d.timestamp);
      this.chart.series[0].setData(this.labelledData.sort(d => d.timestamp), false)

     */
    },
    onToggleSelectedPoints: function () {
      // toggle selected points during labelMode
      Object.keys(this.selectedPoints).forEach(function (idx) {
        let point = this.chartOptions.series[1].data[this.selectedPoints[idx].index];
        if (point) {
          point.select(!this.labelMode, true)
        }
      });
    }
  }
};
</script>
