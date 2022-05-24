<template>
  <ul class="message-list">
    <li v-for="msg in messages" :key="msg.id" class="message-list-item">
      <div
        :class="[
          user.username === msg.username ? 'message-left' : 'message-right',
        ]"
        class="message-content"
      >
        <div class="message-author">{{ msg.username }}</div>
        <div>{{ msg.text }}</div>
      </div>
    </li>
  </ul>
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
}
</script>

<style scoped lang="scss">
@import "src/assets/messenger.colors";
.message {
  &-left {
    align-self: flex-start;
  }
  &-right {
    align-self: flex-end;
    background: $message-current-user-bg !important;
  }
  &-author {
    text-align: left;
    font-weight: bold;
    color: $message-author;
  }
  &-content {
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
    min-height: 75vh;

    &-item {
      margin: 20px;
      display: flex;
      flex-direction: column;
    }
  }
}
</style>
