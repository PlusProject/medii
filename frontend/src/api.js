import Vue from 'vue'
import axios from 'axios'
// import AxiosPlugin from 'vue-axios-cors'

Vue.prototype.$http = axios
axios.defaults.baseURL = 'http://127.0.0.1:8000/search/'// 'http://ec2-52-79-52-192.ap-northeast-2.compute.amazonaws.com:8000/search/'

export default {
  async getByNameAndHospital (name, hospital) {
    try {
        const response = await axios.get('name', {
          params: {
            'doctor_name': name,
            'hospital': hospital
          }
        })
        console.log(response)
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