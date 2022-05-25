<template>
  <div class="message-list-wrapper" ref="messageListScroll">
    <ul class="message-list" ref="messageList">
      <template v-if="messages.length">
        <li v-for="msg in messages" :key="msg.id" class="message-list-item">
          <div
            :class="[
              user.username === msg.username ? 'message-left' : 'message-right',
            ]"
            class="message-content"
          >
            <div class="message-header">
              <div class="message-author">{{ msg.username }}</div>
              <div class="message-time">{{ msg.created }}</div>
            </div>
            <div>{{ msg.text }}</div>
          </div>
        </li>
      </template>
      <template v-else
        ><li class="message-list-item">
          <div class="message-content message-center">
            <div class="message-author">System</div>
            <div>Нет сообщений</div>
          </div>
        </li></template
      >
    </ul>
  </div>
</template>

<script>
export default {
  name: "MessageList",
  props: {
    messages: {
      required: true,
    },
  },
  data() {
    return {
      user: {
        username: "root41",
      },
    }
  },
  watch: {
    "messages.length"() {
      console.log("new msg")
      this.$nextTick(() => {
        this.$refs.messageListScroll.scrollTop =
          this.$refs.messageList.scrollHeight + 200
      })
    },
  },
}
</script>

<style scoped lang="scss">
@import "src/assets/messenger.colors";
.message {
  &-center {
    align-self: center;
  }
  &-left {
    align-self: flex-start;
  }
  &-right {
    align-self: flex-end;
    background: $message-current-user-bg !important;
  }

  &-header {
    display: flex;
    justify-content: space-between;
    width: 100%;
  }
  &-time {
    align-self: center;
    font-size: 10px;
  }

  &-author {
    justify-self: flex-start;
    font-weight: bold;
    color: $message-author;
  }
  &-content {
    min-width: 150px;
    background: $message-bg;
    text-align: justify;
    max-width: 80%;
    border-radius: 10px;
    padding: 10px 15px;
  }
  &-list {
    display: flex;
    flex-direction: column;
    justify-content: flex-end;

    &-wrapper {
      overflow-y: auto;
      
      &::-webkit-scrollbar {
        width: 10px;
        cursor: pointer;
      }
      &::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
      }
      &::-webkit-scrollbar-thumb {
        background-color: rgba(255, 255, 255, 0.1); /* цвет плашки */
        border-radius: 10px; /* закругления плашки */
      }
    }

    &-item {
      margin: 10px 20px;
      display: flex;
      flex-direction: column;
    }
  }
}
</style>
