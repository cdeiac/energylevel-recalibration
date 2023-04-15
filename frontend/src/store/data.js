// Utilities
import { defineStore } from 'pinia'

export const useDataStore = defineStore('data', {
  state: () => {
    return {
      bodyBattery: [],
      bodyBatteryLabels: [],
      steps: [],
      stress: [],
      respiration: [],
      sleep: [],
      activities: [],
      selectedActivity: null
    }
  },
  getters: {
    selectedActivity(state) {
      return state.selectedActivity;
    }
  },
  // could also be defined as
  // state: () => ({ count: 0 })
  actions: {
    filterBodyBattery(date) {
      this.bodyBattery.map(b => b.calendarDate === new Date().toISOString().slice(0, 10))
    },
    setSelectedActivity(activity) {
      this.selectedActivity = activity;
    },
    setBodyBatteryData(data) {
      this.bodyBattery = data;
    },
    setActivityData(data) {
      this.bodyBattery = data;
    }
  },
})
