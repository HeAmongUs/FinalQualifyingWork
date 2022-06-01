<template>
  <div class="messenger">
    <div class="sidebar" v-if="!split || !selectedChatId">
      <header class="header">
        <div class="header-username">
          <my-dropdown>
            <template v-slot:target>
              <div class="color-blue-hover">
                {{ username }}
              </div>
            </template>
            <template v-slot:content>
              <ul>
                <li @click="logout">
                  <span class="button color-blue">
                    <i class="material-icons left color-blue"
                      >assignment_return</i
                    >
                    Logout
                  </span>
                </li>
              </ul>
            </template>
          </my-dropdown>
        </div>
        <div class="header-datetime">
          <div class="header__datetime">{{ filteredDate }}</div>
        </div>
      </header>

      <div class="sidebar-content">
        <chat-list
          :chats="chats"
          v-model="selectedChatId"
          :selected="selectedChatId"
          v-model:search-input="searchInput"
        />
      </div>
    </div>
    <div class="chat" v-if="!split || selectedChatId">
      <header class="header">
        <div class="header-back" @click="selectedChatId = null" v-if="split">
          <i class="material-icons left color-blue-hover">assignment_return</i>
        </div>
        <div class="flex-justify-start">
          <div v-if="selectedChatId">
            {{ chats.find((c) => c.id === selectedChatId).title }}
          </div>
        </div>
      </header>

      <div class="chat-content">
        <message-list :messages="messages" v-if="messages" />
        <message-input
          @sendMessage="(messageText) => handlerSendMessage(messageText)"
        />
      </div>
    </div>
  </div>
</template>

<script>
import ChatList from "./ChatList"
import MessageList from "./MessageList"
import MessageInput from "./MessageInput"
import io from "socket.io-client"
import appConfig from "../../app.config"
import MyDropdown from "../UI/MyDropdown"
import messages from "@/plugins/messages"
export default {
  name: "Messenger",
  // eslint-disable-next-line vue/no-unused-components
  components: { MyDropdown, MessageInput, MessageList, ChatList },
  data() {
    return {
      io: null,
      chats: null,
      userChats: null,
      searchedChats: null,
      selectedChatId: null,
      messages: null,
      date: new Date(),
      searchInput: null,
      width: 0,
    }
  },
  mounted() {
    this.interval = setInterval(() => {
      this.date = new Date()
    }, 1000)
    window.M.updateTextFields()
  },
  beforeUnmount() {
    clearInterval(this.interval)
    window.removeEventListener("resize", this.onResize)
  },
  async created() {
    window.addEventListener("resize", this.onResize)
    this.onResize()

    this.userChats = (await this.$api.chat.getChats()).data
    this.chats = this.userChats

    const accessToken = await this.$store.getters.accessToken
    this.io = await io(`${appConfig.server.baseURL}`, {
      extraHeaders: {
        Authorization: accessToken,
      },
    })

    this.io.on("display new message", (message) => {
      if (this.selectedChatId === message.chatId) {
        this.messages.push(message)
      }
    })

    this.io.on("event", (msg) => {
      this.io.emit("event", msg)
      console.log("EVENT", msg)
    })
    this.io.on("connect", () => {
      console.log("CONNECT")
    })
  },
  methods: {
    async handlerSendMessage(messageText) {
      this.io.emit("send message", {
        chatId: this.selectedChatId,
        messageText: messageText,
      })
      // await this.$api.chat.sendMessage(this.selectedChatId, {
      //   messageText: messageText,
      // })
    },
    onResize() {
      this.width = window.innerWidth
    },
    async logout() {
      try {
        await this.$api.auth.logout()
        this.$store.commit("clearUserInfo")
        await this.$router.push({ name: "Login" })
        this.$message(messages["logout"])
      } catch (e) {
        console.log(e)
      }
    },
  },
  watch: {
    async selectedChatId() {
      if (this.selectedChatId) {
        this.messages = (
          await this.$api.chat.getChatMessages(this.selectedChatId)
        ).data
      }
    },
    async searchInput() {
      this.selectedChatId = null
      this.messages = null
      if (this.searchInput) {
        this.searchedChats = (
          await this.$api.chat.getSearchedChats(this.searchInput)
        ).data
        if (this.searchedChats) {
          this.chats = this.searchedChats
        }
      } else {
        this.chats = this.userChats
      }
    },
  },
  computed: {
    username() {
      return this.$store.getters.userInfo.username || null
    },
    split() {
      return this.width <= 576
    },
    filteredDate() {
      const options = {
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
      }
      return Intl.DateTimeFormat("ru-RU", options).format(new Date(this.date))
    },
  },
}
</script>

<style scoped lang="scss">
@import "../../assets/messenger.colors";

.header {
  height: 50px;
  padding: 10px 15px;
  display: flex;
  justify-content: space-between;
  background: $header-bg;
  border-right: 5px solid $border-list;
  font-size: 14px;
  font-weight: bold;

  &-username {
    cursor: pointer;
    font-weight: bold;
    transition: 0.2s;
  }
  &-datetime {
  }
  &__datetime {
  }

  &-back {
    cursor: pointer;
  }
}

.messenger {
  color: $white;
  position: relative;
  display: flex;
  max-width: 1600px;
  min-height: 100vh;
  max-height: 100vh;
  font-size: 12px;
  margin: 0 auto;

  .sidebar {
    width: 576px;
    min-width: 250px;
    background: $side-bg;

    &-content {
      width: 100%;
    }
  }

  .chat {
    background: $chat-bg;
    width: 100%;

    .header {
      justify-content: flex-start;
    }

    &-content {
      height: calc(100% - 50px);
      display: flex;
      flex-direction: column;
      justify-content: flex-end;
    }
  }
}
// X-Small devices (portrait phones, less than 576px)
@media (max-width: 575.98px) {
}

// Small devices (landscape phones, less than 768px)
@media (max-width: 767.98px) {
}

// Medium devices (tablets, less than 992px)
@media (max-width: 991.98px) {
}

// Large devices (desktops, less than 1200px)
@media (max-width: 1199.98px) {
}

// X-Large devices (large desktops, less than 1400px)
@media (max-width: 1399.98px) {
}
</style>
