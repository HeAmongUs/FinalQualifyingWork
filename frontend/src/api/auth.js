export default function (instance) {
  return {
    login(payload) {
      return instance.post("api/v1/accounts/login", payload)
    },
    logout() {
      return instance.delete("api/v1/accounts/logout")
    },
    refreshToken() {
      return instance.post("api/v1/accounts/refresh")
    },
  }
}
