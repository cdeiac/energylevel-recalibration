<template>
  <v-app id='app'>
    <AppBar />
    <v-main>
      <v-container fluid> <!-- class="fill-height"-->
        <v-row >

          <v-col
            cols="12"
            sm="9"
            lg="9"
          >
            <v-sheet
              rounded="lg"
              border
            >
              <v-btn class="ma-2" color="primary" @click="search">
                Search
              </v-btn>
              <v-btn class="mx-2" color="error" @click="resetLabels">
                Reset
              </v-btn>
              <v-btn class="mx-2" color="secondary" @click="search">
                Confirm Label
              </v-btn>
              <BodyBattery
                v-if="targetBodyBatteryData.length > 0"
                ref="bb-chart"
                @select-activity="selectActivity"
                @label-series="labelData"
                :target-body-battery-data="targetBodyBatteryData"
                :comparison-body-battery-data="comparisonBodyBatteryData"
                :target-date="targetDate"
                :comparison-date="comparisonDate"
                :target-activities="targetActivityData"
                :comparison-activities="comparisonActivityData"
              />
            </v-sheet>
          </v-col>
          <v-col style="height: 100px">
            <v-sheet
              rounded="lg"
              border
            >
              <Activity
                v-if="targetBodyBatteryData.length > 0"
                ref="activity-chart"
                :target-activity="targetActivity"
                :comparison-activity="comparisonActivity"
                :activities="healthData.activities"
              />
            </v-sheet>
          </v-col>
        </v-row>
        <v-row>
          <v-col
            cols="12"
            sm="9"
            lg="9">

            <v-sheet
              rounded="lg"
              border
            >
              <EventChart
                v-if="targetActivityData.length > 0"
                ref="event-chart"
                @select-activity="selectActivity"
                :target-activities="targetActivityData"
                :comparison-activities="comparisonActivityData"
                :target-sleeps="targetSleeps"
                :comparison-sleeps="comparisonSleeps"
              />
            </v-sheet>

          </v-col>
          <v-col style="height: 100px">
            <v-sheet
              rounded="lg"
              border
            >
              <SleepChart
                v-if="targetSleep.durationInSeconds"
                ref="sleep-chart"
                :target-sleep="targetSleep"
                :comparison-sleep="comparisonSleep"
              />
            </v-sheet>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>

import BodyBattery from "@/components/BodyBattery";
import {onBeforeMount, ref} from "vue";
import * as apiService from "@/services/api";
import Activity from "@/components/Activity";
import {saveBodyBatteryLabels} from "@/api/api";
import EventChart from "@/components/EventChart";
import SleepChart from "@/components/SleepChart";
import AppBar from "@/layouts/default/AppBar";

const userId = '33be367f-79e7-4c05-b39f-54b1d2ab3a60' // hardcoded for now
const targetBodyBatteryData = ref([]);
const comparisonBodyBatteryData = ref([]);
const healthData = ref({});
const stressData = ref([]);
const stepsData = ref([]);
const respData = ref([]);
const activityData = ref([]);
const targetActivityData = ref({});
const comparisonActivityData = ref({});
const targetDate = ref(new Date("2023-03-21"));
const comparisonDate = ref();
const suggestedDates = ["2023-03-19", "2023-03-20", "2023-03-21"]
const targetActivity = ref([]);
const comparisonActivity = ref([]);
const targetSleep = ref({});
const comparisonSleep = ref({});
const labelledData = ref([]);

onBeforeMount(() => { getAllData() });

async function getAllData() {
  const newHealthData = await apiService.getAllData(userId)
  healthData.value = newHealthData;

  if (newHealthData) {
    activityData.value = newHealthData.activities;
    targetActivityData.value = newHealthData.activities
      .filter(entry =>
        new Date(entry.startTimeOffsetInSeconds * 1000).toLocaleDateString() === new Date(targetDate.value).toLocaleDateString())
    targetBodyBatteryData.value = newHealthData.bodyBattery
      .filter(entry =>
        new Date(entry.timestamp * 1000).toLocaleDateString() === new Date(targetDate.value).toLocaleDateString())
    stressData.value = newHealthData.stress
    // sleeps
    const wakeupTime = newHealthData.sleep
      .filter(entry =>
        new Date((entry.startTimeOffsetInSeconds + entry.durationInSeconds) * 1000).toLocaleDateString() === new Date(targetDate.value).toLocaleDateString())
    targetSleep.value = {...wakeupTime[0]};
  }
}
function search(e) {
  // TODO: Save labelled data
  //saveBodyBatteryLabels(userId, labelledData);
  // currently picks a random suggestion
  let random = suggestedDates[Math.floor(Math.random()*suggestedDates.length)];
  targetDate.value = new Date(random);
  const currentHealthData = healthData.value;

  // target becomes comparison, suggestion is new target
  comparisonBodyBatteryData.value = targetBodyBatteryData.value;
  comparisonActivityData.value = targetActivityData.value;
  comparisonSleep.value = targetSleep.value

  targetBodyBatteryData.value = currentHealthData.bodyBattery
    .filter(entry => new Date(entry.timestamp * 1000).toDateString() === new Date(targetDate.value).toDateString())
  targetActivityData.value = currentHealthData.activities
    .filter(entry => new Date(entry.startTimeOffsetInSeconds * 1000).toDateString() === new Date(targetDate.value).toDateString());
  // gather all sleep entries (wake up and bedtime)
  const wakeupTime = currentHealthData.sleep
    .filter(entry =>
      new Date((entry.startTimeOffsetInSeconds + entry.durationInSeconds) * 1000).toLocaleDateString() === new Date(targetDate.value).toLocaleDateString())
  targetSleep.value = {...wakeupTime[0]};
}

function selectActivity(activity) {
  console.log("activity was passed to parent", activity);

  if (!targetActivity.value.activityName) {
    targetActivity.value = activity;
  }
  else if(!comparisonActivity.value.activityName) {
    comparisonActivity.value = activity;
  }
  else {
    targetActivity.value = comparisonActivity.value;
    comparisonActivity.value = activity;
  }
  console.log("selectedActivity", targetActivity.value, comparisonActivity.value);
}

function resetLabels() {
  // reset current date's data
  targetBodyBatteryData.value = healthData.value.bodyBattery
    .filter(entry => new Date(entry.timestamp * 1000).toDateString() === new Date(targetDate.value).toDateString())
  activityData.value = healthData.value.activities
    .filter(entry => new Date(entry.startTimeOffsetInSeconds * 1000).toDateString() === new Date(targetDate.value).toDateString());
}

function labelData(x, y) {
  console.log("Labelled data", x, y);
  labelledData.value.push({timestamp: x/1000, value: y})
  saveBodyBatteryLabels(userId, labelledData)

  // TODO: update local data to save roundtrip

}
</script>
