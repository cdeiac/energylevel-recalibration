import http from './common'

export async function getAllBodyBattery(userId) {

  return await http.get('/api/bodyBattery/all', {
    params: {userId: userId}
  }).then(
    (response) => {
    return response.data
  },
  (error) => {
    console.error(error);
    throw error;
  })
}

export async function getAllStress(userId) {

  return await http.get('/api/stressLevel/all', {
    params: {userId: userId}
  }).then(
    (response) => {
      return response.data
    },
    (error) => {
      console.error(error);
      throw error;
    })
}

export async function getAllSteps(userId) {

  return await http.get('/api/steps/all', {
    params: {userId: userId}
  }).then(
    (response) => {
      return response.data
    },
    (error) => {
      console.error(error);
      throw error;
    })
}

export async function getAllRespiration(userId) {

  return await http.get('/api/respiration/all', {
    params: {userId: userId}
  }).then(
    (response) => {
      return response.data
    },
    (error) => {
      console.error(error);
      throw error;
    })
}

export async function getAllSleep(userId) {

  return await http.get('/api/sleep/statistics/all', {
    params: {userId: userId}
  }).then(
    (response) => {
      return response.data
    },
    (error) => {
      console.error(error);
      throw error;
    })
}

export async function getAllActivities(userId) {

  return await http.get('/api/activities/all', {
    params: {userId: userId}
  }).then(
    (response) => {
      return response.data
    },
    (error) => {
      console.error(error);
      throw error;
    })
}

export async function saveBodyBatteryLabels(userId, labels) {

  return await http
    .post('/api/bodyBattery/label', {  params: {userId: userId}, labels})
    .then((response) => {
      return response.data},
      (error) => {
        console.error(error);
        throw error;
      })
}
