<template>
  <div class="chat-list-wrapper">
    <div class="search-input">
      <div class="input-field s6">
        <i class="icon-prefix material-icons flex-center tiny absolute"
          >search</i
        >
        <input v-model.lazy="lazySearchInput" type="text" placeholder="Поиск" />
      </div>
    </div>
    <ul class="chat-list">
      <li
        v-for="chat in chats"
        @click="updateSelected(chat.id)"
        :key="chat.id"
        :class="[selected === chat.id ? 'selected' : '']"
        class="chat-list-item"
      >
        <div class="chat-list-item__icon">
          <i
            class="material-icons small bg-transparent"
            :class="[selected === chat.id ? 'color-blue' : '']"
            >chat</i
          >
        </div>
        <div class="chat-list-item-info">
          <div class="chat-list-item__title">{{ chat.title }}</div>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: "ChatList",

  props: {
    chats: {
      required: true,
    },
    selected: {
      required: false,
      type: Number,
    },
  },
  data() {
    return {
      lazySearchInput: "",
      selectedChatGroupValue: "my",
    }
  },
  methods: {
    updateSelected(selectedChatId) {
      this.$emit("update:modelValue", selectedChatId)
    },
  },
  watch: {
    lazySearchInput() {
      this.$emit("update:searchInput", this.lazySearchInput)
    },
  },
}
</script>

<style scoped lang="scss">
@import "../../assets/messenger.colors";
.search-input {
  padding: 5px 10px;
}
input {
  border-radius: 10px !important;
  background: $input-bg !important;
  color: $white;
  height: 40px !important;
  font-size: 13px !important;

  &::placeholder {
    font-size: 12px;
  }
}
.selected {
  background: rgba(255, 240, 255, 0.15);
  font-weight: bold;
}
.bg-transparent {
  background: transparent;
}
.chat-list {
  &-wrapper {
  }
}
.chat-list-item {
  display: flex;
  height: 60px;
  transition: 0.2s;

  &:hover {
    cursor: pointer;
    background: rgba(255, 255, 255, 0.1);
  }
}
.chat-list-item__icon {
  width: 100px;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}
.chat-list-item-info {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: flex-start;
  align-items: center;
  border-top: 2px solid $border-list;
}

.input-field {
  margin: 0;
}
</style>
