<template>
  <div class="chats">
    <h3>Chats page</h3>
  </div>
</template>

<script>
import io from "socket.io-client"
import appConfig from "../app.config"
export default {
  name: "Chats",
  data() {
    return {
      io: null,
    }
  },
  async created() {
    const accessToken = await this.$store.getters.accessToken
    this.io = await io(`${appConfig.server.baseURL}`, {
      extraHeaders: {
        access_token: accessToken,
      },
    })
    this.io.on("event", (socket) => {
      this.io.emit("event", socket)
      console.log("EVENT", socket)
    })
    this.io.on("connect", () => {
      console.log("CONNECT")
    })
  },
}
</script>

<style scoped></style>
