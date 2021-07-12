import Vue from 'vue'
import axios from 'axios'
// import AxiosPlugin from 'vue-axios-cors'

Vue.prototype.$http = axios
axios.defaults.baseURL = 'localhost:8000/search/'

export default {
  async getData () {
    try {
        const response = await axios.get()
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