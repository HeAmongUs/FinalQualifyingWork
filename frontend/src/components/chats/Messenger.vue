<template>
  <div class="messenger">
    <div class="messenger-header">
      <div class="my-left flex-center">
        <div class="messenger-header-left-content">
          <my-dropdown>
            <template v-slot:target>
              <div class="username">
                {{ username }}
              </div>
            </template>
            <template v-slot:content>
              <ul>
                <li @click="logout">
                  <span class="button">
                    <i class="material-icons left color-blue"
                      >assignment_return</i
                    >
                    Logout
                  </span>
                </li>
              </ul>
            </template>
          </my-dropdown>
          |
          <span> {{ filteredDate }}</span>
        </div>
      </div>
      <div class="my-right flex-justify-start">
        <div v-if="selectedChatId">
          {{ chats.find((c) => c.id === selectedChatId).title }}
        </div>
      </div>
    </div>
    <div class="messenger-content">
      <div class="my-left">
        <chat-list
          :chats="chats"
          v-model="selectedChatId"
          :selected="selectedChatId"
          v-model:search-input="searchInput"
        />
      </div>

      <div class="my-right">
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
  },
  async created() {
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

.my-left {
  width: 30%;
  max-width: 350px;
}
.my-right {
  width: 90%;
}
.messenger {
  color: white;
  max-width: 1600px;
  width: calc(100% - 40px);
  padding: 20px;
  font-size: 12px;
  margin: 0 auto;

  &-header {
    height: 40px;
    display: flex;

    .my-left {
      display: flex;
      background-color: $header-bg;
      border-right: 2px solid $border-list;
      font-size: 14px;

      .username {
        cursor: pointer;
        font-weight: bold;
        display: inline-block;
        transition: 0.2s;

        &:hover {
          color: $blue-main;
        }
      }
    }
    .my-right {
      display: flex;
      background-color: $header-bg;
      padding-left: 10px;
      font-size: 14px;
      font-weight: bold;
    }
  }
  &-content {
    display: flex;
    height: calc(100vh - 80px);

    .my-left {
      background: $side-bg;
    }
    .my-right {
      display: flex;
      flex-direction: column;
      justify-content: flex-end;
      background: $chat-bg;
    }
  }
}
.messenger-left {
  width: 30%;
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
  .messenger {
    padding: 0;
    width: 100%;
    height: 100%;
  }
}

// X-Large devices (large desktops, less than 1400px)
@media (max-width: 1399.98px) {
}
</style>
