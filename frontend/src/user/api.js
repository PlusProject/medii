import Vue from 'vue'
import axios from 'axios'

Vue.prototype.$http = axios
axios.defaults.baseURL = 'http://ec2-52-79-52-192.ap-northeast-2.compute.amazonaws.com:8000/search/'

export default {
  async search (params) {
    try {
        const response = await axios.get('', {
          params: {
            'doctor_name': params.name_kor,
            'hospital': params.belong,
            'disease': params.disease,
            'major': params.major,
            'rare': params.rare
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
  },
  async getCrisCoworker (id) {
    try {
      const response = await axios.get('coworker_cris', {
        params: {
          pid: id
        }
      })
      return response
    } catch (error) {
      console.error(error)
    }
  },
  async getDiseaseList () {
    try {
      const response = await axios.get('disease')
      return response
    } catch (error) {
      console.error(error)
    }
  },
  async getRareDiseaseList () {
    try {
      const response = await axios.get('rare_disease')
      return response
    } catch (error) {
      console.error(error)
    }
  },
  async searchClinicalTrials (params) {
    try {
      const response = await axios.get('searchClinicalTrials', {
        params: {
          'disease': params.disease,
          'rare': params.rare
        }
      })
      console.log(response)
      return response
    } catch (error) {
      console.error(error)
    }
  },
  async getDiseaseMatch(params) {
    try {
        const response = await axios.get('diseasematch', {
          params: {
            'input': params.input,
          }
        })
        console.log(response)
        return response
    } catch (error) {
        console.error(error)
    }
  },
  async recommend (params) {
    try {
        const response = await axios.get('recommend', {
          params: {
            'input': params.input,
          }
        })
        console.log(response)
        return response
    } catch (error) {
        console.error(error)
    }
  },
  async recommend2 (params) {
    try {
        const response = await axios.get('recommend2', {
          params: {
            'input': params.input,
          }
        })
        console.log(response)
        return response
    } catch (error) {
        console.error(error)
    }
  },
  async getCount(params) {
    try {
        const response = await axios.get('count', {
          params: {
            'input': params.input,
          }
        })
        console.log(response)
        return response
    } catch (error) {
        console.error(error)
    }
  },
  async getExtractDisease(params){
    try {
        const response = await axios.get('extractdisease', {
          params: {
            'summary': params.input,
          }
        })
        console.log(response)
        return response
    } catch (error) {
        console.error(error)
    }
  }, 
}
