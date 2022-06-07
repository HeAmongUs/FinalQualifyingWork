<template>
  <div class="login">
    <h4 class="title">{{ formTitle }}</h4>
    <form @submit.prevent="submitHandler" class="login-form">
      <template v-if="!isConfirmed">
        <username-input
          v-model:username="username"
          v-model:isValidUsername="isValidUsername"
        />
        <password-input
          v-model:password="password"
          v-model:isValidPassword="isValidPassword"
        />
      </template>
      <template v-else>
        <OTPInput v-model:OTP="OTP" v-model:isValidOTP="isValidOTP" />
      </template>
      <button
        :disabled="isDisabled"
        class="btn waves-effect waves-light cyan lighten-1"
        type="submit"
      >
        Send
        <i class="material-icons right">send</i>
      </button>
    </form>
  </div>
</template>

<script>
import PasswordInput from "./PasswordInput"
import OTPInput from "./OTPInput"
import UsernameInput from "./UsernameInput"
import messages from "@/plugins/messages"

export default {
  name: "LoginForm",
  components: { UsernameInput, OTPInput, PasswordInput },
  mounted() {
    window.M.updateTextFields()
  },
  data() {
    return {
      username: "",
      isValidUsername: false,
      password: "",
      isValidPassword: false,
      OTP: null,
      isValidOTP: false,
      isConfirmed: false,
    }
  },
  computed: {
    formTitle() {
      return this.isConfirmed ? "Enter code" : "Sign-in"
    },
    isDisabled() {
      if (!this.isConfirmed) {
        if (this.isValidPassword && this.isValidUsername) {
          return false
        }
      } else if (this.isConfirmed) {
        if (this.isValidOTP && this.isValidPassword && this.isValidUsername) {
          return false
        }
      }
      return true
    },
  },
  methods: {
    async submitHandler() {
      const user = {
        username: this.username,
        password: this.password,
      }
      if (this.isConfirmed) {
        user.OTPNumber = this.OTP
      }
      const response = await this.$api.auth.login(user)
      if (response.status === 200) {
        if (this.isConfirmed) {
          localStorage.setItem("accessToken", response.data.access_token)
          localStorage.setItem("refreshToken", response.data.refresh_token)
          await this.$router.push({ name: "Chats" })
          this.$message(messages["loginSuccess"])
        } else {
          this.isConfirmed = true
        }
      }
    },
  },
}
</script>

<style lang="scss">
.login {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 30px 40px;
  border-radius: 10px;
  background: #fff;

  .input {
    margin-bottom: 10px;
    font-size: 16px;
    outline: none;
    transition: 0.3s;
    border: 1px #2c3e50 solid;
    &:hover {
      background: #eee;
    }
  }

  .title {
    padding: 0;
    margin: 0 0 10px 0;
  }

  &-form {
    min-width: 200px;
    display: flex;
    flex-direction: column;
    max-width: 250px;
  }
}
</style>
