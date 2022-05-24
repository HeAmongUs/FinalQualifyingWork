export default function (instance) {
  return {
    getChats() {
      return instance.get("api/v1/chats/list")
    },
    getChatMessages(chatId) {
      return instance.get(`api/v1/chats/${chatId}/messages`)
    },
  }
}
