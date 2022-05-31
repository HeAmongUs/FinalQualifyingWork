export default {
  server: {
    baseURL: "http://192.168.43.108:8000/",
  },
  auth: {
    usernameMinLength: 6,
    usernameMaxLength: 20,
    passwordMinLength: 6,
    passwordIncludesLowercase: true,
    passwordIncludesUppercase: true,
    passwordIncludesDigits: true,
    passwordIncludesSpecialSymbols: true,
    OTPMinValue: 100000,
    OTPMaxValue: 999999,
  },
}
