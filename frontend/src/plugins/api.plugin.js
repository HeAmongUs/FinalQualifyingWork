import api from "@/api"
import instance from "@/api/instance"
import errorMessages from "@/plugins/errorMessages"
import messages from "@/plugins/messages"

export default {
  install: (app) => {
    app.config.globalProperties.$api = api

    instance.interceptors.request.use(
      (config) => {
        config.headers = {
          Authorization: `${localStorage.getItem("accessToken")}`,
        }
        return config
      },
      (error) => {
        console.log(error)
      }
    )
    instance.interceptors.response.use(
      (config) => {
        return config
      },
      async (error) => {
        if (error.response.status === 401) {
          console.log(error.response)
          if (
            error.response.data.message === "token is expired" &&
            !error.response.request.responseURL.includes("refresh")
          ) {
            const resp = await instance.post("api/v1/accounts/refresh")
            if (resp.status === 200) {
              app.config.globalProperties.$message(
                messages["accessTokenUpdate"]
              )
              if (resp.data.access_token) {
                localStorage.accessToken = resp.data.access_token
              }
              return instance.request(error.config)
            } else {
              await app.config.globalProperties.$router.push({ name: "Login" })
              app.config.globalProperties.$message(errorMessages["handler401"])
            }
          }
        } else {
          console.log(error)
          app.config.globalProperties.$message(errorMessages["unhandled"])
        }
      }
    )
  },
}
