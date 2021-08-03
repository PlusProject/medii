import Vue from 'vue'
import axios from 'axios'
// import AxiosPlugin from 'vue-axios-cors'

Vue.prototype.$http = axios
axios.defaults.baseURL = 'http://127.0.0.1:8000/api/search/'// 'http://ec2-52-79-52-192.ap-northeast-2.compute.amazonaws.com:8000/search/'

export default {
  async search (name, hospital, disease, major) {
    try {
        const response = await axios.get('', {
          params: {
            'doctor_name': name,
            'hospital': hospital,
            'disease': disease,
            'major': major
          }
        })
        // console.log(response)
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
        // console.log(response)
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
        // console.log(response)
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
  }

  // async getByHospital (hospital) {
  //   try {
  //       const response = await axios.get('hospital', {
  //         params: {
  //           'hospital' : hospital
  //         }
  //       })
  //       console.log(response)
  //       return response
  //   } catch (error) {
  //       console.error(error)
  //   }
  // }
}

// async function server_request (url, method, options) {
//   if (options !== undefined) {
//     var { params = {}, data = {} } = options
//   } else {
//       params = data = {}
//   }
//   return
// }
