import axios from "axios"
import appConfig from "../app.config"

const instance = axios.create({
  baseURL: appConfig.server.baseURL,
  withCredentials: true,
  headers: {
    accept: "application/json",
  },
})

export default instance
