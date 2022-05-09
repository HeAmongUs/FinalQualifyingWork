<template>
  <div class="input-field s6">
    <input
      v-model.trim="v$.lazyOTP.$model"
      id="otp"
      type="number"
      :class="{ invalid: v$.$invalid && v$.$dirty }"
    />
    <label for="otp">Verify code</label>
    <small
      v-if="v$.lazyOTP.$dirty && v$.lazyOTP.required.$invalid"
      class="helper-text invalid"
    >
      Введите код
    </small>
    <small
      v-else-if="v$.lazyOTP.$dirty && v$.lazyOTP.$invalid"
      class="helper-text invalid"
    >
      Введите корректный код</small
    >
  </div>
</template>

<script>
import { between, required } from "@vuelidate/validators"
import appConfig from "../../app.config"
import useVuelidate from "@vuelidate/core"

export default {
  name: "OTPInput",
  setup() {
    return { v$: useVuelidate() }
  },
  emits: ["update:OTP", "update:isValidOTP"],
  props: {
    OTP: {
      type: Number,
    },
  },
  data() {
    return {
      lazyOTP: this.OTP,
    }
  },
  validations() {
    return {
      lazyOTP: {
        required,
        between: between(
          appConfig.auth.OTPMinValue,
          appConfig.auth.OTPMaxValue
        ),
      },
    }
  },
  watch: {
    lazyOTP() {
      this.$emit("update:OTP", Number(this.lazyOTP))
      this.$emit("update:isValidOTP", !this.v$.$invalid)
    },
  },
}
</script>
<style scoped>
input[type="number"]::-webkit-outer-spin-button,
input[type="number"]::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
input[type="number"] {
  -moz-appearance: textfield;
}
</style>
