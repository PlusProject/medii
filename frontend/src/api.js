import Vue from 'vue'
import axios from 'axios'
// import AxiosPlugin from 'vue-axios-cors'

Vue.prototype.$http = axios
axios.defaults.baseURL = 'http://ec2-13-125-48-73.ap-northeast-2.compute.amazonaws.com:8080/users'

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