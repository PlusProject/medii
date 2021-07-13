import Vue from 'vue'
import axios from 'axios'
// import AxiosPlugin from 'vue-axios-cors'

Vue.prototype.$http = axios
axios.defaults.baseURL = 'http://127.0.0.1:8000/search/'// 'http://ec2-52-79-52-192.ap-northeast-2.compute.amazonaws.com:8000/search/'

export default {
  async getData () {
    try {
        const response = await axios.get('name', {
          params: {
            doctor_name : '이해영'
          }
        })
        console.log(response)
        return response
    } catch (error) {
        console.error(error)
    }
  }
}

// async function server_request (url, method, options) {
//   if (options !== undefined) {
//     var { params = {}, data = {} } = options
//   } else {
//       params = data = {}
//   }
//   return
// }