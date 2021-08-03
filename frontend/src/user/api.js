import Vue from 'vue'
import axios from 'axios'

Vue.prototype.$http = axios
axios.defaults.baseURL = 'http://127.0.0.1:8000/api/search/'// 'http://ec2-52-79-52-192.ap-northeast-2.compute.amazonaws.com:8000/search/'

export default {
  async search (params) {
    try {
        const response = await axios.get('', {
          params: {
            'doctor_name': params.name_kor,
            'hospital': params.belong,
            'disease': params.disease,
            'major': params.major
          }
        })
        console.log(response)
        return response
    } catch (error) {
        console.error(error)
    }
  },
  async getClinicalTrials (pid) {
    try {
        const response = await axios.get('clinicaltrials', {
          params: {
            'pid': pid
          }
        })
        console.log(response)
        return response
    } catch (error) {
        console.error(error)
    }
  },
  async getThesis (pid) {
    try {
        const response = await axios.get('thesis', {
          params: {
            'pid': pid
          }
        })
        console.log(response)
        return response
    } catch (error) {
        console.error(error)
    }
  },
  async getDoctorList () {
    try {
      const response = await axios.get('name')
      return response
    } catch (error) {
      console.error(error)
    }
  },
  async getHospitalList () {
    try {
      const response = await axios.get('hospital')
      return response
    } catch (error) {
      console.error(error)
    }
  },
  async getCoworker (id) {
    try {
      const response = await axios.get('coworker', {
        params: {
          pid: id
        }
      })
      return response
    } catch (error) {
      console.error(error)
    }
  }
}
