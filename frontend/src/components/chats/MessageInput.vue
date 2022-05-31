<template>
  <form @submit.prevent="" class="form">
    <div class="input-field s6 width100">
      <textarea
        v-model.trim="messageText"
        placeholder="Введите сообщение"
        type="text"
        class="materialize-textarea"
        @keydown.enter.exact.prevent
        @keyup.enter.exact="sendMessageHandler"
        @keydown.enter.shift.exact="newline"
      />
    </div>
    <div class="send-btn" v-if="!isDisabled" @click="sendMessageHandler">
      <i class="material-icons color-blue-hover">send</i>
    </div>
  </form>
</template>

<script>
export default {
  name: "MessageInput",
  data() {
    return {
      messageText: "",
    }
  },
  methods: {
    sendMessageHandler() {
      this.$emit("sendMessage", this.messageText)
    },
    newline() {
      this.messageText = `${this.messageText}\n`
    },
  },
  computed: {
    isDisabled() {
      if (this.messageText) {
        return false
      } else return true
    },
  },
}
</script>

<style scoped lang="scss">
@import "../../assets/messenger.colors";
.send-btn {
  padding: 10px 10px 12px;
  display: flex;
  align-items: flex-end !important;

  i {
    cursor: pointer;
  }
}
.input-field {
  margin: 0;
  max-width: calc(100% - 50px);
  position: relative;
}
button {
  align-items: flex-end !important;
}
textarea {
  border: none;
  background: $input-bg;
  padding: 10px;
  justify-content: center;
  min-height: 30px;
  border-radius: 5px;
  color: $white;
  margin-bottom: 0;
  max-height: 150px;
  overflow-y: auto;
  overflow-x: hidden;

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
.form {
  display: flex;
  width: 100%;
  background: $message-input-panel-bg;
  padding: 10px;
}
.width100 {
  width: 100%;
}
</style>
