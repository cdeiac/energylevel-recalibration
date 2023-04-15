import {
  getAllActivities,
  getAllBodyBattery,
  getAllRespiration,
  getAllSleep, getAllSteps,
  getAllStress
} from '@/api/api'


export async function getAllData(userId) {

  const bodyBatteryData = await getAllBodyBattery(userId);
  const stressData = await getAllStress(userId);
  const respirationData = await getAllRespiration(userId);
  const sleepData = await getAllSleep(userId);
  const activityData = await getAllActivities(userId);
  const stepsData = await getAllSteps(userId);

  return new HealthData(bodyBatteryData, stressData, respirationData, sleepData, activityData, stepsData)
}


export class HealthData {
  constructor(bodyBattery, stress, respiration, sleep, activities, steps) {
    this.bodyBattery = bodyBattery;
    this.stress = stress;
    this.sleep = sleep;
    this.activities = activities;
    this.steps = steps;
    this.respiration = respiration
  }
}
