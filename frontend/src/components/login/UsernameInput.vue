<template>
  <div class="input-field s6">
    <input
      v-model.trim="v$.lazyUsername.$model"
      id="username"
      type="text"
      :class="{ invalid: v$.$invalid && v$.$dirty }"
    />
    <label for="username">Username</label>
    <small
      v-if="v$.lazyUsername.$dirty && v$.lazyUsername.required.$invalid"
      class="helper-text invalid"
    >
      Введите Username
    </small>
    <small
      v-else-if="v$.lazyUsername.$dirty && v$.lazyUsername.$invalid"
      class="helper-text invalid"
    >
      Введите корректный Username</small
    >
  </div>
</template>

<script>
import { maxLength, minLength, required } from "@vuelidate/validators"
import appConfig from "../../app.config"
import useVuelidate from "@vuelidate/core"

export default {
  name: "UsernameInput",
  setup() {
    return { v$: useVuelidate() }
  },
  emits: ["update:username", "update:isValidUsername"],
  props: {
    username: {
      type: String,
    },
  },
  data() {
    return {
      lazyUsername: this.username,
    }
  },
  validations() {
    return {
      lazyUsername: {
        required,
        minLength: minLength(appConfig.auth.usernameMinLength),
        maxLength: maxLength(appConfig.auth.usernameMaxLength),
      },
    }
  },
  watch: {
    lazyUsername() {
      this.$emit("update:username", this.lazyUsername)
      this.$emit("update:isValidUsername", !this.v$.$invalid)
    },
  },
}
</script>

<style scoped>

</style>
