<template>
  <div class="input-field s6">
    <input
      v-model.trim="v$.lazyPassword.$model"
      id="password"
      type="password"
      :class="{ invalid: v$.$invalid && v$.$dirty }"
    />
    <label for="password">Пароль</label>
    <small
      v-if="v$.lazyPassword.$dirty && v$.lazyPassword.required.$invalid"
      class="helper-text invalid"
    >
      Введите пароль
    </small>
    <small
      v-else-if="v$.lazyPassword.$dirty && v$.lazyPassword.$invalid"
      class="helper-text invalid"
    >
      Введите корректный пароль</small
    >
  </div>
</template>
<script>
import { minLength, required } from "@vuelidate/validators"
import appConfig from "../../app.config"
import useVuelidate from "@vuelidate/core"
export default {
  name: "PasswordInput",
  setup() {
    return { v$: useVuelidate() }
  },
  emits: ["update:password", "update:isValidPassword"],
  props: {
    password: {
      type: String,
    },
  },
  data() {
    return {
      lazyPassword: this.password,
    }
  },
  validations() {
    return {
      lazyPassword: {
        required,
        minLength: minLength(appConfig.auth.passwordMinLength),
      },
    }
  },
  watch: {
    lazyPassword() {
      this.$emit("update:password", this.lazyPassword)
      this.$emit("update:isValidPassword", !this.v$.$invalid)
    },
  },
}
</script>

<style scoped></style>
