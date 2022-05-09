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
  setup() {
    return {
      io$: io(`${appConfig.server.baseURL}`, {
        extraHeaders: {
          access_token: "mytoken",
        },
      }),
    }
  },
  async mounted() {
    this.io$.on("event", (socket) => {
      this.io$.emit("event", socket)
      console.log("EVENT", socket)
    })
    this.io$.on("connect", () => {
      console.log("CONNECT")
    })
  },
}
</script>

<style scoped></style>
